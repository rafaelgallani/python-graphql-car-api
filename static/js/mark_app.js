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

(async function(){
    resp = await fetch('http://localhost:5000/api?', {
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
    })

    cars = await resp.json()

    function editMark(markId){
        
    }

    return {

    }
})()