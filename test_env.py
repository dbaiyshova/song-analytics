from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

print("ID length:", len(client_id) if client_id else None)
print("SECRET length:", len(client_secret) if client_secret else None)

print("ID first chars:", client_id[:6] if client_id else None)
print("SECRET first chars:", client_secret[:6] if client_secret else None)