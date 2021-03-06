#RA2
# Requerimiento Analitico 2
from django.shortcuts import render
from django.http import HttpResponse
import requests
import numpy as np
import copy
import json
from paramiko import SSHClient
from scp import SCPClient
import json
from datetime import datetime

def hacer_requerimiento(request):

	data = {}

	if(get_hours_since_updated() >= 24):
		process_data()
		print_received()



	return render(request,'app1/RA2_index.html', data)



def process_data():
	"""
	Process the data for the webpage to use
	Export all data to the static folder for D3.js to consume
	"""
	output_folder = 'app1/static/app1/local_jsons/RA2/'

	max_visual_size = 10
	max_input = 0
	max_zone = 263 

	#Temporal dictionary
	sizes_dic = {}
	for i in range(1,max_zone + 1):
		sizes_dic[i] = 0

	complete_dic = {}
	sizes = {}


	#weekdays
	weekdays = ['MON','TUE','WED','THU','FRI','SAT','SUN']

	for weekday in weekdays:
		complete_dic[weekday] = [[] for i in range(24)]
		sizes[weekday] = [ dict(sizes_dic) for i in range(24)]

	#monthdays
	month_days = [i for i in range(1,32)]

	for month_day in month_days:
		complete_dic[month_day] = [[] for i in range(24)]
		sizes[month_day] = [ dict(sizes_dic) for i in range(24)]

	lines = get_data()
	for line in lines:
		line = line.strip()
		moment, hour, trips = line.split('\t')
		moment_type = 'WEEK'
		division = 52
		try:
		    moment = int(moment)
		    moment_type = 'MONTH'
		    division = 12
		except:
		    pass

		hour = int(hour)
		current_list = complete_dic[moment][hour] 
		current_sizes =  sizes[moment][hour]


		for trip in trips.split(';'):
			if(trip):
				source, destination, num_trips = trip.split(':')
				source = int(source)
				destination = int(destination)
				num_trips = float(num_trips)


				#Cosntruct the average				
				mean_trips = np.round(num_trips/division,2)


				temp = {}

				if( source in range(1,max_zone + 1) and destination in range(1,max_zone + 1)):            
					temp['source'] = source
					temp['target'] = destination
					temp['count'] = num_trips

					current_list.append(dict(temp))

					current_sizes[source] = current_sizes[source] + num_trips
					max_input = max(max_input, current_sizes[source])

					current_sizes[destination] = current_sizes[destination] + num_trips					
					max_input = max(max_input, current_sizes[destination])            

				else:
					pass
	
	num_trips = copy.deepcopy(sizes)

	for k,v in sizes.items():
		for temp_dict in v:
			for k2, v2 in temp_dict.items():
				temp_dict[k2] = (v2*max_visual_size)/max_input	
	


	with open(output_folder + 'links.json', 'w') as outfile:
		json.dump(complete_dic, outfile,  cls=MyEncoder)
	    	    
	with open(output_folder + 'sizes.json', 'w') as outfile:
		json.dump(sizes, outfile,  cls=MyEncoder)  
	        
	with open(output_folder + 'num_trips.json', 'w') as outfile:
		json.dump(num_trips, outfile,  cls=MyEncoder)  


def get_data():
	"""
	Gets the data. Method designed to switch between local and remote dataset.

	Returns: array of lines
	"""
	return(get_remote_data())
	#return(get_local_data())


def get_local_data():
	"""
	Loads the data from local. Ment for testing

	Returns: array of strings
		Each string corresponds to a line
	"""

	with open('app1/RA/received_data_sample/RA2_result_sample.txt') as f:
		return(f.readlines())




def get_hours_since_updated():
	with open('app1/static/app1/local_jsons/RA2/config.json') as f:
		js = json.load(f)
		date_format = '%d-%m-%Y %H:%M'
		date = datetime.strptime(js['last_query'],date_format)
		diff = datetime.now() - date
		return(diff.days*24)

def print_received():
	with open('app1/static/app1/local_jsons/RA2/config.json', 'w') as f:
		date_format = '%d-%m-%Y %H:%M'
		f.write('{"last_query" : "' + datetime.now().strftime(date_format) + '"}')






def get_remote_data():
	"""
	Loads the data from local. Ment for testing

	Returns: array of strings
		Each string corresponds to a line
	"""


	host = 'bigdata-cluster1-03.virtual.uniandes.edu.co'
	port = 22
	usr = 'bigdata07'
	pwd = '969ba5d6f576c2c4377f2381d2829207'

	ssh = SSHClient()
	ssh.load_system_host_keys()
	ssh.connect(host, port, usr, pwd)


	# SCPCLient takes a paramiko transport as its only argument
	scp = SCPClient(ssh.get_transport())

	scp.get(remote_path = 'results/RA2/part-00000',
		local_path= 'app1/RA/received_data/RA2/')

	scp.close()

	with open('app1/RA/received_data/RA2/part-00000') as f:
		return(f.readlines())




class MyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.integer):
			return int(obj)
		elif isinstance(obj, np.floating):
			return float(obj)
		elif isinstance(obj, np.ndarray):
			return obj.tolist()
		else:
			return super(MyEncoder, self).default(obj)

