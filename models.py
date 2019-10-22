from mongoengine import Document
from mongoengine.fields import (
    StringField, IntField, DecimalField, ReferenceField
)

class Mark(Document):
    meta = {'collection': 'mark'}
    name = StringField()
    country = StringField()
    id = IntField()

class Model(Document):
    meta = {'collection': 'model'}
    name = StringField()
    mark = ReferenceField(Mark)
    id = IntField()

class Version(Document):
    meta = {'collection': 'modelVersion'}
    name = StringField()
    model = ReferenceField(Model)
    price = DecimalField()
    fuelType = StringField()
    fipeCode = StringField()
    year = IntField()