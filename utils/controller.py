from utils import everything
from utils import spotify_auth
import re
import json
from decouple import config


def start_conversion(url):
    ytRegex = r"(?:(?:\?|&)(?:v|list)=|embed\/|v\/|youtu\.be\/)((?!videoseries)[a-zA-Z0-9_]*)"
    ytMatch = re.search(ytRegex, url)

    spRegex = r"\bhttps?:\/\/[^/]*\bspotify\.com\/playlist\/([^\s?]+)"
    spMatch = re.search(spRegex, url)

    if ytMatch is not None: # Convert YT to Spotify
        ytListId = ytMatch.group(1)
        yt = everything.yt2spoti(login(), config('YT_KEY'), ytListId)
        return yt.convert()
    elif spMatch is not None: # Convert Spotify to YT
        spListId = spMatch.group(1)
        sp = everything.spoti2yt(spListId, login())
        return json.dumps(sp.convert())
    return "Invalid Link"

def login():
    token = spotify_auth.get_spoti_access_token(config('CLIENT_ID'), config('CLIENT_SECRET'))
    print(token)
    return token

def logState(state):
    print(state)
    if state:
        return 'Logged In Successfully. Log Out?'
    return 'Login'