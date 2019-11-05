allBrandsQuery = (
    '{                        ' +
        'allBrands {           ' +
            'edges {          ' +
                'node {       ' +
                    'id,      ' +
                    'country, ' +
                    'brandId,  ' +
                    'name     ' +
                '}            ' +
            '}                ' +
        '}                    ' +
    '}                        '.trim()
);

createBrandMutation = (
    `mutation($brand: CarBrandInput) { 
        createBrand(brand: $brand) {    
            brand {                   
                country,            
                brandId, 
                name                 
            }                        
        }                            
    }`
);

deleteBrandMutation = (
    `mutation($brand: CarBrandInput) { 
        deleteBrand(brand: $brand) {    
            brand {                   
                country,           
                brandId,  
                name                 
            }                        
        }                            
    }`
);

editBrandMutation = `
    mutation ($brand: CarBrandInput){
        editBrand(brand: $brand){
            brand{
                country, name, brandId
            }
        }
    }`;

var app = angular.module('app', []);
app.controller('BrandController', ['$scope', function(scope){
    
    scope.newBrand = {};
    
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
        r.json().then(result => {
            scope.brands = result.data.allBrands.edges.map(a => a.node)
            scope.$apply();
        })
    })


    scope.saveBrandInfo = function(brand){
        let newBrand = Object.assign({}, brand);

        let variables = {
            "brand": {
                name: newBrand.name, 
                country: newBrand.country,
                brandId: newBrand.brandId
            }
        }

        fetch('http://localhost:5000/api?', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "query": editBrandMutation,
                "variables": variables,
            })
        }).then(r => {
            r.json().then(result => {
                if ('data' in result) {
                    scope.$apply()
                    toastr.success('The brand was successfully updated.')
                } else if ('errors' in result) {
                    toastr.error('The brand was not updated. Errors: ' + result.errors.map(a => a.message).join('\n'))
                }
            })
        })

        scope.newBrand = {}
    }

    scope.deleteBrand = function(brand){

        setTimeout(function(){

            let brandToDelete = Object.assign({}, brand);

            let variables = {
                "brand": {
                    "country": brandToDelete.country,
                    "name": brandToDelete.name,
                    "brandId": brandToDelete.brandId,
                }
            }

            fetch('http://localhost:5000/api?', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "query": deleteBrandMutation,
                    "variables": variables,
                })
            }).then(r => {
                r.json().then(result => {
                    if ('data' in result) {
                        
                        toastr.success('The brand was successfully deleted.')

                        let brandIndex = scope.brands.findIndex(a => a.id == brandToDelete.id);
                        scope.brands.splice(brandIndex, 1);
                        
                        scope.$apply()
                    } else if ('errors' in result) {
                        toastr.error('The brand was not deleted. Errors: ' + result.errors.map(a => a.message).join('\n'))
                    }
                })
            })

        }, 500);

    };

    scope.createBrand = function(){
        let brand = Object.assign({}, scope.newBrand);

        let variables = {
            "brand": {
                "country": brand.country,
                "name": brand.name,
            }
        }

        fetch('http://localhost:5000/api?', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "query": createBrandMutation,
                "variables": variables,
            })
        }).then(r => {
            r.json().then(result => {
                if ('data' in result){
                    if (!brand.brandId){
                        brand.brandId = result.data.createBrand.brand.brandId
                    }
                    scope.brands.push(brand)
                    scope.$apply()
                    toastr.success('The brand was successfully added.')
                } else if ('errors' in result){
                    toastr.error('The brand was not added. Errors: ' + result.errors.map(a => a.message).join('\n'))
                }
            })
        })

        scope.newBrand = {}

    }
}])