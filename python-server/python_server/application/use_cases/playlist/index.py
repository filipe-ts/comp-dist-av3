from python_server.application.ports.playlist_repository import IPlaylistRepository
from python_server.domain.entities.playlist import Playlist


async def get_playlist_by_id(
    playlist_repository: IPlaylistRepository, id_: int
) -> Playlist:
    return await playlist_repository.get_by_id(id_)


async def get_playlists_by_user_id(
    playlist_repository: IPlaylistRepository, user_id: int
) -> list[Playlist]:
    return await playlist_repository.get_by_user_id(user_id)


async def get_playlists_by_song_id(
    playlist_repository: IPlaylistRepository, song_id: int
) -> list[Playlist]:
    return await playlist_repository.get_by_song_id(song_id)
