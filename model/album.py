from dataclasses import dataclass

@dataclass
class Album:
    album_id: int
    artist_id: int
    title: str
    time_album:float

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return self.album_id

    def __hash__(self):
        return hash(self.album_id)