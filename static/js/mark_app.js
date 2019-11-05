allMarksQuery = (
    '{                        ' +
        'allMarks {           ' +
            'edges {          ' +
                'node {       ' +
                    'id,      ' +
                    'country, ' +
                    'markId,  ' +
                    'name     ' +
                '}            ' +
            '}                ' +
        '}                    ' +
    '}                        '.trim()
);

createMarkMutation = (
    `mutation($mark: CarMarkInput) { 
        createMark(mark: $mark) {    
            mark {                   
                country,            
                markId, 
                name                 
            }                        
        }                            
    }`
);

deleteMarkMutation = (
    `mutation($mark: CarMarkInput) { 
        deleteMark(mark: $mark) {    
            mark {                   
                country,           
                markId,  
                name                 
            }                        
        }                            
    }`
);

editMarkMutation = `
    mutation ($mark: CarMarkInput){
        editMark(mark: $mark){
            mark{
                country, name, markId
            }
        }
    }`;

var app = angular.module('app', []);
app.controller('BrandController', ['$scope', function(scope){
    
    scope.newMark = {};
    
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
        r.json().then(result => {
            scope.marks = result.data.allMarks.edges.map(a => a.node)
            scope.$apply();
        })
    })


    scope.saveMarkInfo = function(mark){
        let newMark = Object.assign({}, mark);

        let variables = {
            "mark": {
                name: newMark.name, 
                country: newMark.country,
                markId: newMark.markId
            }
        }

        fetch('http://localhost:5000/api?', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "query": editMarkMutation,
                "variables": variables,
            })
        }).then(r => {
            r.json().then(result => {
                if ('data' in result) {
                    scope.$apply()
                    toastr.success('The mark was successfully updated.')
                } else if ('errors' in result) {
                    toastr.error('The mark was not updated. Errors: ' + result.errors.map(a => a.message).join('\n'))
                }
            })
        })

        scope.newMark = {}
    }

    scope.deleteMark = function(mark){

        setTimeout(function(){

            let markToDelete = Object.assign({}, mark);

            let variables = {
                "mark": {
                    "country": markToDelete.country,
                    "name": markToDelete.name,
                    "markId": markToDelete.markId,
                }
            }

            fetch('http://localhost:5000/api?', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "query": deleteMarkMutation,
                    "variables": variables,
                })
            }).then(r => {
                r.json().then(result => {
                    if ('data' in result) {
                        
                        toastr.success('The mark was successfully deleted.')

                        let markIndex = scope.marks.findIndex(a => a.id == markToDelete.id);
                        scope.marks.splice(markIndex, 1);
                        
                        scope.$apply()
                    } else if ('errors' in result) {
                        toastr.error('The mark was not deleted. Errors: ' + result.errors.map(a => a.message).join('\n'))
                    }
                })
            })

        }, 500);

    };

    scope.createMark = function(){
        let mark = Object.assign({}, scope.newMark);

        let variables = {
            "mark": {
                "country": mark.country,
                "name": mark.name,
            }
        }

        fetch('http://localhost:5000/api?', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "query": createMarkMutation,
                "variables": variables,
            })
        }).then(r => {
            r.json().then(result => {
                if ('data' in result){
                    scope.marks.push(mark)
                    scope.$apply()
                    toastr.success('The mark was successfully added.')
                } else if ('errors' in result){
                    toastr.error('The mark was not added. Errors: ' + result.errors.map(a => a.message).join('\n'))
                }
            })
        })

        scope.newMark = {}

    }
}])