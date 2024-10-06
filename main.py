#!/usr/bin/python3
import time
import json
import argparse
import os
import signal

from threading import Event

import spotipy
from spotipy.oauth2 import SpotifyOAuth


SCOPE = "user-modify-playback-state,user-read-playback-state"

dir_path = os.getcwd()

parser = argparse.ArgumentParser(description="Stores the last position in a playlist and continues there once a spcific track is played")
parser.add_argument("username", help="Spotify username")
parser.add_argument('-c', type=argparse.FileType('r'), dest="config", help="Playlist configuration file")
parser.add_argument('-p', action="append", nargs=2, metavar=('playlist_id', 'trigger_track_id'), help="Can be used multiple times", dest="playlists")
parser.add_argument("--store", type=argparse.FileType('r+'), default=os.path.join(dir_path, "store.json"), help="File to store the last state of playback(s)")

args = parser.parse_args()

print("Starting...")

watched_playlists = []

default_config_path = os.path.join(dir_path, "config.json")
if args.config is None and os.path.isfile(default_config_path):
    args.config = open(default_config_path)

if args.config is not None:
    config_c = args.config.read()
    watched_playlists = watched_playlists if len(config_c.strip()) == 0 else json.loads(config_c)
    print("Loaded {} playlists from config.".format(len(watched_playlists)))

if args.playlists is not None:
    for playlist in args.playlists:
        watched_playlists.append({"id": playlist[0], "trigger": playlist[2]})




store_c = args.store.read().strip()

playback_store = {} if len(store_c) == 0 else json.loads(store_c)

if len(watched_playlists) == 0:
    print("No playlists are configured.")
    exit()

exit = Event()
def quit(signum, frame):
    print(f"Received interrupt signal {signum}. Terminating.")
    exit.set()


signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)


auth_manager=SpotifyOAuth(scope=SCOPE)
sp = spotipy.Spotify(auth_manager=auth_manager)

while not exit.is_set():

    # only get a new token / initialize a new spotify client every two minutes
    for i in range(0, 24):
        if exit.is_set():
            break
        
        try:
            playback = sp.current_playback()

            if playback is not None and playback["is_playing"] == True and playback["context"] is not None:
                playlist = playback["context"]["uri"][-22:]
                track = playback["item"]["id"]

                matches = list(filter(lambda x: x["id"] == playlist, watched_playlists))

                if(len(matches) == 1):
                    match = matches[0]

                    if track == match["trigger"] and playlist in playback_store:
                        try:
                            sp.start_playback(context_uri=f"spotify:playlist:{match['id']}", offset={"uri": playback_store[playlist]["uri"]})
                            sp.shuffle(False)
                            sp.seek_track(playback_store[playlist]["seek"])
                        except Exception as e:
                            print("Exception thrown: " + str(e))
                            pass
                    else:
                        if playlist not in playback_store:
                            playback_store[playlist] = {}
                        
                        playback_store[playlist]["uri"] = playback["item"]["uri"]
                        playback_store[playlist]["seek"] = playback["progress_ms"]

                        # store current playback state to disk
                        args.store.seek(0)
                        args.store.write(json.dumps(playback_store))
                        args.store.truncate()
                elif len(matches) > 1:
                    print("Found ambigous playlist: {}".format(playlist))
        except Exception as e:
            print("Exception thrown: " + str(e))
            pass

        exit.wait(5)

