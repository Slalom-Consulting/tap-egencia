import sys
import requests
import json
import logging
import secret 


logging.captureWarnings(True)

def get_new_token():

	baseUrl = secret.get_secret('egenciaBaseUrl')
	auth_server_url = f'${baseUrl}/auth/v1/token'
	client_id = secret.get_secret('egenciaClientId')
	client_secret = secret.get_secret('egenciaClientSecret')

	token_req_payload = {'grant_type': 'client_credentials'}

	token_response = requests.post(
			url=auth_server_url,
			data=token_req_payload,
			auth=(client_id, client_secret)
	)
			 
	if token_response.status_code != 200:
			print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
			sys.exit(1)
	else:
			tokens = json.loads(token_response.text)
			return tokens['access_token']
