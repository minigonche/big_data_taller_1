from django.shortcuts import render
from django.http import HttpResponse
import requests




# ---------- VIEWS -------------

# Index view
def index(request):
    return render(request, 'app1/index.html', None)

# Process form view
def process_form(request):

	#Extracts the input from the FORM
	input1 = request.POST.get('input2')
	input2  = request.POST.get('input1')


	#PLaces info in dictionary for the REST
	send_data = {}
	send_data['input1'] = input1
	send_data['input2'] = input2
	rest_response = rest_method(data = send_data)

	# Data fro the response view
	data = {}
	data['input1'] = input1
	data['input2'] = input2
	data['rest_response'] = str(rest_response)


	return render(request, 'app1/response.html', data)



# --------- SUPPORTING METHODS -------------


def rest_method(url = 'https://jsonplaceholder.typicode.com/posts',  method = 'POST', data = {}):
	"""
    Method that invokes a rest service. Uses the library *requests*

    Parameters
    ----------
    url : string
		The url of the rest service. Default points to service: https://github.com/typicode/jsonplaceholder#how-to
		offered by https://github.com/typicode/jsonplaceholder#how-to. Is a fake Rest service that can be used for
		tutorials and api testing. The service returns any values you send it.

       
    method : string
		Shhould be one of the permitted REST methods: POST, GET, DELETE etc...

 
	data: dictionary
		Dictionary with the specified parameters for the REST service


    Returns
    -------
    response : dictionary
		Dictionary with the response of the server
        
    """

    #TODO: Method fails if response is not 201. CUrrently only supports POST

	response = requests.post(url, data=data)
	return(response.json())



