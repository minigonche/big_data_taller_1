#RF1
# Requerimiento funcional 1

from django.shortcuts import render
import ast
from paramiko import SSHClient
from scp import SCPClient


def hacer_requerimiento(request):

    #TODO
    data = {}
    #default hours
    hora_final_inicio = 1
    hora_final_fin = 2


    # Franja Horaria
    hora_inicio = request.POST.get('RF1_hora_inicio')
    merid_inicio = request.POST.get('RF1_am_pm_inicio')
    hora_fin = request.POST.get('RF1_hora_fin')
    merid_fin = request.POST.get('RF1_am_pm_fin')

    if hora_inicio and hora_fin:
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

    html_incio = hora_inicio_string
    html_fin = hora_fin_string

    top_destination_valores = process_data(hora_final_inicio, hora_final_fin)
    if list(top_destination_valores.keys()) == []:
        data['error'] = 'No se encontró informción para la franja de hora requerida'
        return render(request, 'app1/error.html', data)
    else:
        top_destination = list(top_destination_valores.keys())[0]
        numero_de_viajes = top_destination_valores[top_destination]

    #context -> hora_inicio: html_inicio, hora_fin: html_fin, top_destina
    data['inicio'] = html_incio
    data['fin'] = html_fin
    data['destino'] = top_destination
    data['viajes'] = numero_de_viajes


    return render(request, 'app1/response_RF1.html', data)

def process_data(start, finish):
    """
    Process the received data for the view to manipulate
    """
    response = {}

    data = get_data()

    destination_array = ['Bronx', 'EWR', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Unknown']
    count_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # imports data and makes a dictionary    
    destination_dict = ast.literal_eval(data)

    while start < finish:
        try:
            data = destination_dict[start]
        except KeyError:
            start += 1
            continue
        if data == []:
            start += 1
            continue
        for i in data:
            i = i.strip()
            destination, count = i.split('\t', 1)
            count = int(count)
            if destination in destination_array:
                index = destination_array.index(destination)
                count_array[index] += count
            else:
                continue
        start += 1
        top_destination_index = count_array.index(max(count_array))
        top_destination = destination_array[top_destination_index]

        response[top_destination] = max(count_array)

    return response


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

	with open('app1/RF/received_data_sample/RF1_result_sample.txt') as f:
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

    scp.get(remote_path = 'results/RF1/part-00000',
        local_path= 'app1/RF/received_data/RF1/')

    scp.close()

    with open('app1/RF/received_data/RF1/part-00000') as f:
        return f.readline()






