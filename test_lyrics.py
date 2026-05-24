from src.lyrics_client import get_lyrics

lyrics = get_lyrics(
    "Coldplay",
    "Yellow"
)

if lyrics:
    print(lyrics[:500])
else:
    print("Lyrics not found")