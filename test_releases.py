from src.musicbrainz_client import (
    search_artist,
    get_artist_releases
)

artist_data = search_artist("BTS")

artist_id = artist_data["artists"][0]["id"]

releases = get_artist_releases(artist_id)

print(
    releases["releases"][0]["title"]
)