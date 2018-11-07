

var dibujar_polaridad = function(path)
{
    if(dibujo_polaridad)
    {
      return(0)
    }
    dibujo_polaridad = true


      d3.json(path, function(error, data) {
          var words = data

          console.log(error)

          var words_frequency = [];

          Object.keys(words).forEach(function(word_lemma){
              o = words[word_lemma];
              o.lemma = word_lemma;
              words_frequency.push(o);
          });

          words_frequency.sort(function(a,b){
              return b.count - a.count;
          });

          var max = d3.max(Object.keys(words), function(k){
              return words[k].count;
          });

          console.log(max);

          var font_size = d3.scale.linear()
              .domain([1, max])
              .range([10,100]);

          /*var color = d3.scale.linear()
              .domain([-max, 0, max])
              .range([d3.hcl(36, 65, 50), d3.hcl(95, 65, 80), d3.hcl(150, 65, 50)])
              .interpolate(d3.interpolateHcl);*/

          var color = d3.scale.quantize()
              .domain([-1,0, 1])
              .range([d3.hcl(36, 65, 50),d3.hcl(0, 0, 60), d3.hcl(150, 65, 50)]);



                d3.layout.cloud().size([960, 500])
                    .words(words_frequency)
                    .rotate(function() { return ~~(Math.random() * 2) * 90; })
                    .font("Impact")
                    .spiral('rectangular')
                    .text(function(d){ return d.lemma; })
                    .fontSize(function(d){ return font_size(d.count); })
                    .on("end", draw)
                    .start();

                function draw(words) {
                    var svg = d3.select("#nube_polaridad").append("svg")
                        .attr("width", 960)
                        .attr("height", 500);


                    // append a group for zoomable content
                    var zoom_group = svg.append('g');

                    // define a zoom behavior
                    var zoom = d3.behavior.zoom()
                        .scaleExtent([1,4]) // min-max zoom
                        .on('zoom', function() {
                          // whenever the user zooms,
                          // modify translation and scale of the zoom group accordingly
                          zoom_group.attr('transform', 'translate('+zoom.translate()+')scale('+zoom.scale()+')');
                        });

                    // bind the zoom behavior to the main SVG
                    svg.call(zoom);


                    zoom_group.append("g")
                        .attr("transform", "translate(480,250)")
                        .selectAll("text")
                        .data(words)
                      .enter().append("text")
                        .style("font-size", function(d){ return font_size(d.count) + "px"; })
                        .style("font-family", "Impact")
                        .style("fill", function(d) { return color(d.polarity); })
                        .attr("text-anchor", "middle")
                        .attr("transform", function(d) {
                            var far = 1500*(Math.random() > 0.5 ? +1 : -1);
                            if(d.rotate === 0)
                                return "translate("+far+",0)rotate(" + d.rotate + ")";
                            else
                                return "translate(0,"+far+")rotate(" + d.rotate + ")";
                        })
                        .text(function(d) { return d.lemma; })
                      .transition().duration(2000)
                        .attr("transform", function(d) {
                            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                        });
                }


      });


}



var dibujar_sexismo = function(path)
{

  if(dibujo_sexismo)
  {
    return(0)
  }
    dibujo_sexismo = true

d3.json(path, function(error, data) {
    var words = data

    console.log(error)

    var words_frequency = [];

    Object.keys(words).forEach(function(word_lemma){
        o = words[word_lemma];
        o.lemma = word_lemma;
        words_frequency.push(o);
    });

    words_frequency.sort(function(a,b){
        return b.count - a.count;
    });

    var max = d3.max(Object.keys(words), function(k){
        return words[k].count;
    });
    console.log(max);

    var font_size = d3.scale.linear()
        .domain([1, max])
        .range([10,100]);

    /*var color = d3.scale.linear()
        .domain([-max, 0, max])
        .range([d3.hcl(36, 65, 50), d3.hcl(95, 65, 80), d3.hcl(150, 65, 50)])
        .interpolate(d3.interpolateHcl);*/

    var color = d3.scale.quantize()
        .domain([-2,-1, 0, 1, 2])
        .range([d3.hcl(250, 85, 20),d3.hcl(250, 85, 60), d3.hcl(0, 0, 60), d3.hcl(350, 75, 60), d3.hcl(25, 100, 55)]);



          d3.layout.cloud().size([960, 500])
              .words(words_frequency)
              .rotate(function() { return ~~(Math.random() * 2) * 90; })
              .font("Impact")
              .spiral('rectangular')
              .text(function(d){ return d.lemma; })
              .fontSize(function(d){ return font_size(d.count); })
              .on("end", draw)
              .start();

          function draw(words) {
              var svg = d3.select("#nube_sexismo").append("svg")
                  .attr("width", 960)
                  .attr("height", 500);





              // append a group for zoomable content
              var zoom_group = svg.append('g');

              // define a zoom behavior
              var zoom = d3.behavior.zoom()
                  .scaleExtent([1,4]) // min-max zoom
                  .on('zoom', function() {
                    // whenever the user zooms,
                    // modify translation and scale of the zoom group accordingly
                    zoom_group.attr('transform', 'translate('+zoom.translate()+')scale('+zoom.scale()+')');
                  });

              // bind the zoom behavior to the main SVG
              svg.call(zoom);


              zoom_group.append("g")
                  .attr("transform", "translate(480,250)")
                  .selectAll("text")
                  .data(words)
                .enter().append("text")
                  .style("font-size", function(d){ return font_size(d.count) + "px"; })
                  .style("font-family", "Impact")
                  .style("fill", function(d) { return color(d.polarity); })
                  .attr("text-anchor", "middle")
                  .attr("transform", function(d) {
                      var far = 1500*(Math.random() > 0.5 ? +1 : -1);
                      if(d.rotate === 0)
                          return "translate("+far+",0)rotate(" + d.rotate + ")";
                      else
                          return "translate(0,"+far+")rotate(" + d.rotate + ")";
                  })
                  .text(function(d) { return d.lemma; })
                .transition().duration(2000)
                  .attr("transform", function(d) {
                      return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                  });
          }


});

}
