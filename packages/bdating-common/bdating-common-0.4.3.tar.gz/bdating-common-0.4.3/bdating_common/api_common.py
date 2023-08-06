import os
import logging
import enum

from pydantic import BaseSettings

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from fastapi import FastAPI, Depends, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from bdating_common.model import HealthResponse, ConsumerProfile
from bdating_common import model as model_package

from bdating_common.auth0_token_helper import IllegalTokenExcpetion, Auth0TokenVerifier
from fastapi.responses import JSONResponse
from bdating_common.es_helper import es_get_result_to_dict

import redis
from auth0.v3.authentication import Users as Auth0Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def get_model_enum_values():
    model_enums= {}
    for name in dir(model_package):
        if not name.startswith('__') and name != 'Enum' and type(model_package.__dict__[name]) == enum.EnumMeta:
            model_enums[name] = [
                model_package.__dict__[name].__dict__[variable_name].value
                for variable_name in dir(model_package.__dict__[name]) if not variable_name.startswith('__')
            ]
    return model_enums

class Settings(BaseSettings):
    app_name: str = 'StandardBdatingAPI'
    app_namespace: str = os.getenv('NAMESPACE', "")
    admin_email: str = "admin@bdating.io"
    app_type: str = 'consumer'
    es_endpoint: str = os.getenv('ELASTICSEARCH_HOSTS')
    es_index: str = 'bdating'
    auth0_namespace: str = 'https://app.bdating.io/'
    redis_host: str = os.getenv('REDIS_HOST')
    redis_port: int = 6379
    redis_password: str = os.getenv('REDIS_PASSWORD')
    cors_origins: str = os.getenv('CORS_ORIGINS', 'http://localhost:3000')
    token_cache_db_id: int = 0
    lock_db_id: int = 1


settings = Settings()
token_auth_scheme = HTTPBearer()
token_verifier = Auth0TokenVerifier()

token_cache_redis = None # TODO rework the global clients.

def _get_uid(token: str):
    log = logging.getLogger(__name__)
    global token_cache_redis
    if settings.redis_host:
        if token_cache_redis is None:
            token_cache_redis = redis.Redis(
                settings.redis_host, settings.redis_port,
                db=settings.token_cache_db_id,
                password=settings.redis_password
                )
        cached_value = token_cache_redis.get(token)
        if cached_value is not None:
            return cached_value.decode('utf-8')
    try:
        payload = token_verifier.verify(token)
        if payload.get("status") == 'error':
            raise IllegalTokenExcpetion()
        uid = payload.get(f"{settings.auth0_namespace}uid")
        log.warn('uid retrieved is %s', uid)
        if token_cache_redis is not None and uid:
            ttl = 86400 * 1000 # hard code 1 day, ttl value is in milliseconds
            token_cache_redis.setex(token, ttl, uid)
        return uid
    except Exception as e:
        log.warn('Token verification failed', exc_info=True)
        raise IllegalTokenExcpetion(e)

def get_uid(token: str, token_verifier: object):
    log = logging.getLogger(__name__)
    global token_cache_redis
    if settings.redis_host:
        if token_cache_redis is None:
            token_cache_redis = redis.Redis(
                settings.redis_host, settings.redis_port,
                db=settings.token_cache_db_id,
                password=settings.redis_password
                )
        cached_value = token_cache_redis.get(token.credentials)
        if cached_value is not None:
            return cached_value.decode('utf-8')
    try:
        result = token_verifier.verify(token.credentials)
        log.warn('result %s', result)
        if result.get("status") == 'error':
            raise IllegalTokenExcpetion()
        domain = os.environ.get('DOMAIN')
        log.warn('domain %s', domain)
        users = Auth0Users(domain)
        userinfo = users.userinfo(token.credentials)
        log.warn('userinfo %s', userinfo);
        uid = userinfo.get(f"{settings.auth0_namespace}uid")
        #value = result.get(f"{settings.auth0_namespace}uid")
        #log.warn('uid retrieved is %s', value)
        if token_cache_redis is not None and uid:
            ttl = 86400 * 1000 # hard code 1 day, ttl value is in milliseconds
            token_cache_redis.setex(token.credentials, ttl, uid)
        return uid
    except Exception as e:
        log.warn('Token verification failed', exc_info=True)
        raise IllegalTokenExcpetion(e)

def get_contact(token: str):
    log = logging.getLogger(__name__)
    try:
        payload = token_verifier.verify(token)
        if payload.get('status') == 'error':
            raise IllegalTokenExcpetion()
        contact = payload.get(f"{settings.auth0_namespace}name")
        return contact
    except Exception as e:
        log.warn('Token verification failed', exc_info=True)
        raise IllegalTokenExcpetion(e)

def create_app():
    app = FastAPI(title=settings.app_name)
    es = Elasticsearch(settings.es_endpoint)

    @ app.get("/health", response_model=HealthResponse)
    def get_health():
        return {"status": "OK"}

    @app.exception_handler(NotFoundError)
    async def es_not_found_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder({"detail": "Not found"}),)

    @app.exception_handler(IllegalTokenExcpetion)
    async def illegal_Auth0_token_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=jsonable_encoder({"detail": "Illegal token"}),)

    @app.get("/me")
    def get_own_profile_info(token: str = Depends(token_auth_scheme)):
        """
        Find this user's own profile info.
        """
        uid = get_uid(token, token_verifier)
        return es_get_result_to_dict(es.get(index=settings.es_index, id=f"{uid}:{settings.app_type}"))

    @app.patch("/me")
    def update_own_profile_info(profile: ConsumerProfile, token: str = Depends(token_auth_scheme)):
        """
        Update the profile for the user.
        If the profile does not exist, create it in the first place.
        """
        log = logging.getLogger(__name__)

        profile = jsonable_encoder(profile)
        log.debug('profile %s', profile)
        log.debug('token %s', token)
        uid = get_uid(token, token_verifier)
        return {}
        return es.update(index=settings.es_index, id=f"{uid}:{settings.app_type}", doc_as_upsert=True, doc=profile)

    @app.get('/config/app')
    def get_app_config():
        """get application default configuration"""
        model_info= get_model_enum_values()
        result = {
            "enum_values": model_info
            }
        return result

    if settings.cors_origins:
        origins = settings.cors_origins.split(',')
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    return app
