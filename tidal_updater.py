from typing import Any
import re
import tidalapi
from song import Song

class TidalUpdater:
    
    def __init__(self):
        self.session: tidalapi.Session = tidalapi.Session()

    def login(self):
        self.session.login_oauth_simple()

    @staticmethod
    def __normalize(query: str):
        normalized: str
        normalized = ''.join(filter(lambda character:ord(character) < 0xff, query.lower())) 
        normalized = query.split('-')[0].strip().split('(')[0].strip().split('[')[0].strip()
        normalized = re.sub(r'\s+', ' ', normalized)
        return normalized

    def search_track(self, song: Song) -> str | None:
        query: str = self.__normalize(f"{song.title} {song.artist}")
        res: dict[str, Any] = self.session.search(query)
        tidal_id: str | None = None
        try:
            for t in res['tracks']:
                if t.isrc == song.isrc:
                    tidal_id = t.id
                    break
            if not tidal_id:
                tidal_id = res['tracks'][0].id
        except Exception:
            pass
        finally:
            return tidal_id
    
    def add_to_playlist(self, playlist_name: str, tids: list[str]):
        playlist = self.session.user.create_playlist(playlist_name, "Songs saved from spotify")
        playlist.add(tids)
        