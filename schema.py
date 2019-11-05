#!/usr/bin/env python3
import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Brand as BrandModel
from models import Car as CarModel
from models import Version as VersionModel

class Brand(MongoengineObjectType):

    class Meta:
        model = BrandModel
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
    all_brands = MongoengineConnectionField(Brand)
    # car = graphene.Field(Car)

class CarVersionInput(graphene.InputObjectType):
    version_id  = graphene.Int()
    price = graphene.Float()
    name = graphene.String()
    fuel_type = graphene.String()
    year = graphene.Int()

class CarModelInput(graphene.InputObjectType):
    name   = graphene.String()
    brand   = graphene.Int()
    car_id = graphene.Int()

class CarBrandInput(graphene.InputObjectType):
    country = graphene.String()
    name = graphene.String()
    brand_id = graphene.Int()

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

        brand = BrandModel.objects.get(brand_id=car.brand)

        car_model = CarModel(
            name   = car.name,
            brand   = brand.id,
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


class createBrand(graphene.Mutation):
    brand = graphene.Field(Brand)

    class Arguments:
        brand = CarBrandInput()

    def mutate(root, info, brand):
        if not brand.brand_id:
            brand.brand_id = len(BrandModel.objects) + 1
            
        brand_obj = BrandModel(
            name = brand.name,
            country = brand.country,
            brand_id = brand.brand_id
        )
        brand_obj.save()
        return createBrand(brand=brand_obj)

class editBrand(graphene.Mutation):
    brand = graphene.Field(Brand)
    class Arguments:
        brand = CarBrandInput()

    def mutate(root, info, brand):
        brand_obj = BrandModel.objects.get(brand_id=brand.brand_id)
        
        brand_obj.name = brand.name
        brand_obj.country = brand.country
        
        brand_obj.save()
        return createBrand(brand=brand_obj)

class deleteBrand(graphene.Mutation):
    brand = graphene.Field(Brand)

    class Arguments:
        brand = CarBrandInput()

    def mutate(root, info, brand):
        index = [ m.brand_id for m in BrandModel.objects ].index(brand.brand_id)
        
        BrandModel.objects[index].delete()
        return createBrand(brand=None)
    
class Mutation(graphene.ObjectType):
    
    create_model = createModel.Field()
    edit_model = editModel.Field()
    delete_model = deleteModel.Field()

    create_brand = createBrand.Field()
    edit_brand = editBrand.Field()
    delete_brand = deleteBrand.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, types=[Brand, Car, Version])
