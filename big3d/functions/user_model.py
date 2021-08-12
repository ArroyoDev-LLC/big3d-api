from datetime import datetime

from base import BaseModel
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute


class UserModel(BaseModel):

    first_name = UnicodeAttribute()
    last_name = UnicodeAttribute()
    password = UnicodeAttribute()
    email = UnicodeAttribute()
    address = UnicodeAttribute()
    billing_address = UnicodeAttribute()
