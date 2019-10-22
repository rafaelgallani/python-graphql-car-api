# flask_graphene_mongo/schema.py
import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Mark as MarkModel
from models import Car as CarModel
from models import Version as VersionModel

class Mark(MongoengineObjectType):

    class Meta:
        model = MarkModel
        interfaces = (Node,)


class Car(MongoengineObjectType):

    class Meta:
        model = CarModel
        interfaces = (Node,)


class Version(MongoengineObjectType):

    class Meta:
        model = VersionModel
        interfaces = (Node,)


class Query(graphene.ObjectType):
    node = Node.Field()
    all_versions = MongoengineConnectionField(Version)
    all_cars = MongoengineConnectionField(Car)
    car = graphene.Field(Car)

schema = graphene.Schema(query=Query, types=[Mark, Car, Version])