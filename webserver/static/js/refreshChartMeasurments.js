var interval_refresh_last_measurements = window.setInterval('refresh_chart_measruments()', 5000); // 10 seconds

var drawChart =  function (dataChart) {
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

        d3.select("#chart svg")
            .datum(dataChart)
            .transition().duration(1200)
            .call(chart);

      return chart;
});
};

var clearChart = function () {
    var svg = d3.select("chart svg");
    svg.selectAll("*").remove();
}

var refresh_chart_measruments = function() {
    $.ajax({
        type: "GET",
        url: "refresh_chart_measurements/",
        success: function( chart_data_measurments ) {
            clearChart();
            drawChart(chart_data_measurments);
        },
        error: function(ts,resp,error) {
            console.log("not work - response: "+resp+" - error: "+error);
        }
    });
};

refresh_chart_measruments();

function startRefresh() {
    interval_refresh_last_measurements = window.setInterval('refresh_chart_measruments()', 5000);
    refresh_chart_measruments();
    document.getElementById("startRefresh").disabled = true;
    document.getElementById("stopRefresh").disabled = false;
}
function stopRefresh(){
    clearInterval(interval_refresh_last_measurements);
    document.getElementById("startRefresh").disabled = false;
    document.getElementById("stopRefresh").disabled = true;
}


