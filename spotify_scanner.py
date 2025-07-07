import json
from typing import Any
import spotipy
import os
from song import Song
from spotipy.oauth2 import SpotifyOAuth

class SpotifyScanner:
    
    def __init__(self, 
                 client_id: str | None,
                 client_secret: str | None,
                 redirect_uri: str | None,
                 scope: str | None):
        self.__client_id: str = client_id
        self.__client_secret: str = client_secret
        self.__redirect_uri: str = redirect_uri
        self.__scope: str = scope
        self.sp: spotipy.Spotify
        self.__query_limit: int = 100
        self.__filecontent: list[Song] = []
        self.filename = lambda x: f".spotify_{x}.json"
        
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
            song: Song = Song(
                track['name'],
                track["artists"][0]['name'],
                track["external_ids"]["isrc"]
            )
            self.__filecontent.append(song)
            count += 1
        return count
    
    def get_tracks(self) -> list[Song]:
        return self.__filecontent

    def __load_cached_songs(self, filename: str):
        self.__filecontent.clear()
        with open(filename, "r", encoding="utf-8") as f:
            content: list[dict[str, str]] = json.loads(f.read())
            for entry in content:
                self.__filecontent.append(Song(entry["title"], entry["artist"], entry["isrc"]))

    @staticmethod
    def __get_song_dict(s: Song) -> dict[str, str]:
        return s.get_dictionary()

    def __cache_songs(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            content: list[dict[str, str]] = list(map(self.__get_song_dict, self.__filecontent))
            f.write(json.dumps(content))
        
    def lookup(self, override: bool = False, playlist: str = "likes"):
        name: str = self.filename(playlist)
        if os.path.exists(name) and not override:
            self.__load_cached_songs(name)
            return
        
        keeprunning: bool = True
        offset: int = 0
        while keeprunning:
            if playlist == "likes":
                r: Any = self.sp.current_user_saved_tracks(limit=self.__query_limit, offset=offset)
            else:
                r: Any = self.sp.playlist_tracks(playlist, limit=self.__query_limit, offset=offset)
            count = self.__append_tracks(r)
            keeprunning = count == self.__query_limit
            offset += count
            
        self.__cache_songs(name)
