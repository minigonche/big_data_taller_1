# RA2
# Requerimiento Analitico 2
from django.shortcuts import render



def hacer_requerimiento(request):
    data = {}

    # process_data()

    return render(request, 'app1/RA3_index.html', data)


def process_data():
    """
    Process the data for the webpage to use
    Export all data to the static folder for D3.js to consume
    """