from python_server.application.ports.song_repository import ISongRepository
from python_server.domain.entities.song import Song


class GetSongsByIdUseCase:
    def __init__(self, repo: ISongRepository) -> None:
        self.repo = repo

    async def __call__(self, id_: int) -> Song | None:
        return await self.repo.get_by_id(id_)


class GetSongsByPlaylistIdUseCase:
    def __init__(self, repo: ISongRepository) -> None:
        self.repo = repo

    async def __call__(self, playlist_id: int) -> list[Song]:
        return await self.repo.get_by_playlist_id(playlist_id)


class GetSongsUseCase:
    def __init__(self, repo: ISongRepository) -> None:
        self.repo = repo

    async def __call__(self) -> list[Song]:
        return await self.repo.get()
