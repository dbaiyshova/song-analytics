import os
from pathlib import Path

from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import (
    SpotifyClientCredentials
)

from rapidfuzz import fuzz


def load_environment():

    env_path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / ".env"
    )

    load_dotenv(
        dotenv_path=env_path,
        override=True
    )

    print(
        "ENV FILE:",
        env_path
    )


def get_client():

    load_environment()

    client_id = os.getenv(
        "SPOTIPY_CLIENT_ID",
        ""
    ).strip()

    client_secret = os.getenv(
        "SPOTIPY_CLIENT_SECRET",
        ""
    ).strip()

    print(
        "CLIENT ID START:",
        client_id[:8]
    )

    print(
        "CLIENT SECRET EXISTS:",
        bool(client_secret)
    )

    if not client_id:
        raise ValueError(
            "SPOTIPY_CLIENT_ID not found"
        )

    if not client_secret:
        raise ValueError(
            "SPOTIPY_CLIENT_SECRET not found"
        )

    auth_manager = (
        SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
    )

    return spotipy.Spotify(
        auth_manager=auth_manager
    )


def search_track_spotify(
    artist,
    track
):

    try:

        sp = get_client()

        query = (
            f"track:{track} "
            f"artist:{artist}"
        )

        results = sp.search(
            q=query,
            type="track",
            limit=20
        )

        items = (
            results.get(
                "tracks",
                {}
            ).get(
                "items",
                []
            )
        )

        if not items:
            return None

        best = None
        best_score = 0

        for item in items:

            track_score = fuzz.ratio(
                item["name"].lower(),
                track.lower()
            )

            artist_score = fuzz.ratio(
                item["artists"][0]["name"].lower(),
                artist.lower()
            )

            total_score = (
                track_score * 0.7
                + artist_score * 0.3
            )

            if total_score > best_score:

                best_score = total_score
                best = item

        if best_score < 70:
            return None

        return best

    except Exception as e:

        print(
            "Spotify track error:",
            e
        )

        return None


def search_album_spotify(
    artist,
    album
):

    try:

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

        albums = (
            results.get(
                "albums",
                {}
            ).get(
                "items",
                []
            )
        )

        if not albums:
            return None

        return albums[0]

    except Exception as e:

        print(
            "Spotify album error:",
            e
        )

        return None
    


def get_artist_by_name(artist_name):

    sp = get_client()

    results = sp.search(
        q=artist_name,
        type="artist",
        limit=1
    )

    items = (
        results.get(
            "artists",
            {}
        ).get(
            "items",
            []
        )
    )

    if not items:
        return None

    return items[0]


# def get_artist_albums(
#     artist_name
# ):

#     sp = get_client()

#     results = sp.search(
#         q=f"artist:{artist_name}",
#         type="album",
#         limit=50
#     )

#     albums = (
#         results.get(
#             "albums",
#             {}
#         ).get(
#             "items",
#             []
#         )
#     )

#     unique = {}
    
#     for album in albums:

#         name = album.get("name")

#         if name not in unique:
#             unique[name] = album

#     return list(unique.values())

def get_artist_albums(artist_name):

    sp = get_client()

    results = sp.search(
        q=f"artist:{artist_name}",
        type="album"
    )

    print(results)

    return (
        results.get(
            "albums",
            {}
        ).get(
            "items",
            []
        )
    )


def get_album_tracks(
    album_id
):

    sp = get_client()

    results = sp.album_tracks(
        album_id
    )

    return results.get(
        "items",
        []
    )