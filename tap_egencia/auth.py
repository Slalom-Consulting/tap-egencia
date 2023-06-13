import sys
import os
import requests
import json
import logging
# from tap_egencia.secret import get_secret
from dotenv import load_dotenv



logging.captureWarnings(True)

def get_new_token():
	load_dotenv()
	baseUrl = os.getenv('EGENCIA_BASE_URL')
	auth_server_url = f'{baseUrl}/auth/v1/token'
	client_id = os.getenv('EGENCIA_CLIENT_ID')
	client_secret = os.getenv('EGENCIA_SECRET_ID')

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