#RF1
# Requerimiento funcional 1
from django.http import HttpResponse
import requests
from django.shortcuts import render
import ast
from paramiko import SSHClient
from scp import SCPClient


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



	html = "Hora Inicio: " + str(hora_final_inicio) + ':00 '
	html = html + "Hora Fin: " + str(hora_final_fin) + ':00 '
	html = html + ' Dia Semana: ' +  str(dia_semana)	
	html = html +  ' (POR IMPLEMENTAR)'


	return HttpResponse(html)




def process_data():
	""" 
	Process the received data for the view to manipulate
	"""
	 # imports data and makes a dictionary

	lines = get_data()	
	destination_dict = ast.literal_eval(lines[0])
	final_dict = {}
	for k,v in destination_dict.values():
		k  = int(k)
		final_dict[k] = {}
		current_dic = final_dict[k] 
		for value in v:
			hour, zone, num_trips = value.split('\t')
			hour = int(hour)
			num_trips = int(num_trips)

			if(hour not in current_dic):
				current_dic[hour] = {}

			current_dic[hour][zone] = num_trips

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

	scp.get(remote_path = 'results/RF3/part-00000',
		local_path= 'app1/RF/received_data/RF3/')

	scp.close()

	with open('app1/RF/received_data/RF3/part-00000') as f:
		return(f.readlines())
	

