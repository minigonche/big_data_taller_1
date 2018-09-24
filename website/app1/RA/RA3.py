# RA2
# Requerimiento Analitico 2
from django.shortcuts import render
from django.http import JsonResponse
from paramiko import SSHClient
from scp import SCPClient
import json


def hacer_requerimiento(request):

	data = process_data()
	holidays = ['Christmas','MemorialDay','NewYears','NoHoliday','Summer']

	avg_cost_list = []
	number_of_rides_list = []

	for holiday in holidays:
		holiday = holiday.lower()
		if holiday in list(data.keys()):
			avg_cost = data[holiday][1]
			number_of_rides = data[holiday][0]
			avg_cost_list.append(avg_cost)
			number_of_rides_list.append(number_of_rides)

		else:
			avg_cost_list.append(0)
			number_of_rides_list.append(0)

	context = {'cost': json.dumps(avg_cost_list), 'rides': json.dumps(number_of_rides_list), 'holidays': json.dumps(holidays)}

	#process_data()

	return render(request, 'app1/RA3_index.html', context)


def process_data():
	"""
	Process the data for the webpage to use
	Export all data to the static folder for D3.js to consume
	"""
	lines = get_data()
	response = {}
	for line in lines:
		print(line)
		line = line.strip()
		holiday, total_cost, number_of_trips, average_cost = line.split('\t', 3)


		response[holiday] = [int(number_of_trips), float(average_cost)]

	return response

def get_data():
	"""
	Gets the data. Method designed to switch between local and remote dataset.

	Returns: array of lines
	"""
	#return(get_remote_data())
	return(get_local_data())


def get_local_data():
	"""
	Loads the data from local. Ment for testing

	Returns: array of strings
		Each string corresponds to a line
	"""

	with open('website/app1/RA/received_data_sample/RA3_result_sample.txt') as f:
		return(f.readlines())



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

	scp.get(remote_path = 'results/RA3/part-00000',
		local_path= 'app1/RA/received_data/RA3/')

	scp.close()

	with open('app1/RA/received_data/RA3/part-00000') as f:
		return(f.readlines())