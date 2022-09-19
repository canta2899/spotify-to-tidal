from spotify_scanner import SpotifyScanner
from tidal_updater import TidalUpdater
from dotenv import load_dotenv
from song import Song
import sys
import os

load_dotenv()

CLIENT_ID: str = os.getenv("SPOTIPY_CLIENT_ID") or ""
CLIENT_SECRET: str = os.getenv("SPOTIPY_CLIENT_SECRET") or ""
REDIRECT_URI: str = os.getenv("SPOTIPY_REDIRECT_URI") or ""
SCOPE: str = os.getenv("SPOTIPY_CLIENT_SCOPE") or ""

def run_conversion(spotify_playlist: str, tidal_playlist: str):
    sc: SpotifyScanner = SpotifyScanner(
        CLIENT_ID, 
        CLIENT_SECRET, 
        REDIRECT_URI,
        SCOPE)

    sc.login()
    sc.lookup(playlist=spotify_playlist)

    tracks: dict[str, str] = sc.get_tracks()

    td: TidalUpdater = TidalUpdater()
    td.login()
    tids: list[str] = list()
    for track in tracks:
        title=track["title"]
        artist=track["artist"]
        isrc=track["isrc"]
        res: str | None = td.search_track(Song(title, artist, isrc))
        if not res:
            print(f"Skipped track {track['title']} {track['artist']}")
            continue
        tids.append(res)
            
    td.add_to_playlist(tidal_playlist, tids)
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Include spotify playlist id and tidal playlist name")
        os.exit(1)
    run_conversion(sys.argv[1], " ".join(sys.argv[2:]))
    