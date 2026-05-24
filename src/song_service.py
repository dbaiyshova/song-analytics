from src.spotify_client import search_track_spotify
from src.lyrics_client import get_lyrics
from src.analytics import calculate_basic_metrics


def build_song_object(artist, track):

    # 1. Lyrics
    lyrics = get_lyrics(artist, track)

    # 2. Spotify enrichment
    spotify_data = search_track_spotify(artist, track)

    spotify = None

    if spotify_data:
        spotify = {
            "id": spotify_data["id"],
            "popularity": spotify_data["popularity"],
            "image": spotify_data["album"]["images"][0]["url"]
            if spotify_data["album"]["images"] else None,
            "preview_url": spotify_data.get("preview_url"),
        }

    # 3. Analytics
    analytics = None

    if lyrics:
        analytics = calculate_basic_metrics(lyrics)

    return {
        "artist": artist,
        "title": track,
        "lyrics": lyrics,
        "spotify": spotify,
        "analytics": analytics
    }