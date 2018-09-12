#RF1
# Requerimiento funcional 1
from django.http import HttpResponse
import requests

def hacer_requerimiento(request):
	
	#TODO

	# Mes
	mes = request.POST.get('RF2_mes')

	html = "Mes Selecinado: " + str(mes)
	html = html +  ' (POR IMPLEMENTAR)'
	return HttpResponse(html)
	
