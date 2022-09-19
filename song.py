class Song:

    def __init__(self, title: str, artist: str, isrc: str) -> None:
        self.title: str = title
        self.artist: str = artist
        self.isrc: str = isrc

    def get_dictionary(self) -> dict[str, str]:
        return {
            "title": self.title,
            "artist": self.artist,
            "isrc": self.isrc
        }