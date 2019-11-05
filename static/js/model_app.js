allBrandsQuery = (
    `
    {
        allBrands {
            edges {
                node {
                    id,
                    country,
                    brandId,
                    name
                }
            }
        }
    }
    `
);
allModelsQuery = (
    `
    {
        allCars {
            edges {
                node {
                    id,
                    carId,
                    name,
                    brand {
                        country,
                        name,
                        id,
                        brandId
                    }
                }
            }
        }
    }
    `
);

createModelMutation = (
    `
    mutation($car: CarModelInput) {
        createModel(car: $car) {
            car {
                carId,
                name,
                brand {
                    name,
                    country,
                    brandId
                }
            }
        }
    }
    `
);

deleteModelMutation = (
    `mutation($car: CarModelInput) {
        deleteModel(car: $car) {
            car {
                carId,
                name,
                brand {
                    name,
                    country,
                    brandId
                }
            }
        }
    }`
);

editModelMutation = `
    mutation($car: CarModelInput) {
        editModel(car: $car) {
            car {
                carId,
                name,
                brand {
                    name,
                    country,
                    brandId
                }
            }
        }
    }
    `;

var app = angular.module('app', []);
app.controller('ModelController', ['$scope', function(scope){
    
    scope.newModel = {};
    scope.brands = [];
    scope.models = [];

    /*                  BRANDS                              */

    fetch('http://localhost:5000/api?', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "query": allBrandsQuery,
            "variables": null,
            "operationName": null,
        })
    }).then(r => {
        return r.json().then(result => {
            scope.brands = result.data.allBrands.edges.map(a => a.node)

            if (scope.brands.length){
                scope.newModel.brand = scope.brands[0].brandId;
            }

            scope.$apply();

            return scope.brands
        })
    }).then(brands => {

        /*                 MODELS                     */

        fetch('http://localhost:5000/api?', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "query": allModelsQuery,
                "variables": null,
                "operationName": null,
            })
        }).then(r => {
            r.json().then(result => {
                scope.models = result.data.allCars.edges.map(a => a.node)
                scope.$apply()
            })
        })
    })

    scope.saveModelInfo = function (model) {
        let newModel = Object.assign({}, model);

        let variables = {
            "car": {
                name: newModel.name,
                carId: newModel.carId
            }
        }

        fetch('http://localhost:5000/api?', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "query": editModelMutation,
                "variables": variables,
            })
        }).then(r => {
            r.json().then(result => {
                if ('data' in result) {
                    scope.$apply()
                    toastr.success('The model was successfully updated.')
                } else if ('errors' in result) {
                    toastr.error('The model was not updated. Errors: ' + result.errors.map(a => a.message).join('\n'))
                }
            })
        })
    }

    scope.createModel = function () {
        let model = Object.assign({}, scope.newModel);

        let variables = {
            "car": {
                "name": model.name,
                "brand": model.brand,
            }
        }

        fetch('http://localhost:5000/api?', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "query": createModelMutation,
                "variables": variables,
            })
        }).then(r => {
            r.json().then(result => {
                if ('data' in result) {
                    if (!model.carId) {
                        model.carId = result.data.createModel.car.carId
                    }

                    model.brand = result.data.createModel.car.brand

                    scope.models.push(model)
                    scope.$apply()
                    toastr.success('The model was successfully added.')
                } else if ('errors' in result) {
                    toastr.error('The model was not added. Errors: ' + result.errors.map(a => a.message).join('\n'))
                }
            })
        })

        scope.resetModel();
    }


    scope.resetModel = function(){
        scope.newModel = {}
        if (scope.brands.length) {
            scope.newModel.brand = scope.brands[0].brandId;
        }
    };

    scope.deleteModel = function (model) {

        setTimeout(function () {

            let modelToDelete = Object.assign({}, model);

            let variables = {
                "car": {
                    "carId": modelToDelete.carId,
                }
            }

            fetch('http://localhost:5000/api?', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "query": deleteModelMutation,
                    "variables": variables,
                })
            }).then(r => {
                r.json().then(result => {
                    if ('data' in result) {

                        toastr.success('The model was successfully deleted.')

                        let modelIndex = scope.models.findIndex(a => a.id == modelToDelete.id);
                        scope.models.splice(modelIndex, 1);

                        scope.$apply()
                    } else if ('errors' in result) {
                        toastr.error('The model was not deleted. Errors: ' + result.errors.map(a => a.message).join('\n'))
                    }
                })
            })

        }, 500);

    };


}])