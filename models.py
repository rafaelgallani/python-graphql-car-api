from mongoengine import Document
from mongoengine.fields import (
    StringField, IntField, DecimalField, ReferenceField
)

class Mark(Document):
    meta = {'collection': 'mark'}
    name = StringField()
    country = StringField()
    id = IntField()

class Car(Document):
    meta = {'collection': 'car'}
    name = StringField()
    mark = ReferenceField(Mark)
    id = IntField()

class Version(Document):
    meta = {'collection': 'version'}
    name = StringField()
    model = ReferenceField(Car)
    price = DecimalField()
    fuelType = StringField()
    fipeCode = StringField()
    year = IntField()