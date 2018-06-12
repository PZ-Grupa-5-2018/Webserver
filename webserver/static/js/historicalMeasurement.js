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
                createCSVData(data);
            })
        });
    }
}

var csv;

$(function() {
    $("#historical_chart").hide();
    var isoStr = new Date().toISOString();
    $('.chosen_datetime').val(isoStr.substring(0,isoStr.length-1));
});

function createCSVData(objArray) {
    var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    csv = '';
    for (var i = 0; i < array.length; i++) {
        var output = '';
        for (var index in array[i]) {
            if(index == 'key')
                output += 'Timestamp ,' + array[i][index] + '\n';
            else
                for(measurment in array[i][index])
                    output += array[i][index][measurment].x +  ',' + array[i][index][measurment].y + '\n';
         }
        csv += output + '\r\n';
    }
}
function downloadCSV(args) {
        var data, filename, link;
        if (csv == null){
           alert("The data has not been selected");
           return;
        }
        filename = args.filename || 'export.csv';

        if (!csv.match(/^data:text\/csv/i)) {
            csv = 'data:text/csv;charset=utf-8,' + csv;
        }
        data = encodeURI(csv);

        link = document.createElement('a');
        link.setAttribute('href', data);
        link.setAttribute('download', filename);
        link.click();
}
