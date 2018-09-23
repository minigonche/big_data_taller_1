#RF1
# Requerimiento funcional 1

from django.shortcuts import render
import ast



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
    for line in data:
        destination_dict = ast.literal_eval(line)

    while start < finish:
        data = destination_dict[start]
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
        print(len(destination_array))
        top_destination = destination_array[top_destination_index]

        response[top_destination] = max(count_array)

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

	with open('app1/RF/received_data_sample/RF1_result_sample.txt') as f:
		return(f.readlines())


def get_remote_data():
	"""
	Loads the data from local. Meant for testing

	Returns: array of strings
		Each string corresponds to a line
	"""
	raise Error('Not Implemented yet')


def runMapReduce(start, end):
    '''
    :param start: The hour of the day to start the search. Must be a positive integer from 0-23.
    :param end: The hour of the day to end the search. Must be a positive integer from 0-23, larger than the start.
    :return: nothing. This method is responsible for excecuting the mapReduce via FTP.
    '''

