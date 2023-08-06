from enum import Enum

class EyeColor(str, Enum):
  blue = '蓝色'
  black = '黑色'
  green = '绿色'
  other = '褐色'
  brown = '其他'


class HairColor(str, Enum):
  blue = '蓝发'
  black = '黑发'
  red = '红发'
  other = '金发'
  blond = '其他'


class Ethnicity(str, Enum):
  asian = '亚洲'
  caucasian = '白人'
  australian = '澳大利亚人'


class BuildType(str, Enum):
  slender = '高挑'
  fit = '匀称'
  skinny = '苗条'
  athletic = '健美'
  chunky = '结实'


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
  english = '英文'
  chinese = '普通话'
  japanese = '日语'
  korea = '韩语'
  cantonese = '广东话'


class PaymentMethod (str, Enum):
  card = '刷卡'
  cash = '先进'
  pay_id = 'PayID'

class TimeSlotStatus(str, Enum):
  available = '空闲'
  booked = '订满'
  locked = '上锁'

class BookingStatus(str, Enum):
  attempt = '预定中'
  confirmed = '已经预定'
  cancel_attemp = '取消中'
  cancel_confirmed = '已取消'  # ?? need this or directly delete
  fulfilled = '已完成'
  archived = '已归档'
  deleted = '已删除'  # need this? or simply delete it. as _id will conflict