#!/usr/bin/env python3
from mongoengine import connect
from models import Mark, Car, Version

# database is mocked, the connection string could be any one with a valid mongodb instance.
connect('car-database-mock', host='mongomock://localhost', alias='default')

def init_db():

    mark = Mark(name='Ford', mark_id=1, country='US')
    mark.save()

    fiesta = Car(mark=mark, name='Fiesta', car_id=1)
    edge = Car(mark=mark, name='Edge', car_id=2)
    ecosport = Car(mark=mark, name='Ecosport', car_id=3)
    ka = Car(mark=mark, name='Ka', car_id=4)

    flex_counter = 0
    gas_counter = 0

    for car in [fiesta, edge, ecosport, ka]:
        
        flex_counter += 1
        gas_counter  += 1

        car.save()
        
        flex_version = Version(model=car, name='{name} {fuel} - {year}'.format(name=car.name, fuel='Flex', year=2011, version_id=flex_counter))
        gasoline_version = Version(model=car, name='{name} {fuel} - {year}'.format(name=car.name, fuel='Gasolina', year=2011, version_id=gas_counter))
        
        flex_version.save()
        gasoline_version.save()