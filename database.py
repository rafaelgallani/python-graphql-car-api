#!/usr/bin/env python3
from mongoengine import connect
import random
from models import Brand, Car, Version

# database is mocked, the connection string could be any one with a valid mongodb instance.
connect('car-database-mock', host='mongomock://localhost', alias='default')

def init_db():

    brand = Brand(name='Ford', brand_id=1, country='US').save()
    Brand(name='Ford2', brand_id=2, country='US').save()
    brand.save()

    fiesta = Car(brand=brand, name='Fiesta', car_id=1)
    edge = Car(brand=brand, name='Edge', car_id=2)
    ecosport = Car(brand=brand, name='Ecosport', car_id=3)
    ka = Car(brand=brand, name='Ka', car_id=4)

    flex_counter = 0
    gas_counter = 0

    for car in [fiesta, edge, ecosport, ka]:
        
        flex_counter += 1
        gas_counter  += 1

        car.save()
        
        flex_version = Version(price=random.randrange(0, 50000), model=car, name='{name} {fuel} - {year}'.format(name=car.name, fuel='Flex', year=2011, version_id=flex_counter))
        gasoline_version = Version(price=random.randrange(0, 50000), model=car, name='{name} {fuel} - {year}'.format(name=car.name, fuel='Gasolina', year=2011, version_id=gas_counter))
        
        flex_version.save()
        gasoline_version.save()