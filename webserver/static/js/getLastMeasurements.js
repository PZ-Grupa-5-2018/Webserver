var interval_refresh_last_measurements = window.setInterval('update_last_20_measurements()', 5000); // 5 seconds

var update_last_20_measurements = function() {
    $.ajax({
        type: "GET",
        url: "get_last_measurements/",
        success: function( data ) {
            var html = '';
            html += '<table class="table table-striped table-bordered">';
            html += '<thead>';
            html += '<tr>';
            html += '<th scope="col">ID</th>';
            html += '<th scope="col">IP</th>';
            html += '<th scope="col">Type</th>';
            html += '<th scope="col">Value</th>';
            html += '<th scope="col">Timestamp</th>';
            html += '</tr>';
            html += '</thead>';
            html += '<tbody>';
            $.each(data, function(key, value){

                html += '<tr>';
                html += '<th scope="row">' + value.id + '</th>';
                html += '<td>'+value.ip+'</td>';
                html += '<td>'+value.type+'</td>';
                html += '<td>'+value.value+'</td>';
                html += '<td>'+value.timestamp+'</td>';

            });
            html += '</tbody>';
            html += '</table>';
            $('#last_20_measurements_table').html(html);
        },
        error: function(ts,resp,error) {
            console.log("not work - response: "+resp+" - error: "+error);
        }
    });
};
update_last_20_measurements();