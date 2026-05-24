from src.musicbrainz_client import (
    search_artist,
    get_artist_releases,
    get_release_tracks
)

artist_data = search_artist("BTS")

artist_id = artist_data["artists"][0]["id"]

releases_data = get_artist_releases(
    artist_id
)

release_id = releases_data[
    "releases"
][0]["id"]

track_data = get_release_tracks(
    release_id
)

media = track_data.get(
    "media",
    []
)

if media:

    tracks = media[0].get(
        "tracks",
        []
    )

    for track in tracks[:5]:
        print(track["title"])