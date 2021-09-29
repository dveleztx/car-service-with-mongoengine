# Imports
import mongoengine
import uuid


class Engine(mongoengine.EmbeddedDocument):
    horsepower = mongoengine.IntField(required=True)
    liters = mongoengine.FloatField(required=False)
    mpg = mongoengine.FloatField(required=True)
    serial_number = mongoengine.StringField(
        default=lambda: str(uuid.uuid4())
    )
