createRadar = function(playerName, colors, data, maxValue) {
  var w = 500,
    h = 500;

  var colors = JSON.parse(colors);
  var data = JSON.parse(data);
  var maxValue = JSON.parse(maxValue);

  //Legend titles
  var LegendOptions = [playerName];

  //Data
  var d = [
    data
    // [
    //   { axis: "Home Runs", value: 20 },
    //   { axis: "RBIs", value: 35 },
    //   { axis: "Runs", value: 35 },
    //   { axis: "OBP", value: 0.34 },
    //   { axis: "SLG", value: 0.75 }
    // ]
    // , [
    //   { axis: "Home Runs", value: 15 },
    //   { axis: "RBIs", value: 45 },
    //   { axis: "Runs", value: 50 },
    //   { axis: "OBP", value: 0.30 },
    //   { axis: "SLG", value: 0.6 }
    // ]
  ];

  //Options for the Radar chart, other than default
  var mycfg = {
    w: w,
    h: h,
    maxValue: maxValue,
    levels: 6,
    ExtraWidthX: 300,
    color: colors
  }

  //Call function to draw the Radar chart
  //Will expect that data is in %'s
  var svg = RadarChart.draw("#chart", d, mycfg);

  ////////////////////////////////////////////
  /////////// Initiate legend ////////////////
  ////////////////////////////////////////////

  //Create the title for the legend
  var text = svg.append("text")
    .attr("class", "title")
    .attr('transform', 'translate(90,0)')
    .attr("x", w - 70)
    .attr("y", 10)
    .attr("font-size", "12px")
    .attr("fill", "#404040")
    .text("Player Statistics");

  //Initiate Legend	
  var legend = svg.append("g")
    .attr("class", "legend")
    .attr("height", 100)
    .attr("width", 200)
    .attr('transform', 'translate(90,20)');

  //Create colour squares
  legend.selectAll('rect')
    .data(LegendOptions)
    .enter()
    .append("rect")
    .attr("x", w - 65)
    .attr("y", function (d, i) { return i * 20; })
    .attr("width", 10)
    .attr("height", 10)
    .style("fill", function (d, i) { return colors[i]; });

  //Create text next to squares
  legend.selectAll('text')
    .data(LegendOptions)
    .enter()
    .append("text")
    .attr("x", w - 52)
    .attr("y", function (d, i) { return i * 20 + 9; })
    .attr("font-size", "11px")
    .attr("fill", "#737373")
    .text(function (d) { return d; });
}
