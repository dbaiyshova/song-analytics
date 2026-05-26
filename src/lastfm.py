import os
import requests
import re


def get_artist_tags(artist_name):

    api_key = os.getenv("LASTFM_API_KEY")

    url = "https://ws.audioscrobbler.com/2.0/"

    params = {
        "method": "artist.getTopTags",
        "artist": artist_name,
        "api_key": api_key,
        "format": "json",
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    data = response.json()

    return data.get("toptags", {}).get("tag", [])


def clean_lastfm_tags(tags, artist_name):

    merged = {}

    # normalize artist name
    artist_name = re.sub(r"[-_/ ]+", "", artist_name.lower().strip())

    genre_roots = {
        "pop",
        "rock",
        "metal",
        "hiphop",
        "rap",
        "rnb",
        "jazz",
        "blues",
        "folk",
        "country",
        "electronic",
        "house",
        "techno",
        "trance",
        "indie",
        "alternative",
        "punk",
        "reggae",
        "soul",
        "funk",
        "disco",
        "kpop",
        "jpop",
        "cpop",
    }

    for tag in tags:

        # raw tag name
        name = tag["name"].lower().strip()

        # normalize → remove separators
        name = re.sub(r"[-_/ ]+", "", name)

        # remove artist name itself
        if name == artist_name:
            continue

        # keep only genre-like tags
        if not any(root in name for root in genre_roots):
            continue

        count = int(tag["count"])

        # merge duplicates automatically
        merged[name] = merged.get(name, 0) + count

    return [
        {"name": name, "count": count}
        for name, count in sorted(
            merged.items(),
            key=lambda x: x[1],
            reverse=True,
        )
    ]


def get_artist_info(artist_name):

    api_key = os.getenv("LASTFM_API_KEY")

    url = "https://ws.audioscrobbler.com/2.0/"

    params = {
        "method": "artist.getinfo",
        "artist": artist_name,
        "api_key": api_key,
        "format": "json",
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    data = response.json()

    return data.get("artist", {})
