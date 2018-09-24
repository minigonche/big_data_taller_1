#RF1
# Requerimiento funcional 1
from django.http import HttpResponse
from django.shortcuts import render
import requests
import numpy as np
import pickle
from paramiko import SSHClient
from scp import SCPClient

def hacer_requerimiento(request):

	num_anhos = 9
	div_constant = 52

	data = {}
	
	dias = {'1':'Lunes','2':'Martes','3':'Miercoles', '4':'Jueves','5':'Viernes','6':'Sabado','7':'Domingo'}
	airports = { '1': 'Newark', '132': 'JFK', '138':'LaGuardia'}

	#gets the type of summary	
	consolidado = request.POST.get('RF3_consolidado')

	#Loads the zone dictionary
	zones = get_zones()

	# Franja Horaria
	hora_inicio = request.POST.get('RF3_hora_inicio')
	merid_inicio = request.POST.get('RF3_am_pm_inicio')
	hora_fin = request.POST.get('RF3_hora_fin')
	merid_fin = request.POST.get('RF3_am_pm_fin')

	hora_final_inicio = int(hora_inicio)
	if(merid_inicio == 'PM'):
		hora_final_inicio = hora_final_inicio + 12

	hora_final_fin = int(hora_fin)
	if(merid_fin == 'PM'):
		hora_final_fin = hora_final_fin + 12

	#time strings
	hora_inicio_string = hora_inicio + ':00' + merid_inicio.lower()
	hora_fin_string = hora_fin + ':00' + merid_fin.lower()

	
	#REVISA SI LA FRANJA HORARIA ES CORRECTA
	if(hora_final_inicio >= hora_final_fin):
		data['error'] = 'Favor inserte una franja horaria valida. Franja recibida: ' + hora_inicio_string + ' a ' + hora_fin_string + '.'
		return render(request, 'app1/error.html', data)

	# Mes
	dia_semana = request.POST.get('RF3_dia_semana')

	#Aeropuerto
	aeropuerto = request.POST.get('RF3_aeropuerto')


	data['time_start'] = hora_inicio_string
	data['time_end'] = hora_fin_string
	data['airport'] = airports[aeropuerto]
	data['weekday'] = dias[dia_semana]

	values =  process_data()

	trips = []

	final_dict = {}
	if( dia_semana in values):
		if(aeropuerto in values[dia_semana]):
			current_dic = values[dia_semana][aeropuerto]
			to_merged_dic = {}

			for h in current_dic.keys():
				hour = int(h)
				if(hora_final_inicio <= hour and hour < hora_final_fin):
					to_merged_dic[h] = dict(current_dic[h])

			final_dict = merge_dicts(to_merged_dic)

	#sorts the dictionary
	i = 0;
	for dest in sorted(final_dict.items(), key=lambda kv: -1*kv[1]):
		if(dest[0] in zones):
			if(consolidado == "PROMEDIO"):
				prom_dest = np.round(dest[1]/(num_anhos*div_constant),1)
				if(prom_dest > 0):
					i = i + 1
					zone = zones[dest[0]]
					trips.append({'pos':i, 'dest_name': zone['zone'], 'dest_neighborhood': zone['location'], 'count':prom_dest})
			else:
				i = i + 1
				zone = zones[dest[0]]
				trips.append({'pos':i, 'dest_name': zone['zone'], 'dest_neighborhood': zone['location'], 'count':dest[1]})					

	data['trips'] = trips

	if(consolidado == "PROMEDIO"):
		data['consolidado'] = 'Promedio'
	else:
		data['consolidado'] = 'Total'


	return render(request, 'app1/response_RF3.html', data)

def merge_dicts(large_dict):
	"""
	Merges the dictionaries
	"""

	response = {}
	for hour in large_dict.keys():
		current_dic = large_dict[hour]
		for dest in current_dic:
			if(dest in response):
				response[dest] = response[dest] + current_dic[dest]
			else:
				response[dest] = current_dic[dest]

	return(response)


def process_data():
	""" 
	Process the received data for the view to manipulate
	"""
	lines = get_data()
	response = {}
	for line in lines:
		line = line.strip()
		weekday, hour, airport, trips = line.split('\t')

		if(weekday not in response.keys()):
			response[weekday] = {}

		if(airport not in response[weekday].keys()):
			response[weekday][airport] = {}

		if(hour not in response[weekday][airport].keys()):
			response[weekday][airport][hour] = {}

		current_dic = response[weekday][airport][hour]
		for trip in trips.split(';'):
			if(trip):
				source, amount = trip.split(':')
				current_dic[source] = int(amount)


	return(response)


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

	with open('app1/RF/received_data_sample/RF3_result_sample.txt') as f:
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

	scp.get(remote_path = 'results/RF3/part-00000', 
		local_path= 'app1/RF/received_data/RF3/')

	scp.close()

	with open('app1/RF/received_data/RF3/part-00000') as f:
		return(f.readlines())





def get_zones():
	with open( 'app1/static/app1/zones/zonas_dict.pkl', 'rb') as f:
		return pickle.load(f)
	