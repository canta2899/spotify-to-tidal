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
batch_size = 100


def run_conversion(spotify_playlist: str, tidal_playlist: str):
    sc: SpotifyScanner = SpotifyScanner(
        CLIENT_ID, 
        CLIENT_SECRET, 
        REDIRECT_URI,
        SCOPE)

    sc.login()
    sc.lookup(playlist=spotify_playlist)

    tracks: list[Song] = sc.get_tracks()

    td: TidalUpdater = TidalUpdater()
    td.login()
    tids: list[str] = list()
    for song in tracks:
        res: str | None = td.search_track(song)
        if not res:
            print(f"Skipped track {song.title} {song.artist}")
            continue
        tids.append(res)

    playlist = td.get_or_create_playlist(tidal_playlist)
    for i in range(0, len(tids), batch_size):
        td.add_to_playlist(playlist, tids[i:i+batch_size])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Include spotify playlist id and tidal playlist name")
        os.exit(1)
    run_conversion(sys.argv[1], " ".join(sys.argv[2:]))
    