from yootoob import YouTubeClient
from spoopfy import SpotifyClient
import os 

def run():
    youtube_client=YouTubeClient('') #this part runs by fetching the the credentials client_secrets file
    spotify_client= SpotifyClient(os.getenv('Spotify_auth_token')) 
    #this is where you enter your spotify token
    #unfortunately im gonna need a better way to access this token for distribution purposes, as this method is only
    #feasable if it runs locally
   
   
    playlists=youtube_client.get_playlists()

    for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")
    choice=int(input('Enter choice plz'))
    chosen_playlist=playlists[choice]
    print(f"You selected:{chosen_playlist.title}")      
    #this is the file that you run
    #it imports all of the contents from
    #the other 2 files, but still do not know
    #how to fetch a person's youtube playlist
    #through client credentials and spotify token

    songs=youtube_client.get_videos_from_playlist(chosen_playlist.id)
    print(f"adding {len(songs)}")


    for song in songs:
        spotify_song_id=spotify_client.search_song(song.artist, song.track)
        if spotify_song_id:
            added_song=spotify_client.add_song_to_spotify(spotify_song_id)
            if added_song:
                print(f"Song Added{song.artist}")


if __name__=='__main__':
    run()