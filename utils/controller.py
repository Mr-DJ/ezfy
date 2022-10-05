from utils import everything
from utils import spotify_auth
import re
import json
from decouple import config
import os

class migrate:
    c_type = ''
    
    def __init__(self):
        self.c_type = ''

    def start_conversion(self, url):
        ytRegex = r"(?:(?:\?|&)(?:v|list)=|embed\/|v\/|youtu\.be\/)((?!videoseries)[a-zA-Z0-9_]*)"
        ytMatch = re.search(ytRegex, url)

        spRegex = r"\bhttps?:\/\/[^/]*\bspotify\.com\/playlist\/([^\s?]+)"
        spMatch = re.search(spRegex, url)

        if ytMatch is not None: # Convert YT to Spotify
            self.c_type = 'yt2sp'
            ytListId = ytMatch.group(1)
            yt = everything.yt2spoti(login(), os.environ.get('YT_KEY'), ytListId)
            return yt.convert()
        elif spMatch is not None: # Convert Spotify to YT
            self.c_type = 'sp2yt'
            spListId = spMatch.group(1)
            sp = everything.spoti2yt(spListId, login())
            return sp.convert()
        return "Invalid Link"

def login():
    token = spotify_auth.get_spoti_access_token(os.environ.get('CLIENT_ID'), os.environ.get('CLIENT_SECRET'))
    return token

def logState(state):
    if state:
        return 'Logged In Successfully. Log Out?'
    return 'Login'