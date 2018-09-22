from django.shortcuts import render
from django.http import HttpResponse
import requests

#Importa los scripts de los requerimientos
from app1.RF import RF1 as rf1
from app1.RF import RF2 as rf2
from app1.RF import RF3 as rf3
from app1.RF import RF4 as rf4
from app1.RA import RA2 as ra2



# ---------- VIEWS -------------

# Index view
def index(request):
    return render(request, 'app1/index.html', None)


def RF_1(request):
	return rf1.hacer_requerimiento(request)

def RF_2(request):
	return rf2.hacer_requerimiento(request)

def RF_3(request):
	return rf3.hacer_requerimiento(request)

def RF_4(request):
	return rf4.hacer_requerimiento(request)


def RA_2(request):
	return ra2.hacer_requerimiento(request)



