#RF1
# Requerimiento funcional 1
from django.http import HttpResponse
import requests

def hacer_requerimiento(request):

	#TODO

	# Franja Horaria
	hora_inicio = request.POST.get('RF1_hora_inicio')
	merid_inicio = request.POST.get('RF1_am_pm_inicio')
	hora_fin = request.POST.get('RF1_hora_fin')
	merid_fin = request.POST.get('RF1_am_pm_fin')


	hora_final_inicio = int(hora_inicio)
	if(merid_inicio == 'PM'):
		hora_final_inicio = hora_final_inicio + 12

	hora_final_fin = int(hora_fin)
	if(merid_fin == 'PM'):
		hora_final_fin = hora_final_fin + 12

	html = "Hora Inicio: " + str(hora_final_inicio) + ':00 '
	html = html + "Hora Fin: " + str(hora_final_fin) + ':00 '
	html = html +  ' (POR IMPLEMENTAR)'
	return HttpResponse(html)
