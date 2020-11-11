d3.json("http://127.0.0.1:5000/api/v1.0/archvisdata", function(data) {
    let count = data.map(function(d){return d.target});

    let yticks = data.map(function(d){return d.source});
    let barPlotData = [
      {
        y: yticks,
        x: count,
        text: "jibberjabbr",
        type: "bar",
        orientation: "h",
        marker: {
            color: rainbow
          }
      }
    ];
    let barPlotLayout = {
      title: "Number of Best Sellers By Author",
      width: 1500,
      height:1200,
      margin: { t: 30, l: 150 }
    };
    Plotly.newPlot("bar", barPlotData, barPlotLayout);
});

d3.json("http://127.0.0.1:5000/api/v1.0/adelavisdata", function(error,data) {

  function tabulate(data, columns) {
		var table = d3.select('#books-table').append('table-active')
		var thead = table.append('thead')
		var	tbody = table.append('tbody');

		// append the header row
		thead.append('tr')
		  .selectAll('th')
		  .data(columns).enter()
		  .append('th')
		    .text(function (column) { return column; });

		// create a row for each object in the data
		var rows = tbody.selectAll('tr')
		  .data(data)
		  .enter()
		  .append('tr');

		// create a cell in each row for each column
		var cells = rows.selectAll('td')
		  .data(function (row) {
		    return columns.map(function (column) {
		      return {column: column, value: row[column]};
		    });
		  })
		  .enter()
		  .append('td')
		    .text(function (d) { return d.value; });

	  return table;
	}

	// render the table(s)
	tabulate(data, ['author', 'descriptions']); // 2 column table

});
let svgWidth = 1000;
let svgHeight = 500;
let margin = {
    top: 20,
    right: 40,
    bottom: 60,
    left: 100
};
let width = svgWidth - margin.left - margin.right;
let height = svgHeight - margin.top - margin.bottom;
let svg = d3.select("#scatter")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);
let scatterGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);
d3.json("http://127.0.0.1:5000/api/v1.0/adelavisscatterdata", function(scatterData) {
    // console.log(scatterData) });
// d3.json("http://127.0.0.1:5000/api/v1.0/wordcloudvisdata", function(data) {
//     let words = data;
//     console.log(words);
    // parse data/cast as numbers
    scatterData.forEach(function(data) {
        scatterData.weeks_on_list = +scatterData.weeks_on_list;
        scatterData.title = +scatterData.title;
    });
    let xLinearScale = d3.scaleLinear()
        .domain([d3.min(scatterData, d => (0.90) * d.title), d3.max(scatterData, d => (1.10 * d.title))])
        .range([0, width])
    let yLinearScale = d3.scaleLinear()
        .domain([d3.min(scatterData, d => (0.90) * d.weeks_on_list), d3.max(scatterData, d => (1.10) * d.weeks_on_list)])
        .range([height, 0])
    // create axis functions
    let bottomAxis = d3.axisBottom(xLinearScale);
    let leftAxis = d3.axisLeft(yLinearScale);
    // append Axes to the chart
    scatterGroup.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(bottomAxis);
    scatterGroup.append("g")
        .call(leftAxis);
    // create circles
    let circlesGroup = scatterGroup.selectAll("circle")
    .data(scatterData)
    .enter()
    .append("circle")
    .attr("cx", d => xLinearScale(d.title))
    .attr("cy", d => yLinearScale(d.weeks_on_list))
    .attr("r", "15")
    .attr("fill", "pink")
    .attr("opacity", ".5");
    // initialize tool tip
    let toolTip = d3.tip()
        .attr("class", "tooltip")
        .offset([80, -60])
        .html(function(d) {
            return(`Title: ${d.title}, Weeks_on_list: ${d.weeks_on_list}`);
        });
    // create tooltip in the chart
    // create event listeners to display and hide the tooltip
    circlesGroup.on("mouseover", function(data) {
        toolTip.show(data);
    })
    // onmouseout event
    .on("mouseout", function(data, index) {
        toolTip.hide(data);
    });
    // create axes labels
    scatterGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left + 40)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .attr("class", "axisText")
    .text("Lacks Healthcare(%)");
    scatterGroup.append("text")
    .attr("transform", `translate(${width / 2}, ${height + margin.top + 30})`)
    .attr("class", "axisText")
    .text("In Poverty(%)");
    scatterGroup.selectAll("null")
    .data(scatterData).enter().append("text") 
    .text(d => d.abbr)
    .attr("x", d => xLinearScale(d.title)-10)
    .attr("y", d => yLinearScale(d.weeks_on_list))
    .attr("class", "tooltiptext");
    scatterGroup.call(toolTip);
}).catch(function(error) {
    console.log(error);
});