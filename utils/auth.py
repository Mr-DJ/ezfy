import requests
import os
import dotenv
from dotenv import load_dotenv , find_dotenv

load_dotenv(find_dotenv())

def get_oauth():
    client_id = os.environ['CLIENT_ID'] #from dashboard
    client_secret = os.environ['CLIENT_SECRET']  # from dashboard

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
})

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    return access_token
