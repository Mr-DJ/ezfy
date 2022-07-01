import youtube_client as YouTubeClient
import spotify_client as SpotifyClient
import os 
#the 2 imports are still correct and ill replace them soon enough
#still need a credentials file along with these 3
def run():
    youtube_client=YouTubeClient('')
    spotify_client= SpotifyClient(os.getenv('SPOTIFY_AUTH_TOKEN'))
    playlists=youtube_client.get_playlists()

    for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")
    choice=int(input('Enter choice plz'))
    chosen_playlist=playlists[choice]
    print(f"You selected:{chosen_playlist.title}")

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
