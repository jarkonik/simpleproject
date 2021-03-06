

var rows = []
var formatdate = d3.time.format("%b %d %Y");

d3.csv("static/dortmund.csv", function(error, csv) {
  csv.forEach(function(row) {
    row.mu = parseFloat(row.mu).toFixed(1);
    row.sigma = parseFloat(row.sigma).toFixed(1);
    row.dt = formatdate(new Date(Date.parse(row.date)));

    var res = parseFloat(row.result);
    if (res < .5) {
      row.result = "loss";
    } else if (res > .5) {
      row.result = "win";
    } else {
      row.result = "draw";
    }
    
    rows.push(row);
  });

  var table = d3.select("#datatable").append("table");
      thead = table.append("thead");
      tbody = table.append("tbody");

  thead.append("th").text("Date");
  thead.append("th").text("Opponent");
  thead.append("th").text("Result");
  thead.append("th").text("Rating");
  thead.append("th").text("");

  var tr = tbody.selectAll("tr")
      .data(rows)
      .enter().append("tr");

  var td = tr.selectAll("td")
        .data(function(d) { return [d.dt, d.opp, d.result, d.mu]; })
      .enter().append("td")
        .text(function(d) { return d; });

  var width = 80,
      height = d3.select("table")[0][0].clientHeight,
      mx = 10,
      radius = 2;

  // Now add the chart column
  d3.select("#datatable tbody tr").append("td")
    .attr("id", "chart")
    .attr("width", width + "px")
    .attr("rowspan", rows.length);

  var chart = d3.select("#chart").append("svg")
      .attr("class", "chart")
      .attr("width", width)
      .attr("height", height);

  var maxMu = 0;
  var minMu = Number.MAX_VALUE;
  for (i=0; i < rows.length; i++) {
    if (rows[i].mu > maxMu) { maxMu = rows[i].mu; }
    if (rows[i].mu < minMu) { minMu = rows[i].mu; }
  }

  var dates = rows.map(function(t) { return t.dt; });

  var xscale = d3.scale.linear()
    .domain([minMu, maxMu])
    .range([mx, width-mx])
    .nice();

  var yscale = d3.scale.ordinal()
    .domain(dates)
    .rangeBands([0, height]);

  chart.selectAll(".xaxislabel")
      .data(xscale.ticks(2))
    .enter().append("text")
      .attr("class", "xaxislabel")
      .attr("x", function(d) { return xscale(d); })
      .attr("y", 10)
      .attr("text-anchor", "middle")
      .text(String)

  chart.selectAll(".xaxistick")
      .data(xscale.ticks(2))
    .enter().append("line")
      .attr("x1", function(d) { return xscale(d); })
      .attr("x2", function(d) { return xscale(d); })
      .attr("y1", 10)
      .attr("y2", height)
      .attr("stroke", "#eee")
      .attr("stroke-width", 1);

  chart.selectAll(".line")
      .data(rows)
    .enter().append("line")
      .attr("x1", function(d) { return xscale(d.mu); })
      .attr("y1", function(d) { return yscale(d.dt) + yscale.rangeBand()/2; })
      .attr("x2", function(d,i) { return rows[i+1] ? xscale(rows[i+1].mu) : xscale(d.mu); })
      .attr("y2", function(d,i) { return rows[i+1] ? yscale(rows[i+1].dt) + yscale.rangeBand()/2 : yscale(d.dt) + yscale.rangeBand()/2; })
      .attr("stroke", "#777")
      .attr("stroke-width", 1);

  var pt = chart.selectAll(".pt")
      .data(rows)
    .enter().append("g")
      .attr("class", "pt")
      .attr("transform", function(d) { return "translate(" + xscale(d.mu) + "," + (yscale(d.dt) + yscale.rangeBand()/2) + ")"; });

  pt.append("circle")
      .attr("cx", 0)
      .attr("cy", 0)
      .attr("r", radius)
      .attr("opacity", .5)
      .attr("fill", "#ff0000");

});
