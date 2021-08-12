from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

# Base class to handle common operations
# Replace the host with the url of the db on aws
class Base(Model):
    class Meta:
        table_name = "dynamodb-" + cls.__name__
        host = ""

    id = UnicodeAttribute(hash_key=True)

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
