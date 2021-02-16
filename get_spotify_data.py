import os
import sys
import time
import json
import spotipy
import webbrowser
import time
import spotipy.util as util
from json.decoder import JSONDecodeError
from requests import HTTPError

class Track:
    def __init__(self, device_name, title, artist, duration_ms, progress_ms, art, is_playing):
        self.device_name = device_name
        self.title = title
        self.artist = artist
        self.duration_ms = duration_ms
        self.progress_ms = progress_ms
        self.art = art
        self.is_playing = is_playing

# get the username from terminal
username = sys.argv[1]

# authorize
spotifyObject = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(
    "f34308de95354355a1cd0c3565659dd8",
    "f883197f63654ba0906f2de7ac31be8d",
    "https://google.co.nz/",
    scope="user-read-playback-state"
    ))


def main_loop():
    MAX_TITLE_LENGTH = 36
    TIME_TO_SLEEP = 0.3
    TIME_UNTIL_TIMEOUT = 300
    current_time = 0
    t0 = time.time()
    while current_time < TIME_UNTIL_TIMEOUT:
        current_time += TIME_TO_SLEEP
        try:
            # get track info
            track = spotifyObject.current_user_playing_track()
            devices = spotifyObject.devices()
            for device in devices['devices']:
                if device['is_active']:
                    device_name = device['name']
            title = track['item']['name']
            if len(title) >= MAX_TITLE_LENGTH:
                title = title[:MAX_TITLE_LENGTH] + "..."
            artist = track['item']['artists'][0]['name']
            duration_ms = track['item']['duration_ms']
            progress_ms = track['progress_ms']
            try:
                art = track['item']['album']['images'][1]
            except IndexError:
                art = None
            is_playing = track['is_playing']
            track = Track(device_name, title, artist, duration_ms, progress_ms, art, is_playing)
            track = json.dumps(track.__dict__)
        except (NameError, TypeError, HTTPError):
            track = None

        # write data to disk
        with open("data.json", "w") as data:
            data.seek(0)
            if track:
                data.write(track)
            else:
                data.write('{"error": "Nothing being played.", "errorno": "1"}')
            data.truncate()

        time.sleep(TIME_TO_SLEEP)
    print(f"System timed out. ({ time.time() - t0 } seconds elapsed)")

if __name__ == "__main__":
    main_loop()