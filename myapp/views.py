from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.generic import View
from django.template import Template, Context


import requests
import json
from myapp.google_distance import GoogleDistance


class HomeView(View):

    def get(self, request, *args, **kwargs):

        template = Template("""
        <!DOCTYPE html>
        <html>
            {% load staticfiles %}
                <head>
                    <title>Data</title>
                    <style>

                

                    </style>

                    <script src="http://d3js.org/d3.v3.min.js"></script>
                    <script>



                    function drawgraph(){
                        var width = 800;
                        var height = 200;
                        var root = d3.select('#chart').append('svg')
                        .attr({
                            'width': width,
                            'height': height,
                        })
                        .style('border', '1px solid black');

                        var durations = {{ chart_data | safe }};
                        var cities = {{ chart_cities | safe }}
                        var maxDataValue = d3.max(durations);
                        var barHeight = height / durations.length;
                        var barWidth = function(datum) {
                            return datum * ((width-150) / maxDataValue);
                        };
                        var barX = 150;
                        var textX = 0;
                        var barY = function(datum, index) {
                            return (index) * barHeight;
                        };
                        var textY = function(datum, index) {
                            return (index+1) * (barHeight-1);
                        };
                        var bar = root.selectAll('g')
                            .data(durations).enter()

                            .append('g')

                        bar.append("rect")              
                            .attr({
                                'class': 'number',
                                'x': barX,
                                'y': barY,
                                'width': barWidth,
                                'height': barHeight,
                                'fill': '#0f0',
                                'stroke': '#00f',
                            });
                        bar.append("text")
                            .attr("x", textX)
                            .attr("y", textY)

                            .text(function(d,i) {   return cities[i]; });
                    }



                    </script>


                </head>

                <body onload="drawgraph()">
          
                    <h1>Distance and estimated time to arrive to various cities from Krakow:</h1>

                    <div>
                        <ul>
                            {% for city,info in destianions_with_time.items %}
                                <li>
                                <b>{{ city|safe }}</b><br>
                                Distance: {{ info.distance_text | safe }}
                                duration: {{ info.duration_text | safe }}
                                </li>

                            {% endfor %}
                        </ul>
                    </div>
                    <h1>Chart of durations drawn using d3 library:</h1>
                    <div id="chart"></div>
                </body>
            </html>
        """)

        #Get distances from Google
        destinations = ['Poznan','Warszawa','Gdansk','Zakopane','Rzeszow','Wroclaw','Katowice']
        result =GoogleDistance.get_distance_data("Poznan",destinations,'AIzaSyDkdZe_tf0LWNNjZty0SSwF80KZib6o5_I')

        # Convert to js compatible arrays
        chart_data = []
        chart_cities = []
        for city,data in result.items():
            chart_data.append(data['duration_value'])
            chart_cities.append(city)
        chart_data = json.dumps(chart_data)
        chart_cities = json.dumps(chart_cities)
      
        context = Context({'destianions_with_time': result,'chart_data': chart_data,'chart_cities': chart_cities})

        return HttpResponse(template.render(context))


