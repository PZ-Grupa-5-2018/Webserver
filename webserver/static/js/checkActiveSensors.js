var interval_refresh_last_measurements = window.setInterval('check_active_sensors()', 5000); // 5 seconds

var last_data_from_monitor=0

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    ymd=[year, month, day].join('-');
    ymd+='T';
    ymd+=date.getHours()-2;
    ymd+=':';
    ymd+=date.getMinutes();
    ymd+=':';
    ymd+=date.getSeconds();
    ymd+='Z';
    return ymd;
}

function checkTimestamp(timestamp, date, difference_in_seconds){
    var splitted_timestamp = timestamp.split("T");
    splitted_year_month_day= splitted_timestamp[0].split("-");
    var d = new Date();
    d.setFullYear(splitted_year_month_day[0]);
    d.setMonth(splitted_year_month_day[1]-1);
    d.setDate(splitted_year_month_day[2]);
    splitted_time = splitted_timestamp[1].split("Z");
    splitted_time = splitted_time[0];
    splitted_time = splitted_time.split(":");

    d.setHours(parseInt(splitted_time[0])+2);
    d.setMinutes(splitted_time[1]);
    d.setSeconds(parseInt(splitted_time[2])+difference_in_seconds);

    if(d>date)
        return true;
    else
        return false;
}

var check_active_sensors = function() {
    $.ajax({
        type: "GET",
        url: "check_active_sensors/",
        success: function( data ) {
            var html = '';
            html += '<table class="table table-striped table-bordered">';
            html += '<thead>';
            html += '<tr>';
            html += '<th scope="col">Host name</th>';
            html += '<th scope="col">Host IP</th>';
            html += '<th scope="col">Metric Type</th>';
            html += '<th scope="col">Show</th>';
            html += '</tr>';
            html += '</thead>';
            html += '<tbody>';

            $.each(data, function(key, value){
                var today = new Date();
                if(checkTimestamp(value.measurement_timestamp, today, 60)){
                     html += '<tr>';
                     html += '<th scope="row">' + value.host_name + '</th>';
                     html += '<td>'+value.host_ip+'</td>';
                     html += '<td>'+value.metric_type+'</td>';
                     html += '<td> <a href="hosts/'+value.host_id+'/metrics/'+value.metric_id+'/">Show</a></td>';
                }
            });

            html += '</tbody>';
            html += '</table>';
            last_data_from_monitor=data;
            $('#list_of_active_sensors').html(html);

        },
        error: function(ts,resp,error) {
            console.log("not work - response: "+resp+" - error: "+error);
        }
    });
};
check_active_sensors();