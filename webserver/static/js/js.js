var connected_monitors_hosts={};

function updateHostList(){
    var html = '';
    html+='<table id="host_datatable" class="table table-striped table-bordered">';
    html+='<thead>';
    html+='<tr>';
    html+='<th scope="col">Monitor URL</th>';
    html+='<th scope="col">Host IP</th>';
    html+='<th scope="col">Host Mac</th>';
    html+='<th scope="col">Host Name</th>';
    html+='<th scope="col">Host CPU</th>';
    html+='<th scope="col">Host Memory</th>';
    html+='<th scope="col">Details</th>';
    html+='</tr>';
    html+='</thead>';
    html+='<tbody>';
    $.each(connected_monitors_hosts, function(monitor_key, monitor_value){
        $.each(monitor_value.hosts, function(key, value){
            html += '<tr>';
            html += '<th scope="row">'+monitor_value.monitor_url+'</th>';
            html += '<td>'+value.ip+'</td>';
            html += '<td>'+value.mac+'</td>';
            html += '<td>'+value.name+'</td>';
            html += '<td>'+value.cpu+'</td>';
            html += '<td>'+value.memory+'</td>';
            html += '<td> <a href="'+monitor_key+'/hosts/'+value.id+'/">Show</a></td>';
            html += '</tr>';
        });
    });
    html+='</tbody></table>';
    $('#connected_monitors_host_list_box').html(html);
}

function getMonitorHosts(monitor_id){
    $.ajax({
        type: "GET",
        url: monitor_id+"/get_monitor_hosts/",
        success: function( data ) {
            connected_monitors_hosts[monitor_id]=data;
            updateHostList();
        },
        error: function(ts,resp,error) {
            console.log("not work - response: "+resp+" - error: "+error);
        }
    });

}

function removeMonitorHosts(monitor_id){
    delete connected_monitors_hosts[monitor_id];
    updateHostList();
}

function connectToMonitor(monitor_id){
    getMonitorHosts(monitor_id);
    var html = '';
    html += '<div class="disconnect_from_monitor">';
    html += '<div class="connection_to_monitor_status">Connected</div>';
    html += '<div class="disconnection_from_monitor_button">';
    html += '<button type="button" class="btn btn-outline-danger" onclick="disconnectFromMonitor('+monitor_id+');">Disconnect</button>';
    html += '</div>';
    html += '</div>';
    $('#monitor_connection_box_'+monitor_id).html(html);
}

function disconnectFromMonitor(monitor_id){
    removeMonitorHosts(monitor_id);
    var html = '';
    html += '<div class="connect_to_monitor">';
    html += '<div class="connection_to_monitor_status">Disconnected</div>';
    html += '<div class="connection_to_monitor_button">';
    html += '<button type="button" class="btn btn-outline-success" onclick="connectToMonitor('+monitor_id+');">Connect</button>';
    html += '</div>';
    html += '</div>';
    $('#monitor_connection_box_'+monitor_id).html(html);
}

var interval_refresh_last_measurements = window.setInterval('update_last_20_measurements_from_all_monitors()', 10000); // 10 seconds
//monitor_list=monitor_id1&monitor_id2&monitor_id3...
function get_last_20_measurements_from_all_monitors(monitor_list) {
    $.ajax({
        type: "GET",
        url: monitor_list+"/get_last_measurements_from_monitor_list/",
        success: function( data ) {
            var html = '';
            html += '<table class="table table-striped table-bordered">';
            html += '<thead>';
            html += '<tr>';
            html += '<th scope="col">ID</th>';
            html += '<th scope="col">Monitor URL</th>';
            html += '<th scope="col">Host IP</th>';
            html += '<th scope="col">Metric Type</th>';
            html += '<th scope="col">Measurement Value</th>';
            html += '<th scope="col">Timestamp</th>';
            html += '</tr>';
            html += '</thead>';
            html += '<tbody>';
            $.each(data, function(key, value){

                html += '<tr>';
                html += '<th scope="row">' + value.id + '</th>';
                html += '<th scope="row">' + value.monitor_url + '</th>';
                html += '<td>'+value.ip+'</td>';
                html += '<td>'+value.type+'</td>';
                html += '<td>'+value.value+'</td>';
                html += '<td>'+value.timestamp+'</td>';

            });
            html += '</tbody>';
            html += '</table>';
            $('#last_20_measurements_from_all_monitors_table').html(html);
        },
        error: function(ts,resp,error) {
            console.log("not work - response: "+resp+" - error: "+error);
        }
    });
};

function update_last_20_measurements_from_all_monitors() {
    var monitor_list_as_string='list_';
    $.each(connected_monitors_hosts, function(monitor_key, monitor_value){
        monitor_list_as_string+=String(monitor_key)+'_';
    });
    get_last_20_measurements_from_all_monitors(monitor_list_as_string);
}

