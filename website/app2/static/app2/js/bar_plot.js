var dibujar_bar_plot = function(path)
{

      if(dibujo_plot)
      {
        return(0)
      }

      dibujo_plot = true
      var margin = {top: 20, right: 20, bottom: 30, left: 40},
          width = 960 - margin.left - margin.right,
          height = 500 - margin.top - margin.bottom - 10;

      var x0 = d3.scale.ordinal()
          .rangeRoundBands([0, width], .1);

      var x1 = d3.scale.ordinal();

      var y = d3.scale.linear()
          .range([height, 0]);

      var color = d3.scale.ordinal()
          .range(["#9EBD06","00A1DC","#DD4B39"]);

      var xAxis = d3.svg.axis()
          .scale(x0)
          .orient("bottom");

      var yAxis = d3.svg.axis()
          .scale(y)
          .orient("left")
          .tickFormat(d3.format(".2s"));

      var svg_plot = d3.select("#par_plot_chart").append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var globalData = [];
      var countType = undefined;

      d3.csv(path, function(error, data) {

        if (error) throw error;
        var sortType = 'Propio'

        countType = d3.keys(data[0]).filter(function(key) { return key !== "Measure"; });
        data.forEach(function(d) {
          d.counts = countType.map(function(name) { return {name: name, value: +d[name]}; });
        })
        globalData = data.slice();
        data = data.sort(function(a, b){
          return +b[sortType] - +a[sortType];
        })

        x0.domain(data.map(function(d) { return d.Measure; }));
        x1.domain(countType).rangeRoundBands([0, x0.rangeBand()]);
        y.domain([0, d3.max(data, function(d) { return d3.max(d.counts, function(d) { return d.value; }); })]);

        svg_plot.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg_plot.append("g")
            .attr("class", "y axis")
            .call(yAxis)
          .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Porcentaje (%)");

        var Measure = svg_plot.selectAll(".Measure")
            .data(data)
          .enter().append("g")
            .attr("class", "g Measure")
            .attr("transform", function(d) { return "translate(" + x0(d.Measure) + ",0)"; });

        Measure.selectAll("rect")
            .data(function(d) { return d.counts; })
          .enter().append("rect")
            .attr("width", x1.rangeBand())
            .attr("height", 0)
            .attr("x", function(d) { return x1(d.name); })
            .attr("y", function(d) { return y(0); })
            .style("fill", function(d) { return color(d.name); })
            .style("opacity", function(d) {
              if (d.name === sortType) return 1;
              return 0.15;
            })
            .transition().duration(1000)
            .attr("height", function(d) { return height - y(d.value); })
            .attr("y", function(d) { return y(d.value); })

        var legend = svg_plot.selectAll(".legend")
            .data(countType.slice().reverse())
          .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

        legend.append("rect")
            .attr("x", width - 18)
            .attr("width", 18)
            .attr("height", 18)
            .style("fill", color);

        legend.append("text")
            .attr("x", width - 24)
            .attr("y", 9)
            .attr("dy", ".30em")
            .style("text-anchor", "end")
            .text(function(d) { return d; });

      });

      d3.selectAll("input").on("change", change);

      function change() {
        sortType = this.value
        if(sortType == 'Propio' || sortType == 'Otro')
        {
          transitionData(sortType);
        }
      }

      function transitionData(sortType){
        var data = globalData.slice().sort(function(a, b){
          return +b[sortType] - +a[sortType];
        })

        x0.domain(data.map(function(d) { return d.Measure; }));
        x1.domain(countType).rangeRoundBands([0, x0.rangeBand()]);

        var Measure = d3.selectAll(".Measure")

        Measure.transition().delay(800)
            .duration(function(d, i){ return 300 * i + 300; })
            .attr("transform", function(d) { return "translate(" + x0(d.Measure) + ",0)"; });

        Measure.selectAll("rect")
            .transition()
            .duration(800)
            .style("opacity", function(d) {
              if (d.name === sortType) return 1;
              return 0.15;
            })

        xAxis.scale(x0);
        d3.selectAll(".x.axis").transition().delay(1000)
            .duration(data.length * 100).call(xAxis)
      }
}
