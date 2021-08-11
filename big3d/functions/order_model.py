from datetime import datetime

from base import BaseModel
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute


class OrderModel(BaseModel):

    amount = UnicodeAttribute()
    user = UnicodeAttribute()
    details = JSONAttribute()
