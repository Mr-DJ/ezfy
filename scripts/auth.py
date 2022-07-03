import requests

def get_oauth():
    client_id = "38eeb384bc80459eacda78870cad27a3" #from dashboard
    client_secret = "9a88d70bdbee453baaa1f9564bc26ca4" # from dashboard

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