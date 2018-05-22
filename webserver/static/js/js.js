
$(document).ready(function(){
    $.ajax({
        url: "https://pz-monitor-2.herokuapp.com/hosts/1/",
        success: function( data ) {
            console.log("work");
        },
        error: function(ts,resp,error) {
            console.log("not work - response: "+resp+" error: "+error);
        }
    }).then(function(data) {
       $('#test_id').append(data.id);
       $('#test_name').append(data.name);
    });
});

/*
var proxy_url_tmp = "https://pz-webserver.herokuapp.com/";

$.ajax({
   type: "GET",
   dataType: "json",
   url: proxy_url_tmp + "https://pz-monitor-2.herokuapp.com/hosts/1/",
   success: function(data){
   alert("work");
   },
   error: function(a,b,c){
   alert("not work");
   }
});
*/
