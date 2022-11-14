import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="075efa6725bf43f689ce897c46a58aaa",
                                               client_secret="15f47ee34684452fba2ac5aa84ba3c01",
                                               redirect_uri="http://localhost:8888/callback/",
                                               scope="user-library-read"))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])


#track id, covert art url