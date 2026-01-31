from dataclasses import dataclass

@dataclass
class Song:
    song_id: int
    album_id: int
    playlist_id: int


    def __str__(self):
        return str(self.song_id)

    def __repr__(self):
        return self.song_id

    def __hash__(self):
        return hash(self.song_id)