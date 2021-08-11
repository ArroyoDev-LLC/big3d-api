from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class Base(Model):
    class Meta:
        table_name = "dynamodb-" + cls.__name__
        host = ""

    id = UnicodeAttribute()

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
