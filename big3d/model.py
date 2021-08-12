import uuid

from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute


class Big3D(Model):
    class Meta:
        table_name = "dynamodb-Big3D"
        region = "us-east-1"
        host = ""

    order_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(range_key=True)
    created_at = UTCDateTimeAttribute()
    order_details = JSONAttribute()

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
