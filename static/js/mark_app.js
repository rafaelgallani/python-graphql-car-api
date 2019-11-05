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
                name                 
            }                        
        }                            
    }`
);

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
        
    }

    scope.deleteMark = function(mark){

        setTimeout(function(){
            let markIndex = scope.marks.findIndex(a => a.id == mark.id);
            scope.marks.splice(markIndex, 1);
            scope.$apply()

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