from rapidfuzz import fuzz
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os


def get_client():

    auth = SpotifyClientCredentials(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
    )

    return spotipy.Spotify(auth_manager=auth)


def search_track_spotify(artist, track):

    sp = get_client()

    query = f"track:{track} artist:{artist}"

    results = sp.search(q=query, type="track", limit=10)

    items = results["tracks"]["items"]

    if not items:
        return None

    # pick best match using fuzzy logic
    best = None
    best_score = 0

    for item in items:

        score = fuzz.ratio(
            item["name"].lower(),
            track.lower()
        )

        if score > best_score:
            best_score = score
            best = item

    return best