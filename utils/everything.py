import os
import requests
import json
import urllib.parse as ul
from pyyoutube import Api
import json
import urllib.request
import urllib
from decouple import config

spotify_token = '' #this is where the spotify token should be entered
spotify_user_id = '' #the spotify user_id
scopes = ["https://www.googleapis.com/auth/youtube.readonly"] # leave it unchanged
yt_api_key = config("YT_KEY") # enter your YT api key
playlist_id = "" #desired playlist
list = []

def printURL(url): # test function
    return "YOU ENTERED THE FOLLOWING URL: " + url

def get_play(playlist_id): #extract a list of video Id from a given playlist
    api = Api(api_key=yt_api_key)
    song_list = []
    get_play = api.get_playlist_items(playlist_id=playlist_id,count=None)
    for i in range(0,len(get_play.items)):
        song_list.append(get_play.items[i].snippet.resourceId.videoId)

    return song_list
def extract_song(video_id): #extract names of songs from Yt video id
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        song_name = data['title']
    return song_name
  
def get_spotify_uri(track): #get Uniform Resource Identifier(URI) of a given track name
    track = ul.quote(track)
    query = "https://api.spotify.com/v1/search?q={}&type=track".format(
        track,  
    )
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
    response = response.json()
    songs = response["tracks"]["items"]
  
    uri = songs[0]["uri"]
  
    return uri
  
  
def initiate_playlist(): #create a new playlist the given user's library
    
    request_body = {
            "name": "New Playlist",
            "description": "Songs",
            "public": True,
        }
    
  
    query = "https://api.spotify.com/v1/users/{}/playlists".format(
        spotify_user_id)
    response = requests.post(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token),
        },
        json=request_body
    )
    response = response.json()
    return response["id"] # or return response["items"][0]["id"]
  
  
def add_song(playlist_id, uris): #add songs to user's playlist 
    """Add all liked songs into a new Spotify playlist"""
  
    request_data = {
        "uris":uris
    }
  
    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
        playlist_id)
  
    response = requests.post(
        query,
        params=request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
    try:
        response.json()['snapshot_id'] # every transaction returns a snapshot, we can validate it this way
        return "songs added successfully"
    except:
        return "Couldn't add song"
  
  

# iterate through the video IDs and add name of the songs to a list
for i in get_play(playlist_id):
    try:
        list.append(extract_song(i))
    except:
        continue

# print(list)

#iterate through the list of songs and add track to spotify playlist
spotify_playlist_id = initiate_playlist()
for j in list :
    try:
        add_song(spotify_playlist_id,get_spotify_uri(j))
    except:
        continue
