from urllib import response
import requests
import urllib.parse

class SpotifyClient(object):
    def __init__(self):
        def __init__(self, api_token):
            self.api_token=api_token

    def search_song(self, artist, track):  #the song is searched in spotify which was forked from youtube
        query=urllib.parse.quote(f'{artist} {track}')
        url=f"https://api.spotify.com/v1/search?q={query}&type=track"
        response=requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"

            }
        )

        response_json=response.json()

        results= response_json['tracks']['items']
        if results:
            return results[0]['id']
        else:
            raise Exception(f"song not found for{artist}={track}")
   
    def add_song_to_spotify(self, song_id):
        url="https://api.spotify.com/v1/me/tracks"
        response=requests.put(
            url,
            json={       #this function then appends the song onto the users spotify playlist
                         #after forking from youtube
                "ids": [song_id]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        return response