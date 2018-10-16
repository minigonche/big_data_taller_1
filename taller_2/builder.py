import urllib.request, urllib.parse, urllib.error
import requests
import base64
import json


access_token = ''
key = 'dHAWevYBB52A2W6rmROpCoOKA'
secret = 'xKdrF5quPEkKj4GSdEaOpskjA1KUqPOGrNQpbpJqwXfONBfJJm'

def getBearer(key, secret):

    # 1. URL encode the consumer key and the consumer secret according to RFC 1738. Note that at the time of writing.
    # NOT NEEDED

    # 2. Concatenate the encoded consumer key, a colon character ”:”, and the encoded consumer secret into a single string.
    key_secret = '{}:{}'.format(key, secret).encode('ascii')

    # 3. Base64 encode the string from the previous step.
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    # 4. Request Bearer token.
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

    auth_data = {
        'grant_type': 'client_credentials'
        }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

    # 5. Request data if response ok.
    if auth_resp.status_code != 200:
        print('Invalid response {}'.format(auth_resp.status_code))
        return None

    else:
        access_token_type = auth_resp.json()['token_type']
        access_token = auth_resp.json()['access_token']

        return access_token

def makeRequest(query, result_type, count):
    #https://developer.twitter.com/en/docs/api-reference-index

    base_url = 'https://api.twitter.com/'
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    search_params = {
        'q': query,
        'result_type': result_type,
        'count': count
    }

    search_url = '{}1.1/search/tweets.json'.format(base_url)

    search_resp = requests.get(search_url, headers=search_headers, params=search_params)

    return search_resp



access_token = getBearer(key, secret)
r = makeRequest('Bolsanaro', 'recent', 1)
print(json.dumps(r.json(),indent=4))