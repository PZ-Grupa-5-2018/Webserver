function draw_historical_chart() {
    var chkArray = [];

	$(".metric_type:checked").each(function() {
		chkArray.push($(this).val());
	});

	var dateTime = $('.chosen_datetime').val();

	if(chkArray.length < 1){
		alert("Please at least check one of the metric type");
	}
	else{
	    var data = {
            'timestamp': dateTime,
            'metric_ids': chkArray
        };
        $.ajax({
            type: "POST",
            url: "historicalMeasurements/",
            data: JSON.stringify(data),
            contentType: 'application/json',
            dataType: 'json',
            success: (function (data) {
                console.log(data)
            })
        });
    }
}


$(function() {
    var isoStr = new Date().toISOString();
    $('.chosen_datetime').val(isoStr.substring(0,isoStr.length-1));
});