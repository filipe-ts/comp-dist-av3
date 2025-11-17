from datetime import datetime

from pydantic import BaseModel


class Song(BaseModel):
    id: int
    created_at: datetime
    nome: str
    artista: str
