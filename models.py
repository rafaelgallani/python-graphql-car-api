#!/usr/bin/env python3
from mongoengine import Document
from mongoengine.fields import (
    StringField, IntField, DecimalField, ReferenceField
)

class Mark(Document):
    meta = {'collection': 'mark'}
    name = StringField()
    country = StringField()
    mark_id = IntField()

class Car(Document):
    meta = {'collection': 'car'}
    name = StringField()
    mark = ReferenceField(Mark)
    car_id = IntField()

class Version(Document):
    meta = {'collection': 'version'}
    name = StringField()
    model = ReferenceField(Car)
    price = DecimalField()
    fuelType = StringField()
    fipeCode = StringField()
    year = IntField()
    version_id = IntField()