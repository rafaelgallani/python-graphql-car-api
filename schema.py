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
    # car = graphene.Field(Car)

class CarVersionInput(graphene.InputObjectType):
    version_id  = graphene.Int()
    price = graphene.Float()
    name = graphene.String()
    fuel_type = graphene.String()
    year = graphene.Int()

class CarModelInput(graphene.InputObjectType):
    name   = graphene.String()
    mark   = graphene.Int()
    car_id = graphene.Int()

class CarMarkInput(graphene.InputObjectType):
    country = graphene.String()
    name = graphene.String()
    mark_id = graphene.Int()

# class createVersion(graphene.Mutation):
#     car_version = graphene.Field(Version)

#     class Arguments:
#         car_data = CarVersionInput()

#     def mutate(root, info, car_data):
#         car_version = VersionModel(
#             version_id = car_data.version_id,
#             price = car_data.price,
#             name = car_data.name,
#             fuelType = car_data.fuel_type,
#             year = car_data.year
#         )
#         car_version.save()
#         return createVersion(car_version=car_version)

class createModel(graphene.Mutation):
    car = graphene.Field(Car)

    class Arguments:
        car = CarModelInput()

    def mutate(root, info, car):

        if not car.car_id:
            car.car_id = len(CarModel.objects) + 1

        mark = MarkModel.objects.get(mark_id=car.mark)

        car_model = CarModel(
            name   = car.name,
            mark   = mark.id,
            car_id = car.car_id
        )
        car_model.save()
        return createModel(car=car_model)

class editModel(graphene.Mutation):
    car = graphene.Field(Car)
    class Arguments:
        car = CarModelInput()

    def mutate(root, info, car):
        
        model_obj = CarModel.objects.get(car_id=car.car_id)
        
        model_obj.name = car.name
        
        model_obj.save()
        return editModel(car=model_obj)

class deleteModel(graphene.Mutation):
    car = graphene.Field(Car)

    class Arguments:
        car = CarModelInput()

    def mutate(root, info, car):
        index = [ m.car_id for m in CarModel.objects ].index(car_data.car_id)
        
        CarModel.objects[index].delete()
        return deleteModel(car=None)


class createMark(graphene.Mutation):
    mark = graphene.Field(Mark)

    class Arguments:
        mark = CarMarkInput()

    def mutate(root, info, mark):
        if not mark.mark_id:
            mark.mark_id = len(MarkModel.objects) + 1
            
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

class deleteMark(graphene.Mutation):
    mark = graphene.Field(Mark)

    class Arguments:
        mark = CarMarkInput()

    def mutate(root, info, mark):
        index = [ m.mark_id for m in MarkModel.objects ].index(mark.mark_id)
        
        MarkModel.objects[index].delete()
        return createMark(mark=None)
    
class Mutation(graphene.ObjectType):
    
    create_model = createModel.Field()
    edit_model = editModel.Field()
    delete_model = deleteModel.Field()

    create_mark = createMark.Field()
    edit_mark = editMark.Field()
    delete_mark = deleteMark.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, types=[Mark, Car, Version])
