#!/usr/bin/env python3
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

class CarVersionInput(graphene.InputObjectType):
    version_id  = graphene.Int()
    price = graphene.Float()
    name = graphene.String()
    fuel_type = graphene.String()
    year = graphene.Int()

class createCar(graphene.Mutation):
    car_version = graphene.Field(Version)

    class Arguments:
        car_data = CarVersionInput()

    def mutate(root, info, car_data):
        car_version = Version(
            version_id = car_data.version_id,
            price = car_data.price,
            name = car_data.name,
            fuel_type = car_data.fuel_type,
            year = car_data.year
        )
        car_version.save()
        return createCar(car_version=car_version)
    
class Mutation(graphene.ObjectType):
    create_car = createCar.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, types=[Mark, Car, Version])
