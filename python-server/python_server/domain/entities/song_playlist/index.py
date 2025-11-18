from datetime import datetime

from pydantic import BaseModel


class SongPlaylist(BaseModel):
    id: int
    created_at: datetime
    playlist_id: int
    musica_id: int
