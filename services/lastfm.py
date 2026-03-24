import requests
import os

def get_similar_tracks(artist, track):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getsimilar",
        "artist": artist,
        "track": track,
        "api_key": os.getenv("LASTFM_API_KEY"),
        "format": "json",
        "limit": 5
    }

    res = requests.get(url, params=params)
    data = res.json()

    tracks = data.get("similartracks", {}).get("track", [])

    return [
        {"artist": t["artist"]["name"], "track": t["name"]}
        for t in tracks
    ]