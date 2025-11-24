from abc import ABC, abstractmethod

from python_server.domain.entities.playlist import Playlist


class IPlaylistRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id_: int) -> Playlist | None:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> list[Playlist]:
        pass

    @abstractmethod
    async def get_by_song_id(self, song_id: int) -> list[Playlist]:
        pass


class IPlaylistRepositorySync(ABC):
    @abstractmethod
    def get_by_id(self, id_: int) -> Playlist | None:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> list[Playlist]:
        pass

    @abstractmethod
    def get_by_song_id(self, song_id: int) -> list[Playlist]:
        pass
