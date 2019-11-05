#!/usr/bin/env python3
from mongoengine import Document
from mongoengine.fields import (
    StringField, IntField, DecimalField, ReferenceField
)

class Brand(Document):
    meta = {'collection': 'brand'}
    name = StringField()
    country = StringField()
    brand_id = IntField()

class Car(Document):
    meta = {'collection': 'car'}
    name = StringField()
    brand = ReferenceField(Brand)
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