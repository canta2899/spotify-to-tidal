from typing import Any
import re
import tidalapi

class TidalUpdater:
    
    def __init__(self):
        self.session: tidalapi.Session = tidalapi.Session()

    def login(self):
        self.session.login_oauth_simple()

    @staticmethod
    def __normalize(query: str):
        normalized: str
        normalized = ''.join(filter(lambda character:ord(character) < 0xff, normalized.lower())) 
        normalized = normalized.split('-')[0].strip().split('(')[0].strip().split('[')[0].strip()
        normalized = re.sub(r'\s+', ' ')
        return normalized

    def search_track(self, title: str, artist: str, isrc: str) -> str | None:
        query: str = self.__normalize(f"{title} {artist}")
        res: dict[str, Any] = self.session.search(query)
        tidal_id: str | None
        try:
            for t in res['tracks']:
                if t.isrc == isrc:
                    tidal_id = t.id
                    break
        except Exception:
            tidal_id = None
        finally:
            return tidal_id
    
    def add_to_playlist(self, playlist_name: str, tids: list[str]):
        playlist = self.session.user.create_playlist(playlist_name, "Songs saved from spotify")
        playlist.add(tids)
        