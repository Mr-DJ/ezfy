from utils import everything
from utils import spotify_auth
from decouple import config

p = everything.yt2spoti('a','b','c','d')
q = everything.spoti2yt('a','b')

def conversion_type(url):
    if(url[0:25] == 'https://www.youtube.com/p'): # Convert YT to Spotify
        return "You entered a youtube link"
    elif(url[0:25] == 'https://open.spotify.com/'): # Convert Spotify to YT
        return "You entered a spotify link"
    return "invalid link"
