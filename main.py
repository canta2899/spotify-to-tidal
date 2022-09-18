from dotenv import load_dotenv
import os

from spotify_scanner import SpotifyScanner

load_dotenv()

client_id: str | None = os.getenv("SPOTIPY_CLIENT_ID")
client_secret: str | None = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri: str | None = os.getenv("SPOTIPY_REDIRECT_URI")
scope: str | None = os.getenv("SPOTIPY_CLIENT_SCOPE")

sc: SpotifyScanner = SpotifyScanner(
    client_id, 
    client_secret, 
    redirect_uri,
    scope)

sc.login()

sc.lookup()

sc.save_file()
