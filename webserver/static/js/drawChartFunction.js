var drawSingleChart =  function () {
    nv.addGraph(function() {
      var chart = nv.models.lineChart()
          .useInteractiveGuideline(false);

        chart.xAxis
            .axisLabel('Time')
            .tickFormat(function(d) {
                 return d3.time.format('%x ')(new Date(d*1000))
            });
        ;

        chart.yAxis
            .axisLabel('Usage')
            .tickFormat(d3.format('.02f'))
        ;

        d3.select("#singleChart svg")
            .datum(chart_data_measurments)
            .transition().duration(1200)
            .call(chart);

      return chart;
});
};

window.onload = function() {
    drawSingleChart();
}