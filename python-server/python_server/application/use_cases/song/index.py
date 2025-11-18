from python_server.application.ports.song_repository import ISongRepository
from python_server.domain.entities.song import Song


async def get_song_by_id(song_repository: ISongRepository, id_: int) -> Song:
    return await song_repository.get_by_id(id_)


async def get_songs_by_playlist_id(
    song_repository: ISongRepository, playlist_id: int
) -> list[Song]:
    return await song_repository.get_by_playlist_id(playlist_id)


async def get_songs(song_repository: ISongRepository) -> list[Song]:
    return await song_repository.get()
