from src.spotify_client import get_client
import streamlit as st


def search_artist_spotify(artist_name):

    sp = get_client()

    results = sp.search(q=artist_name, type="artist", limit=1)

    items = results.get("artists", {}).get("items", [])

    if not items:
        return None

    artist = items[0]

    images = artist.get("images", [])

    image_url = None
    if images:
        image_url = images[0].get("url")

    return {
        "id": artist.get("id"),
        "name": artist.get("name"),
        "followers": (artist.get("followers", {}).get("total", 0)),
        "genres": artist.get("genres", []),
        "popularity": artist.get("popularity", 0),
        "spotify_url": (artist.get("external_urls", {}).get("spotify")),
        "image": image_url,
    }
