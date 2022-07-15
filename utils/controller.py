from utils import everything
from utils import spotify_auth
from decouple import config


def conversion_type(url):
    if(url[0:25] == 'https://www.youtube.com/p'): # Convert YT to Spotify
        return "You entered a youtube link"
    elif(url[0:25] == 'https://open.spotify.com/'): # Convert Spotify to YT
        return "You entered a spotify link"
    return "invalid link"

def login():
    token = spotify_auth.get_spoti_access_token(config('CLIENT_ID'), config('CLIENT_SECRET'))
    return token

def logState(state):
    if state:
        return 'Logged In Successfully'
    return 'Login'