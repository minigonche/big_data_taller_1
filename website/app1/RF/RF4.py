#RF1
# Requerimiento funcional 1
from django.http import HttpResponse
import requests
from django.shortcuts import render

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
