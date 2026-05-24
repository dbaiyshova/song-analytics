from src.spotify_client import search_track_spotify
from src.lyrics_client import get_lyrics
from src.analytics import calculate_basic_metrics


def build_song_object(artist, track):

    # ======================
    # LYRICS
    # ======================

    lyrics = get_lyrics(
        artist,
        track
    )

    # ======================
    # SPOTIFY
    # ======================

    spotify_data = None

    try:

        spotify_data = search_track_spotify(
            artist,
            track
        )

    except Exception as e:

        print("Spotify error:")
        print(e)

    spotify = None

    if spotify_data:

        spotify = {
            "id": spotify_data.get(
                "id"
            ),

            "title": spotify_data.get(
                "name"
            ),

            "popularity": spotify_data.get(
                "popularity",
                0
            ),

            "preview_url": spotify_data.get(
                "preview_url"
            ),

            "spotify_url": spotify_data.get(
                "external_urls",
                {}
            ).get(
                "spotify"
            ),

            "album": spotify_data.get(
                "album",
                {}
            ).get(
                "name"
            ),

            "image": (
                spotify_data.get(
                    "album",
                    {}
                )
                .get(
                    "images",
                    [{}]
                )[0]
                .get(
                    "url"
                )
            )
        }

    # ======================
    # ANALYTICS
    # ======================

    analytics = None

    if lyrics:

        try:

            analytics = calculate_basic_metrics(
                lyrics
            )

        except Exception as e:

            print(
                "Analytics error:"
            )

            print(e)

    # ======================
    # RETURN
    # ======================

    return {
        "artist": artist,
        "title": track,
        "lyrics": lyrics,
        "spotify": spotify,
        "analytics": analytics
    }