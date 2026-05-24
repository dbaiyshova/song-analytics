import requests


def get_lyrics(artist, song):
    url = (
        f"https://api.lyrics.ovh/v1/"
        f"{artist}/{song}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    return data.get("lyrics")