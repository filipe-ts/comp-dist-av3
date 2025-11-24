from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    created_at: datetime
    nome: str | None
    idade: int | None
