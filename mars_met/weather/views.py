
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count, Sum
from models import *
from django.db.models import F
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required

from chartit import DataPool, Chart

def index_view(request):
	
	mars_met_data = magnitude.objects.all()

	marsdata = \
		DataPool(
			series=
				[{'options': {
					'source': mars_met_data},
					'terms': [
						'sol',
						'min_temp',
						'max_temp',
						'pressure',
						'ls']}
				])

	line_chart = Chart(
            datasource = marsdata,
            series_options =
              [{'options': {
            		'type': 'line',
            		'xAxis': 0,
            		'yAxis': 0,
            		'zIndex': 1},
            	'terms':{
            		'sol': [
            			'min_temp',
            			'max_temp']}},
            	{'options': {
            		'type': 'line',
            		'xAxis': 1,
            		'yAxis': 1},
            	'terms':{
            		'sol': [
            			'pressure']}}
            	],
            chart_options =
              {'chart': {
              		'zoomType': 'x',
              		'backgroundColor': '#FFF7F2',
              		'borderColor': '#000000',
              		'borderWidth': 3},
				'exporting': {
					'enabled': True},
				'credits': {
					'enabled': False},
              'title': {
                   'text': 'Mars Temperature Data'},
               'subtitle': {
               		'text': 'Curiosity MSL REMS Data'},
               'xAxis': [{
                    'title': {
                       'text': 'Sol'},
                   	'labels': {
                   		'step': 10}},
                   	{'title': {
                   		'enabled': False},
                   	'labels': {
                   		'enabled': False},
                   	'tickLength': 0}],
          		'yAxis': [{
          			'title': {
          				'text': u'\u00b0C'}},
          			{'title': {
          				'text': 'hPa'}}]})

	polar_chart = Chart(
			datasource = marsdata,
			series_options =
				[{'options': {
					'type': 'line',
					'stacking': True},
				'terms': {
					'ls': [
						'sol']
					}}],
			chart_options = 
				{'chart': {
					'polar': True,
					'alignTicks': False,
              		'backgroundColor': '#FFF7F2',
              		'borderColor': '#000000',
              		'borderWidth': 3},
				'exporting': {
					'enabled': True},
				'credits': {
					'enabled': False},
				'title': {
					'text': 'Mars Solar Longitude Data'},
               'subtitle': {
               		'text': 'Curiosity MSL REMS Data'},
				'xAxis': {
					'min': 0.0,
					'max': 360.0,
					'tickInterval': 90,
					'startOnTick': 0}})

	charts = [line_chart, polar_chart]

	return render_to_response('weather/index.html', {'mars_met_data':mars_met_data,'charts': charts},context_instance=RequestContext(request))
