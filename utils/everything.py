import os
import requests
import json
import urllib.parse as ul
from pyyoutube import Api
import json
import urllib.request
import urllib
from decouple import config

# spotify_token = '' #this is where the spotify token should be entered
# spotify_user_id = '' #the spotify user_id
# yt_api_key = config("YT_KEY") # enter your YT api key
# playlist_id = "" #desired playlist



class yt2spoti:
    def __init__(self,spotify_token,spotify_user_id,yt_api_key,playlist_id):
        self.spotify_token = spotify_token
        self.spotify_user_id =spotify_user_id
        self.yt_api_key = yt_api_key
        self.playlist_id =playlist_id


    list = []
    def printURL(url): # test function
        return "YOU ENTERED THE FOLLOWING URL: " + url

    def get_play(self,playlist_id): #extract a list of video Id from a given playlist
        api = Api(api_key=self.yt_api_key)
        song_list = []
        get_play = api.get_playlist_items(playlist_id=playlist_id,count=None)
        for i in range(0,len(get_play.items)):
            song_list.append(get_play.items[i].snippet.resourceId.videoId)

        return song_list
    def extract_song(self,video_id): #extract names of songs from Yt video id
        params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
        url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string
        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            song_name = data['title']
        return song_name
    
    def get_spotify_uri(self,track): #get Uniform Resource Identifier(URI) of a given track name
        track = ul.quote(track)
        query = "https://api.spotify.com/v1/search?q={}&type=track".format(
            track,  
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response = response.json()
        songs = response["tracks"]["items"]
    
        uri = songs[0]["uri"]
    
        return uri
    
    
    def initiate_playlist(self): #create a new playlist the given user's library
        
        request_body = {
                "name": "New Playlist",
                "description": "Songs",
                "public": True,
            }
        
    
        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            self.spotify_user_id)
        response = requests.post(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token),
            },
            json=request_body
        )
        response = response.json()
        return response["id"] # or return response["items"][0]["id"]
    
    
    def add_song(self,playlist_id, uris): #add songs to user's playlist 
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
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        try:
            response.json()['snapshot_id'] # every transaction returns a snapshot, we can validate it this way
            return "songs added successfully"
        except:
            return "Couldn't add song"
    
    
    def convert(self):
        list = []
        # iterate through the video IDs and add name of the songs to a list
        for i in self.get_play(self.playlist_id):
            try:
                list.append(self.extract_song(i))
            except:
                continue

        #iterate through the list of songs and add track to spotify playlist
        spotify_playlist_id = self.initiate_playlist()
        for j in list :
            try:
                self.add_song(spotify_playlist_id,self.get_spotify_uri(j))
            except:
                continue
