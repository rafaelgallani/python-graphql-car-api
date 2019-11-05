allMarksQuery = (
    `
    {
        allMarks {
            edges {
                node {
                    id,
                    country,
                    markId,
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
                    mark {
                        country,
                        name,
                        id,
                        markId
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
                mark {
                    name,
                    country,
                    markId
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
                mark {
                    name,
                    country,
                    markId
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
                mark {
                    name,
                    country,
                    markId
                }
            }
        }
    }
    `;

var app = angular.module('app', []);
app.controller('ModelController', ['$scope', function(scope){
    
    scope.newModel = {};
    scope.marks = [];
    scope.models = [];

    /*                  MARKS                              */

    fetch('http://localhost:5000/api?', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "query": allMarksQuery,
            "variables": null,
            "operationName": null,
        })
    }).then(r => {
        return r.json().then(result => {
            scope.marks = result.data.allMarks.edges.map(a => a.node)

            if (scope.marks.length){
                scope.newModel.mark = scope.marks[0].markId;
            }

            scope.$apply();

            return scope.marks
        })
    }).then(marks => {

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
                "mark": model.mark,
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

                    model.mark = result.data.createModel.car.mark

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
        if (scope.marks.length) {
            scope.newModel.mark = scope.marks[0].markId;
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