var rows;
var dataArray = [];
var dateParser = d3.time.format("%Y").parse;

var w = 800;
var h = 450;

var x;
var y;

var yIndexScale;

var xAxisMetric;
var yAxisMetric;

var internetLine;
var indexLine;

//var xAxisIndex;
var yAxisIndex;

var chartMargin = {
	top: 58,
	bottom: 100,
	left: 80,
	right: 40
};

var width = w - chartMargin.left - chartMargin.right;
var height = h - chartMargin.top - chartMargin.bottom;

function request(country, metric, index){
	
	//console.log("http://localhost:8080/country?country="+country+"&year_from=1998&year_to=2015&metric="+metric+"&human_index="+index);
	
	
	var ajaxRequest = new XMLHttpRequest();
	ajaxRequest.open("GET", "http://localhost:8080/country?country="+country+"&year_from=1998&year_to=2015&metric="+metric+"&human_index="+index)
	ajaxRequest.onload = function(){
		rows = JSON.parse(ajaxRequest.responseText);
	}
	ajaxRequest.send();
	
	transformInArray();

	if(dataArray.length != 0){
		createChart();
	}
	
	console.log(dataArray);
	
}

function transformInArray(){

	for(year in rows){
		dataArray.push({
			year: year,
			internet: rows[year][0],
			human: rows[year][1]
		});
	}
}

function createChart(){
	
	var svg = d3.select("body").append("svg")
				.attr("id", "chart")
				.attr("width", w)
				.attr("height", h);

	var chart = svg.append("g")
					.classed("display", true)
					.attr("transform", "translate(" + chartMargin.left + "," + chartMargin.top + ")");

	
	var max = d3.max(dataArray, function(measurement){
		return measurement.internet;
	});

	y = d3.scale.linear()
			.domain([0, d3.max(dataArray, function(measurement){
							return measurement.internet;
	})])
	.range([height,0]);

	x = d3.time.scale() 
				.domain(d3.extent(dataArray, function(row){
					var date = dateParser(row.year);
					return date;
				}))
				.range([0, width]);

	yIndexScale = d3.scale.linear()
				.domain([d3.min(dataArray, function(measurement){
					return measurement.human;
				}), d3.max(dataArray, function(measurement){
					return measurement.human;
				})])
				.range([height, 0]);

	xAxisMetric = d3.svg.axis()
			  .scale(x)
			  .orient("bottom");

	yAxisMetric = d3.svg.axis()
		      .scale(y)
		      .orient("left");

    
	yAxisIndex = d3.svg.axis()
					.scale(yIndexScale)
					.orient("right");
	

	internetLine = d3.svg.line()
					 .x(function(row){
					 	var date = dateParser(row.year);
					 	return x(date);
					 })
					 .y(function(row){
					 	return y(row.internet);
					 });

	indexLine = d3.svg.line()
					 .x(function(row){
					 	var date = dateParser(row.year);
					 	return x(date);
					 })
					 .y(function(row){
					 	return yIndexScale(row.human);
					 });



		plot.call(chart, {
		data: dataArray,
		axis:{
			xAxisMetric: xAxisMetric,
			yAxisMetric: yAxisMetric,
			yAxisIndex: yAxisIndex
		}
	});


	dataArray = [];

}


function plot(params){

	//console.log("PARAMS", params.data);
	this.append("g")
		.classed("x axis", true)
		.attr("transform", "translate(0, " + height +")")
		.call(params.axis.xAxisMetric);
		
	this.append("g")
		.classed("y axis", true)
		.attr("transform", "translate(0, 0)")
		.call(params.axis.yAxisMetric);

	
	//human index
	this.append("g")
		.classed("y axis", true)
		.attr("transform", "translate("+width+", 0)")
		.call(params.axis.yAxisIndex);
	

	this.selectAll("trendline")
		.data([params.data])
		.enter()
		.append("path")	
		.classed("trendline", true);

		//human
	this.selectAll("trendlineIndex")
		.data([params.data])
		.enter()
		.append("path")	
		.classed("trendlineIndex", true);
	
	this.selectAll(".point")
		.data(params.data)
		.enter()
		.append("circle")
		.classed("point", true)
		.attr("r", 2);

	this.selectAll(".trendline")
		.attr("d", function(row){
			return internetLine(row);
		});

		//human index
	this.selectAll(".trendlineIndex")
		.attr("d", function(row){
			return indexLine(row);
		});


	this.selectAll(".point")
		.attr("cx", function(d){
			var date = dateParser(d.year);
			return x(date);
		})
		.attr("cy", function(d){
			return y(d.internet);
		});

		//human index
	this.selectAll(".point")
		.attr("cx", function(row){
			var date = dateParser(row.year);
			return x(date);
		})
		.attr("cy", function(row){
			console.log(row.human);
			return yIndexScale(row.human);
		});
	

	this.selectAll(".trendline")
		.data([params.data])
		.exit()
		.remove();

	this.selectAll(".trendlineIndex")
		.data([params.data])
		.exit()
		.remove();


	this.selectAll(".point")
		.data(params.data)
		.exit()
		.remove();

	
}
