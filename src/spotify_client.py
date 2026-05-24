from rapidfuzz import fuzz
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os


from dotenv import load_dotenv



load_dotenv()


def get_client():

    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

    if not client_id:
        raise ValueError(
            "SPOTIPY_CLIENT_ID not found in .env"
        )

    if not client_secret:
        raise ValueError(
            "SPOTIPY_CLIENT_SECRET not found in .env"
        )

    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )

    return spotipy.Spotify(
        auth_manager=auth_manager
    )



def search_track_spotify(artist, track):

    sp = get_client()

    query = f"track:{track} artist:{artist}"

    results = sp.search(
        q=query,
        type="track",
        limit=20
    )

    items = results["tracks"]["items"]

    if not items:
        return None

    best = None
    best_score = 0

    for item in items:

        track_score = fuzz.ratio(
            item["name"].lower(),
            track.lower()
        )

        artist_name = item["artists"][0]["name"]

        artist_score = fuzz.ratio(
            artist_name.lower(),
            artist.lower()
        )

        total_score = (
            track_score * 0.7 +
            artist_score * 0.3
        )

        if total_score > best_score:
            best_score = total_score
            best = item

    print("BEST SCORE:", best_score)

    if best_score < 70:
        return None

    return best



def search_album_spotify(
    artist,
    album
):

    sp = get_client()

    query = (
        f"album:{album} "
        f"artist:{artist}"
    )

    results = sp.search(
        q=query,
        type="album",
        limit=1
    )

    albums = results["albums"]["items"]

    if not albums:
        return None

    return albums[0]