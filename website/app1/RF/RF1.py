#RF1
# Requerimiento funcional 1
from django.http import HttpResponse
import requests

def hacer_requerimiento(request):

	#TODO

	# Franja Horaria
	hora_inicio = request.POST.get('RF1_horas_inicio')
	minutos_inicio = request.POST.get('RF1_minutos_fin')
	hora_fin = request.POST.get('RF1_horas_fin')
	minutos_fin = request.POST.get('RF1_minutos_fin')


	html = "Hora Inicio: " + str(hora_inicio) + ':' + str(minutos_inicio) + ' '
	html = html + "Hora Fin: " + str(hora_fin) + ':' + str(minutos_fin) + ' '
	html = html +  ' (POR IMPLEMENTAR)'
	return HttpResponse(html)
