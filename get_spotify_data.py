import os
import sys
import time
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

class Track:
    def __init__(self, title, artist, duration_ms, progress_ms, art, is_playing):
        self.title = title
        self.artist = artist
        self.duration_ms = duration_ms
        self.progress_ms = progress_ms
        self.art = art
        self.is_playing = is_playing

def get_token(username):
    try:
        token = util.prompt_for_user_token(username,
            scope = "user-read-private user-read-playback-state user-modify-playback-state",
            client_id = "f34308de95354355a1cd0c3565659dd8",
            client_secret = "f883197f63654ba0906f2de7ac31be8d",
            redirect_uri = "https://google.co.nz/"
            )
    except (TypeError, AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username,
            scope = "user-read-private user-read-playback-state user-modify-playback-state",
            client_id = "f34308de95354355a1cd0c3565659dd8",
            client_secret = "f883197f63654ba0906f2de7ac31be8d",
            redirect_uri = "https://google.co.nz/"
        )
    return token


# get the username from terminal
username = sys.argv[1]

# get auth token and use it to make spotifyObject
token = get_token(username)

spotifyObject = spotipy.Spotify(auth=token)

while True:

    # get track info
    track = spotifyObject.current_user_playing_track()
    try:
        title = track['item']['name']
        artist = track['item']['artists'][0]['name']
        duration_ms = track['item']['duration_ms']
        progress_ms = track['progress_ms']
        try:
            art = track['item']['album']['images'][1]
        except IndexError:
            print(track)
            art = None
        is_playing = track['is_playing']
        track = Track(title, artist, duration_ms, progress_ms, art, is_playing)
        track = json.dumps(track.__dict__)
    except TypeError:
        track = None

    # write data to disk
    if track:
        with open("data.json", "w") as data:
            data.seek(0)
            data.write(track)
            data.truncate()
        print(track)
    else:
        print('nothing playing')

    time.sleep(1)
