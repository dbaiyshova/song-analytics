import requests

BASE_URL = "https://musicbrainz.org/ws/2"


def search_artist(name):
    url = f"{BASE_URL}/artist"

    params = {
        "query": name,
        "fmt": "json"
    }

    response = requests.get(
        url,
        params=params,
        headers={
            "User-Agent": "song-analytics/1.0"
        }
    )

    response.raise_for_status()

    return response.json()


def get_artist_releases(artist_id):
    url = f"{BASE_URL}/release"

    params = {
        "artist": artist_id,
        "fmt": "json",
        "limit": 100
    }

    response = requests.get(
        url,
        params=params,
        headers={
            "User-Agent": "song-analytics/1.0"
        }
    )

    response.raise_for_status()

    return response.json()



def get_release_tracks(release_id):

    url = (
        f"{BASE_URL}/release/{release_id}"
    )

    params = {
        "fmt": "json",
        "inc": "recordings"
    }

    response = requests.get(
        url,
        params=params,
        headers={
            "User-Agent": "song-analytics/1.0"
        }
    )

    response.raise_for_status()

    return response.json()