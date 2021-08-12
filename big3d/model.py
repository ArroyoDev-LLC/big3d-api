import uuid

from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute

from big3d.utils import validate_incoming_data


class big3D_table(Model):
    class Meta:
        table_name = "dynamodb-big3D"
        host = "http://localhost:8000"

    order_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(range_key=True)
    created_at = UTCDateTimeAttribute()
    order_details = JSONAttribute()

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            yield name, attr.serialize(getattr(self, name))


big3D_table.create_table(read_capacity_units=1, write_capacity_units=1)
