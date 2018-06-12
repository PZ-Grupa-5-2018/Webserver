var historical_chart =  function (dataChart) {
    nv.addGraph(function() {
        d3.selectAll('.nvtooltip').remove();
      var chart = nv.models.lineChart()
          .useInteractiveGuideline(false)
      ;
        chart.xAxis
            .axisLabel('Time')
            .tickFormat(function(d) {
                 return d3.time.format('%X')(new Date(d*1000))
            });

        chart.yAxis
            .axisLabel('Usage')
            .tickFormat(d3.format('.02f'))
        ;

        d3.select("#historical_chart svg")
            .datum(dataChart)
            .transition().duration(1200)
            .call(chart);

      return chart;
});
};

function draw_historical_chart() {
    var chkArray = [];

	$(".metric_type:checked").each(function() {
		chkArray.push($(this).val());
	});

	var dateTime = $('.chosen_datetime').val();

	if(chkArray.length < 1 ){
		alert("Please at least check one of the metric type");
	}
	else if (dateTime < 1){
        alert("Please select the date time");
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
                $("#historical_chart").show();
                historical_chart(data);
            })
        });
    }
}


$(function() {
    $("#historical_chart").hide();
    var isoStr = new Date().toISOString();
    $('.chosen_datetime').val(isoStr.substring(0,isoStr.length-1));
});

