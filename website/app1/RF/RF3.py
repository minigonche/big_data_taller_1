#RF1
# Requerimiento funcional 1
from django.http import HttpResponse
import requests

def hacer_requerimiento(request):
	
	#TODO

	#Franja Horaria
	hora_inicio = request.POST.get('RF3_horas_inicio')
	minutos_inicio = request.POST.get('RF3_minutos_fin')
	hora_fin = request.POST.get('RF3_horas_fin')
	minutos_fin = request.POST.get('RF3_minutos_fin')

	# Mes
	dia_semana = request.POST.get('RF3_dia_semana')

	#Aeropuerto
	aeropuerto = request.POST.get('RF3_aeropuerto')


	html = "Hora Inicio: " + str(hora_inicio) + ':' + str(minutos_inicio) + ' '
	html = html + "Hora Fin: " + str(hora_fin) + ':' + str(minutos_fin) + ' '
	html = html + ' Dia Semana: ' +  str(dia_semana)
	html = html + ' Aeropuerto: ' +  str(aeropuerto)
	html = html +  ' (POR IMPLEMENTAR)'


	return HttpResponse(html)
