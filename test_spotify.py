from src.spotify_client import get_client

sp = get_client()

results = sp.search(
    q="BTS",
    type="artist",
    limit=1
)

print(results)