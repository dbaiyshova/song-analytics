from src.spotify_client import get_client


def search_artist_spotify(artist_name):

    sp = get_client()

    results = sp.search(
        q=artist_name,
        type="artist",
        limit=1
    )

    items = results["artists"]["items"]

    if not items:
        return None

    artist = items[0]

    return {
        "name": artist.get("name"),

        "followers": artist.get(
            "followers",
            {}
        ).get(
            "total",
            0
        ),

        "genres": artist.get(
            "genres",
            []
        ),

        "popularity": artist.get(
            "popularity",
            0
        ),

        "spotify_url": artist.get(
            "external_urls",
            {}
        ).get(
            "spotify"
        ),

        "image": (
            artist.get(
                "images",
                [{}]
            )[0].get("url")
            if artist.get("images")
            else None
        )
    }