from abc import ABC, abstractmethod
from python_server.domain.entities.song import Song


class ISongRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id_: int) -> Song:
        pass

    @abstractmethod
    async def get_by_playlist_id(self, playlist_id: int) -> list[Song]:
        pass
    
    @abstractmethod
    async def get(self) -> list[Song]:
        pass
