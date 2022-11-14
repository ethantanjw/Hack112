import spotipy
import random
from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials

class SongGenerator:
    def __init__(self):
        self.sadsongs = None
        self.popsongs = None
        self.rnbsongs = None
        self.topsongs = None

        # username = '8kre5pga5ch5lwdkfwbt3b3fy'
        clientID =  '075efa6725bf43f689ce897c46a58aaa'
        clientSecret = '15f47ee34684452fba2ac5aa84ba3c01'
        # redirect_uri = 'http://localhost:8888/callback/'
        client_credentials_manager = SpotifyClientCredentials(
            client_id='075efa6725bf43f689ce897c46a58aaa', 
            client_secret='15f47ee34684452fba2ac5aa84ba3c01')
        self.spotifyObject = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        # token_dict = oauth_object.get_access_token()
        # token = token_dict['access_token']
        # self.spotifyObject = spotipy.Spotify(auth=token)
        # user_name = self.spotifyObject.current_user()

    def assignSongs(self):
        # sad playlist
        pl_id = 'https://open.spotify.com/playlist/3sWo9fIxqr3c2LgcuJ9TeW?si=b1d74e70e5144396' 
        offset = 0
        sadPlaylistData = self.spotifyObject.playlist_items(pl_id,
                                        offset=offset,
                                        fields='items.track.id,total',
                                        additional_types=['track']) 

        sadPlaylist = sadPlaylistData['items']

        # pop playlist
        pl_id = 'https://open.spotify.com/playlist/4fodP7a0IiLy69HwrYPuQY?si=cf39342caa1d4910 ' 
        offset = 0
        popPlaylistData = self.spotifyObject.playlist_items(pl_id,
                                        offset=offset,
                                        fields='items.track.id,total',
                                        additional_types=['track']) 

        popPlaylist = popPlaylistData['items']

        # top playlist
        pl_id = 'https://open.spotify.com/playlist/5aahtkVoOj646hGD0ufu62?si=9c20e8705ab3460b ' 
        offset = 0
        topPlaylistData = self.spotifyObject.playlist_items(pl_id,
                                        offset=offset,
                                        fields='items.track.id,total',
                                        additional_types=['track']) 

        topPlaylist = topPlaylistData['items']

        # rnb playlist
        pl_id = 'https://open.spotify.com/playlist/2faA36PzAaRI0uAXvRUrj5?si=59aa9eb91e4b433c ' 
        offset = 0
        rnbPlaylistData = self.spotifyObject.playlist_items(pl_id,
                                        offset=offset,
                                        fields='items.track.id,total',
                                        additional_types=['track']) 

        rnbPlaylist = rnbPlaylistData['items']
        
        self.popsongs = self.loadSongs(popPlaylist)
        self.sadsongs = self.loadSongs(sadPlaylist)
        self.topsongs = self.loadSongs(topPlaylist)
        self.rnbsongs = self.loadSongs(rnbPlaylist)

    def loadSongs(self, playlist):
        counter = 0
        songsdict = dict()

        for song in playlist:
            counter += 1
            print(f"Loading song no. {counter}...")
            # print(song)
            song_id = song['track']['id']
            track = self.spotifyObject.track(song_id)
            tempdict = {"id": song['track']['id'],
                        "artists": track['artists'][0]['name'],
                        "name": track['name'],
                        "art": track['album']['images'][0]['url'],
                        "url": "https://open.spotify.com/track/" + song['track']['id'],
                        "uri": "spotify:track:" + song['track']['id']}
            songsdict[counter] = tempdict
        return songsdict

    def getSong(self, emotion):
        if emotion == "sad":
            number = random.randint(1, len(self.rnbsongs))
            return self.sadsongs[number]
        elif emotion == "happy" or emotion == "surprise":
            number = random.randint(1, len(self.popsongs))
            return self.popsongs[number]
        elif emotion == "angry" or emotion == "disgust" or emotion == "fear":
            number = random.randint(1, len(self.sadsongs))
            return self.rnbsongs[number]
        elif emotion == "neutral":
            number = random.randint(1, len(self.topsongs))
            return self.topsongs[number]
