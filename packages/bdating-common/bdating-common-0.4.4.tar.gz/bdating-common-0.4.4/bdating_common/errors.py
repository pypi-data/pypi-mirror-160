GENERAL_ERROR = 'GENERAL_ERROR'
GENERAL_ERROR_MESSAGE = 'Something is wrong.'
def create_error(code: str=GENERAL_ERROR, message: str=GENERAL_ERROR_MESSAGE, exception: Exception = None):
    if exception is not None:
        message = message + "Exception: " + str(exception)
    return {
        'error' : {
            'code': code,
            'message': message
        }
    }
