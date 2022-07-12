
from spotipy.oauth2 import SpotifyOAuth

def get_spoti_access_token(client_id,client_secret):
    CLIENT_ID = client_id
    CLIENT_SECRET = client_secret


    sp = SpotifyOAuth(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    redirect_uri="http://localhost:8888/callback",
                    scope="playlist-modify-public")
    return sp.get_access_token(as_dict=False)



