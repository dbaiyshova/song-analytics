from src.musicbrainz_client import search_artist

data = search_artist("BTS")

print(data["artists"][0]["name"])