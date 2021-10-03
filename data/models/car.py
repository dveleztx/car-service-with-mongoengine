# Imports
import mongoengine
import uuid
# Custom Imports
from data.models.engine import Engine
from data.models.service_record import ServiceRecord


class Car(mongoengine.Document):
    # id # --> _id = ObjectId()...
    make = mongoengine.StringField(required=True)
    model = mongoengine.StringField(required=True)
    year = mongoengine.IntField(required=True)
    mileage = mongoengine.FloatField(default=0.0)
    vi_number = mongoengine.StringField(
        default=lambda: str(uuid.uuid4()).replace("-", "")
    )

    engine = mongoengine.EmbeddedDocumentField(Engine, required=True)
    service_history = mongoengine.EmbeddedDocumentListField(ServiceRecord)

    # db.cars.createIndex({"service_history.customer_rating": 1},
    # {background:true, name: "Customer ratings of service index"})
    meta = {
        "db_alias": "core",
        "collection": "cars",
        "indexes": [
            'mileage',
            'year',
            "service_history.price",
            "service_history.description",
            {
                "fields": [
                    "service_history.price",
                    "service_history.description",
                ]
            },
        ]
    }
