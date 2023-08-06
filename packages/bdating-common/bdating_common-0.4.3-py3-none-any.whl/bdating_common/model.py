
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
# data model


class Location(BaseModel):
  lat: float
  lon: float


class BaseProfile(BaseModel):
  wallet: Optional[str]
  uid: Optional[str]
  name: str
  referrer: str = None
  gender: str = None
  register_timestamp: int = 0


class EyeColor(str, Enum):
  blue = 'blue'
  black = 'black'
  green = 'green'
  other = 'other'
  brown = 'brown'


class HairColor(str, Enum):
  blue = 'blue'
  black = 'black'
  red = 'red'
  other = 'other'
  blond = 'blond'


class Ethnicity(str, Enum):
  asian = 'asian'
  caucasian = 'caucasian'
  australian = 'australian'


class BuildType(str, Enum):
  slender = 'slender'
  fit = 'fit'
  skinny = 'skinny'
  athletic = 'athletic'
  chunky = 'chunky'


class BuildType(str, Enum):
  slender = 'slender'
  fit = 'fit'
  skinny = 'skinny'
  athletic = 'athletic'
  chunky = 'chunky'


class BustSize(str, Enum):
  a = 'a'
  b = 'b'
  c = 'c'
  d = 'd'
  e = 'e'
  f = 'f'
  g_plus = 'g+'


class DressSize(str, Enum):
  small = 'small'
  medium = 'medium'
  large = 'large'
  large_plus = 'large+'
  small_minus = 'small-'


class SpeakingLanguage (str, Enum):
  english = 'english'
  chinese = 'chinese'
  japanese = 'japanese'
  korea = 'korean'


class ProviderProfile(BaseProfile):
  address: str
  postcode: Optional[int]
  city: Optional[str]
  country: Optional[str]
  age: int = 27
  location: Location
  contact_detail: str = None
  rate_aud: int = 150
  hair_color: Optional[HairColor]
  build: Optional[BuildType]
  ethnicity: Optional[Ethnicity]
  eye_color: Optional[EyeColor]
  bio: Optional[str]
  photos: List[str] = []
  height: Optional[int]
  bust: Optional[BustSize]
  rating: Optional[float]
  dress_size: Optional[DressSize]
  speaking_language: List[SpeakingLanguage] = []


class ConsumerProfile(BaseProfile):
  pass


class TimeSlotStatus(str, Enum):
  available = 'available'
  booked = 'booked'
  locked = 'locked'


class TimeSlot(ProviderProfile):
  slot_id: int  # the slot id, YYYYmmddXX
  slot_status: TimeSlotStatus = TimeSlotStatus.available


# details of a booking, which is shown to the provider and consumer
class BookingDetail(TimeSlot):
  total_fee_aud: int


class BookingHistory(BaseModel):  # state chagen history of a booking
  ationer: str
  timestamp: int
  additional_comment: Optional[str]


class BookingStatus(str, Enum):
  attempt = 'attempt'
  confirmed = 'confirmed'
  cancel_attempt = 'cancel_attempt'
  cancel_confirmed = 'cancel_confirmed'  # ?? need this or directly delete
  fulfilled = 'fulfilled'
  archived = 'archived'
  deleted = 'deleted'  # need this? or simply delete it. as _id will conflict


class Booking(BaseModel):  # booking to a timeslot
  consumer_uid: str
  provider_uid: str
  all_slots: List[int] = []
  status: BookingStatus
  consumer_comments: Optional[str]
  consumer_rating: Optional[float]
  provider_comments: Optional[str]
  provider_rating: Optional[float]
  last_update: int
  detail: BookingDetail
  total_fee_aud: int
  book_time: int  # epoch second of booked
  history: List[BookingHistory] = []


class Transaction(BaseModel):
  consumer_uid: str
  provider_uid: str
  booking: Booking
  timestamp: int
  total_fee_aud: int


# response model


class SingleProviderResponse(ProviderProfile):
  pass


class SingleConsumerResponse(ConsumerProfile):
  pass


class SingleTimeSlotResponse(TimeSlot):
  pass


class SingleBookingResponse(Booking):
  pass


class SingleTransactionResponse(Transaction):
  pass


class ProviderListResponse(BaseProfile):
  results: List[ProviderProfile] = []
  start: Optional[int]
  total_size: Optional[int]
  next_cursor: Optional[str]


class TimeSlotListResponse(BaseProfile):
  results: List[TimeSlot] = []
  start: Optional[int]
  total_size: Optional[int]
  next_cursor: Optional[str]


class BookingListResponse(BaseProfile):
  results: List[Booking] = []
  start: Optional[int]
  total_size: Optional[int]
  next_cursor: Optional[str]


class OrderListResponse(BaseProfile):
  results: List[Booking] = []
  start: Optional[int]
  total_size: Optional[int]
  next_cursor: Optional[str]

# general model


class HealthResponse(BaseModel):
  status: str
