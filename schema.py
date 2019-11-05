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
    all_marks = MongoengineConnectionField(Mark)
    car = graphene.Field(Car)

class CarVersionInput(graphene.InputObjectType):
    version_id  = graphene.Int()
    price = graphene.Float()
    name = graphene.String()
    fuel_type = graphene.String()
    year = graphene.Int()

class CarMarkInput(graphene.InputObjectType):
    country = graphene.String()
    name = graphene.String()
    mark_id = graphene.Int()

class createCar(graphene.Mutation):
    car_version = graphene.Field(Version)

    class Arguments:
        car_data = CarVersionInput()

    def mutate(root, info, car_data):
        car_version = VersionModel(
            version_id = car_data.version_id,
            price = car_data.price,
            name = car_data.name,
            fuelType = car_data.fuel_type,
            year = car_data.year
        )
        car_version.save()
        return createCar(car_version=car_version)

class createMark(graphene.Mutation):
    mark = graphene.Field(Mark)

    class Arguments:
        mark = CarMarkInput()

    def mutate(root, info, mark):
        mark_obj = MarkModel(
            name = mark.name,
            country = mark.country,
            mark_id = mark.mark_id
        )
        mark_obj.save()
        return createMark(mark=mark_obj)

class editMark(graphene.Mutation):
    mark = graphene.Field(Mark)

    class Arguments:
        mark = CarMarkInput()

    def mutate(root, info, mark):
        mark_obj = MarkModel.objects.get(mark_id=mark.mark_id)
        
        mark_obj.name = mark.name
        mark_obj.country = mark.country
        
        mark_obj.save()
        return createMark(mark=mark_obj)
    
class Mutation(graphene.ObjectType):
    create_car = createCar.Field()
    create_mark = createMark.Field()
    edit_mark = editMark.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, types=[Mark, Car, Version])
