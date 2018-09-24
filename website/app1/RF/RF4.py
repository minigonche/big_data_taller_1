#RF1
# Requerimiento funcional 1
from django.http import HttpResponse
import requests
from django.shortcuts import render
import ast
from paramiko import SSHClient
from scp import SCPClient



week_days = {'1':'Mon','2':'Tue','3':'Wed', '4':'Thu','5':'Fri','6':'Sat','7':'Sun'}

dias = {'1':'Lunes','2':'Martes','3':'Miercoles', '4':'Jueves','5':'Viernes','6':'Sabado','7':'Domingo'}

meses = ['Enero','Febrero','Marzo','Abril',
			'Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

def hacer_requerimiento(request):

	#TODO
	data = {}

	# Franja Horaria
	hora_inicio = request.POST.get('RF4_hora_inicio')
	merid_inicio = request.POST.get('RF4_am_pm_inicio')
	hora_fin = request.POST.get('RF4_hora_fin')
	merid_fin = request.POST.get('RF4_am_pm_fin')


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
	dia_semana = request.POST.get('RF4_dia_semana')
	week_day = week_days[dia_semana]

	data['time_start'] = hora_inicio_string
	data['time_end'] = hora_fin_string	
	data['weekday'] = dias[dia_semana]

	values =  process_data()

	#iterates over each month

	months_summary = []

	for i in range(len(meses)):
		month = i + 1
		final_dict = {}
		if( week_day in values):
			if( month in values[week_day]):

				current_dic = values[week_day][month]
				to_merged_dic = {}

				for h in current_dic.keys():
					hour = int(h)
					if(hora_final_inicio <= hour and hour < hora_final_fin):
						to_merged_dic[h] = dict(current_dic[h])

				final_dict = merge_dicts(to_merged_dic)

		print(final_dict)
		if(final_dict):
			borough, num_trips =  sorted(final_dict.items(), key=lambda kv: -1*kv[1])[0]
			current_summary = {'mes': meses[i], 'borough': borough, 'num_trips': num_trips}
		else:
			current_summary = {'mes': meses[i], 'borough': "-", 'num_trips': "-"}

		months_summary.append(current_summary)


	data['months_summary'] = months_summary


	return render(request, 'app1/response_RF4.html', data)





def process_data():
	""" 
	Process the received data for the view to manipulate
	"""
	 # imports data and makes a dictionary

	final_dict = {}
	lines = get_data()

	for line in lines:
		line = line.strip()
		week_day, trips = line.split('\t',1)
		trips = ast.literal_eval(trips)

		if(week_day not in final_dict):
			final_dict[week_day] = {}


		for trip in trips:
			hour, month, zone, num_trips = trip.split('\t')
			hour, month, num_trips  = int(hour), int(month), int(num_trips)

			if(month not in final_dict[week_day]):
				final_dict[week_day][month] = {}

			if(hour not in final_dict[week_day][month]):
				final_dict[week_day][month][hour] = {}

			final_dict[week_day][month][hour][zone] = num_trips

	return(final_dict)
		


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

	with open('app1/RF/received_data_sample/RF4_result_sample.txt') as f:
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

	scp.get(remote_path = 'results/RF4/part-00000',
		local_path= 'app1/RF/received_data/RF4/')

	scp.close()

	with open('app1/RF/received_data/RF4/part-00000') as f:
		return(f.readlines())
	


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