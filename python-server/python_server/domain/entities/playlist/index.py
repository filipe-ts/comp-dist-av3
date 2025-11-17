from datetime import datetime

from pydantic import BaseModel


class Playlist(BaseModel):
    id: int
    created_at: datetime
    nome: str
