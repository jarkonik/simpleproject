from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.generic import View
from django.template import Template, Context, loader, RequestContext


import requests
import json
from myapp.google_distance import GoogleDistance


class HomeView(View):

    def get(self, request, *args, **kwargs):

        #Set origin city
        origin = request.GET.get('origin','Kraków')


        template = loader.get_template('home.html')
       
        #Get distances from Google
        destinations = ['London','Paris','Warsaw','New York','Los Angeles','Melbourne','Moscow','Berlin','Oslo','Rome']
        result =GoogleDistance.get_distance_data(origin,destinations,'AIzaSyDkdZe_tf0LWNNjZty0SSwF80KZib6o5_I')

        # Convert to js compatible arrays
        chart_data = []
        chart_cities = []
        for city,data in result.items():
            chart_data.append(data['duration_value'])
            chart_cities.append(city)
        chart_data = json.dumps(chart_data)
        chart_cities = json.dumps(chart_cities)
      
        context = RequestContext(request,{'destianions_with_time': result,'chart_data': chart_data,'chart_cities': chart_cities,'origin': origin})

        return HttpResponse(template.render(context))


