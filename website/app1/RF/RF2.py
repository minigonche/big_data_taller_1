#RF1
# Requerimiento funcional 1
from django.shortcuts import render
from django.http import HttpResponse
import requests
import numpy as np

def hacer_requerimiento(request):
	
	data = {}

	meses = ['Enero','Febrero','Marzo','Abril',
			'Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
	
	# Mes
	mes = request.POST.get('RF2_mes')
	data['mes'] = meses[int(mes) - 1]

	valores = process_data()
	if(mes in valores):
		data['valor'] = str(np.round(valores[mes][0],2)) + ' USD'
		data['total_viajes'] = int(np.round(valores[mes][1],0))
	else:
		data['total_viajes'] = 0
		data['valor'] = ' no hay viajes en las fechas selecionadas'

	
	return render(request, 'app1/response_RF2.html', data)



def process_data():
	""" 
	Process the received data for the view to manipulate
	"""
	lines = get_data()
	response = {}
	for line in lines:
		line = line.strip()
		month, value, total = line.split('\t')
		response[month] = [float(value), float(total)]

	return(response)


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

	with open('app1/RF/received_data_sample/RF2_result_sample.txt') as f:
		return(f.readlines())




def get_remote_data():
	""" 
	Loads the data from local. Ment for testing

	Returns: array of strings
		Each string corresponds to a line
	"""
	raise Error('Not Implemented yet')
	
