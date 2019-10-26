# Car Data API - GraphQL + Python + MongoDB
A car data API built using GraphQL as query language protocol for the data. 
The project was developed with Python 3.7, using graphene for the GraphQL implementation. 
The server is running with Flask. MongoDB is used as the database. Initially, was a local mock. 

## Queries

All queries are described with GraphiQL, in the main page. Still, here's a brief description on them:

### allVersions
```
allVersions(
    before: String
    after: String
    first: Int
    last: Int
    fipeCode: String
    fuelType: String
    id: ID
    name: String
    price: Float
    versionId: Int
    year: Int
    model: ID
): VersionConnection
```

### allCars
```
allCars(
    before: String
    after: String
    first: Int
    last: Int
    carId: Int
    id: ID
    name: String
    mark: ID
): CarConnection
```

## Mutations
The existent mutations are also described in GraphiQL. In short:

### createCar

  

Example: http://localhost:5000/cars?query=mutation%20createCar(%24car%3A%20CarVersionInput!)%20%7B%0A%20%20createCar(carData%3A%20%24car)%7B%0A%20%20%20%20carVersion%20%7B%0A%20%20%20%20%20%20id%2C%0A%20%20%20%20%20%20name%2C%0A%20%20%20%20%20%20price%2C%0A%20%20%20%20%7D%20%20%0A%20%20%7D%0A%7D&operationName=createCar&variables=%7B%0A%20%20%22car%22%3A%20%7B%0A%20%20%20%20%22versionId%22%3A%20123123%2C%0A%20%20%20%20%22price%22%3A%205555%2C%0A%20%20%20%20%22name%22%3A%20%22Teste%20Rafael%22%2C%0A%20%20%20%20%22fuelType%22%3A%20%22Gasolina%22%2C%0A%20%20%20%20%22year%22%3A%202019%0A%20%20%7D%0A%7D%20%20

  
  

#### Declaration:

  

```
mutation createCar($car: CarVersionInput!) {
	createCar(carData: $car){
		carVersion {
			id,
			name,
			price
		}
	}
}
```

  

#### Variables:

  

```
{
	"car": {
		"versionId": 123123,
		"price": 5555,
		"name": "Teste Rafael",
		"fuelType": "Gasolina",	
		"year": 2019
	}
}
```

### createModel:
Example: http://localhost:5000/cars?query=mutation%20(%24mark%3A%20CarModelInput)%7B%0A%09createMark(mark%3A%20%24mark)%7B%0A%20%20%20%20mark%7B%0A%20%20%20%20%20%20country%2C%20name%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D&operationName=undefined&variables=%7B%0A%20%20%22mark%22%3A%20%7B%0A%20%20%20%20%22country%22%3A%20%22Brasil%22%2C%0A%20%20%20%20%22markId%22%3A%20321%2C%0A%20%20%20%20%22name%22%3A%20%22Rafael%20Autom%C3%B3veis%22%0A%20%20%7D%0A%7D

#### Declaration:
```
mutation ($mark: CarModelInput){
	createMark(mark: $mark){
		mark{
			country,  name
		}
	}
}
```

#### Variables:
```
{
	"mark": {
		"country": "Brasil",
		"markId": 321,
		"name": "Rafael Automóveis"
	}
}
```