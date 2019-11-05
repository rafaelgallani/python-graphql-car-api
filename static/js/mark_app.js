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

    marks = await resp.json()
    marks = marks.data.allMarks.edges.map(a => a.node)

    marksHtml = marks.map(mark => {
        return `
            <tr>
                <td>
                    <span class="custom-checkbox">
                        <input type="checkbox" id="checkbox5" name="options[]" value="1">
                        <label for="checkbox5"></label>
                    </span>
                </td>
                <td>${mark.name}</td>
                <td>${mark.country}</td>
                <td>
                    <a href="#editEmployeeModal" class="edit" data-toggle="modal"><i class="material-icons"
                            data-toggle="tooltip" title="Edit">&#xE254;</i></a>
                    <a href="#deleteEmployeeModal" class="delete" data-toggle="modal"><i class="material-icons"
                            data-toggle="tooltip" title="Delete">&#xE872;</i></a>
                </td>
            </tr>
        `
    }).join('\n')


    $('#marks-table').html(marksHtml)

    // Activate tooltip
    $('[data-toggle="tooltip"]').tooltip();

    // Select/Deselect checkboxes
    var checkbox = $('table tbody input[type="checkbox"]');
    $("#selectAll").click(function () {
        if (this.checked) {
            checkbox.each(function () {
                this.checked = true;
            });
        } else {
            checkbox.each(function () {
                this.checked = false;
            });
        }
    });
    checkbox.click(function () {
        if (!this.checked) {
            $("#selectAll").prop("checked", false);
        }
    });

    return {

    }
})()