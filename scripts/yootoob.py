import os
from urllib import response
import google_auth_oauthlib.flow
import googleapiclient.discovery
import youtube_dl 
from requests import request


class Playlist(object):
    def __init__(self, id, title):
        self.id=id
        self.title=title




class Song(object):
    def __init__(self, artist, track):
        self.artist=artist
        self.track=track

class YouTubeClient(object):
    
    def __init__(self, credentials_location, youtube_client):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


    
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        

   
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_location, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        self.youtube_client = youtube_client

    def get_playlists(self):
        request = self.youtube_client.playlists().list(
            part ="id, snippet",
            maxResults=50,
            mine=True
        )
        response = request.execute()

        playlists=[Playlist(item['id'], item['snippet']['title']) for item in response['items']]
        return playlists
        
    def get_videos_from_playlist(self, playlist_id):
        songs=[]
        request = self.youtube_client.playlistItems().list(
            playlistId=playlist_id,
            part="id, snippet"
        )
        response= request.execute()
        for item in response['items']:
            video_id=item['snippet']['resourceId']['videoId']
            artist, track = self.fetch_artist_track(video_id)
            if artist and track:
                songs.append(Song(artist, track))
        return songs
    
    
    def get_artist_and_track_from_video(self, video_id):
        youtube_url= f"https://www.youtube.com/watch?v={video_id}"

        video= youtube_dl.YoutubeDL({'quiet': True}).extract_info(
            youtube_url, download=False
        )
        artist=video['artist']
        track=video['track']

        return artist, track 