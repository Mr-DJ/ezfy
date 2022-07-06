import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl
import requests
import json
spotify_token = '' #this is where the spotify token should be entered
spotify_user_id = '' #the spotify user_id
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
  
  #below function is the youtube prewritten playlist fetch code
def get_play():
  
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" 
    #Normally, OAuthLib will raise an InsecureTransportError 
    # if you attempt to use OAuth2 over HTTP, rather than HTTPS. 
    # Setting this environment variable will prevent this error from being raised. 
    # This is mostly useful for local testing, or automated tests. Never set this variable in 
    # production. REMEMBER THIS PART !!!!!!!!
  
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "" #this is the place where the program refers to the client _secrets file
  
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
  
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId="" #enter the playlist id over here, i.e the final bit of text in your youtube playlist link
    )
    response = request.execute()
  
    return response
  
  
def extract_youtube_song(dic):
   
  
    url = "https://www.youtube.com/watch?v="
    info = []
    
    for i in range(len(dic["items"])):
  
        video_url = url+str(dic["items"][i]["snippet"]
                            ['resourceId']['videoId'])
        details = youtube_dl.YoutubeDL(
            {}).extract_info(video_url, download=False)
        track, artist = details['track'], details['artist']
  
        info.append((track, artist))
    return info
  
  
def get_spotify_uri(track, artist):
    
  
    query = "https://api.spotify.com/v1/search?\
    query=track%3A{}+artist%3A{}&type=track".format(
        track,
        artist
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
  
    url = songs[0]["uri"]
  
    return url
  
  
def initiate_playlist():
    
    request_body = json.dumps(
        {
            "name": "New Playlist",
            "description": "Songs",
            "public": True,
        }
    )
  
    query = "https://api.spotify.com/v1/users/{}/playlists".format(
        spotify_user_id)
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token),
        },
    )
    response = response.json()
    return response["id"]
  
  
def add_song(playlist_id, urls):
    """Add all liked songs into a new Spotify playlist"""
  
    request_data = json.dumps(urls)
  
    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
        playlist_id)
  
    response = requests.post(
        query,
        data=request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
  
    return "songs added successfully"
  
  
# this function runs to get the prewritten youtube playlist code, i.e receiving playlist data
response = get_play()
  
# this extracts a spotify playlist
play_id = initiate_playlist()
  
# extracts the artist name and 
song_info = extract_youtube_song(response)
  
# getting url for spotify songs
  
urls = []
for i in range(len(response['items'])):
    urls.append(get_spotify_uri(song_info[i][0], song_info[i][1]))
  
# adding song to new playlist
add_song(play_id, urls)
