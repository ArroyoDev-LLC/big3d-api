from datetime import datetime

from base import BaseModel
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute


class OrderModel(BaseModel):

    amount = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute()
    created_at = UTCDateTimeAttribute()

    # Dump any additional information here,
    # tracking number, static files, etc.
    order_details = JSONAttribute()
