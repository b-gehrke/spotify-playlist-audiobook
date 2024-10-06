#!/usr/bin/python3
import spotipy
from spotipy.oauth2 import SpotifyOAuth

print ("!If the program quits immedtialy, the stored token is still valid. No refreshing needs to be done")


SCOPE = "user-modify-playback-state,user-read-playback-state"
SCOPE = input("Scope [" + SCOPE + "]: ") or SCOPE

username = input("Username: ")

auth_manager=SpotifyOAuth(scope=SCOPE)
print(auth_manager.get_authorize_url())
sp = spotipy.Spotify(auth_manager=auth_manager)
