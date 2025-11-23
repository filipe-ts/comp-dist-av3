from python_server.application.ports.playlist_repository import IPlaylistRepository
from python_server.domain.entities.playlist import Playlist


class GetPlaylistByIdUseCase:
    def __init__(self, repo: IPlaylistRepository):
        self.repo = repo

    async def __call__(self, id_: int) -> Playlist | None:
        return await self.repo.get_by_id(id_)


class GetPlaylistsByUserIdUseCase:
    def __init__(self, repo: IPlaylistRepository):
        self.repo = repo

    async def __call__(self, user_id: int) -> Playlist | None:
        return await self.repo.get_by_user_id(user_id)


class GetPlaylistsBySongIdUseCase:
    def __init__(self, repo: IPlaylistRepository):
        self.repo = repo

    async def __call__(self, song_id: int) -> list[Playlist]:
        return await self.repo.get_by_song_id(song_id)
