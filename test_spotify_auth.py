from src.spotify_client import get_client

sp = get_client()

result = sp.search(
    q="BTS",
    type="artist",
    limit=1
)

print(result)