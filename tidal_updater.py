from typing import Any
import tidalapi

class TidalUpdater:
    
    def __init__(self):
        self.session: tidalapi.Session = tidalapi.Session()

    def login(self):
        self.session.login_oauth_simple()    

    def search_track(self, title: str, artist: str) -> str | None:
        query: str = f"{title} {artist}"
        query = query.split('-')[0].strip().split('(')[0].strip().split('[')[0].strip()
        track: dict[str, Any] = self.session.search(query, limit=1)
        try:
            return track['tracks'][0].id
        except Exception:
            return None
    
    def add_to_playlist(self, playlist_name: str, tids: list[str]):
        playlist = self.session.user.create_playlist(playlist_name, "Songs saved from spotify")
        playlist.add(tids)
        