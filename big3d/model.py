import uuid

from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute

from utils import validate_incoming_data


class big3D_table(Base):
    class Meta:
        table_name = "dynamodb-big3D"
        host = "https://localhost:8000"

    order_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(sort_key=True)
    created_at = UTCDateTimeAttribute()
    order_details = JSONAttribute()

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
