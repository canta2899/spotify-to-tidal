import json
from typing import Any
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth

class SpotifyScanner:
    
    def __init__(self, 
                 client_id: str | None,
                 client_secret: str | None,
                 redirect_uri: str | None,
                 scope: str | None):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__redirect_uri = redirect_uri
        self.__scope = scope
        self.sp: spotipy.Spotify
        self.__query_limit = 50
        self.__filecontent: list[dict[str,str]] = []
        self.filename = "./spotify_out.json"
        
    def login(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.__client_id, 
            client_secret=self.__client_secret, 
            redirect_uri=self.__redirect_uri, 
            scope=self.__scope))
    
    def __append_tracks(self, results: dict) -> int:
        count: int = 0
        for item in results['items']:
            track = item['track']
            entry: dict = {}
            entry["title"] = track['name']
            entry["artist"] = track["artists"][0]['name']
            self.__filecontent.append(entry)
            count += 1
        return count
        
    def lookup(self, override: bool = False):
        if os.path.exists(self.filename) and not override:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.__filecontent = json.loads(f.read())
            return
        
        keeprunning: bool = True
        offset: int = 0
        while keeprunning:
            r: Any = self.sp.current_user_saved_tracks(limit=50, offset=offset)
            count = self.__append_tracks(r)
            keeprunning = count == self.__query_limit
            offset += count
            
    def save_file(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.__filecontent, indent=4))
