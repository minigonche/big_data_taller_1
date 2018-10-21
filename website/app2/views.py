from django.shortcuts import render
from django.http import HttpResponse
import requests

from app2.Requerimientos import Polaridad as pol
from app2.Requerimientos import Historico as his
from app2.Requerimientos import Matoneo as mat


# Index view
def index(request):
    return render(request, 'app2/index.html', None)

def Polaridad(request):
	return pol.hacer_requerimiento(request)

def Historico(request):
	return his.hacer_requerimiento(request)

def Matoneo(request):
	return mat.hacer_requerimiento(request)
