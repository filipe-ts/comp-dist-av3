from fastapi import APIRouter, Depends, Request
from python_server.application.use_cases.song import GetSongsUseCase, GetSongsByPlaylistIdUseCase, GetSongsByIdUseCase
from python_server.domain.entities import Song
from pydantic import BaseModel
from python_server.adapters.adapters_entities import IFromDomain
from datetime import datetime


class FastapiSong(BaseModel, IFromDomain):
    id: int
    created_at: datetime
    nome: str | None
    artista: str | None

    @classmethod
    def from_domain(cls, song: Song) -> "FastapiSong":
        return FastapiSong(id=song.id, created_at=song.created_at, nome=song.nome, artista=song.artista)


def get_sogs_service(request: Request) -> GetSongsUseCase:
    return request.app.state.container.resolve(GetSongsUseCase)


def get_songs_by_playlist_id_service(request: Request) -> GetSongsByPlaylistIdUseCase:
    return request.app.state.container.resolve(GetSongsByPlaylistIdUseCase)


def get_songs_by_id_service(request: Request) -> GetSongsByIdUseCase:
    return request.app.state.container.resolve(GetSongsByIdUseCase)


song_router = APIRouter(prefix="/songs", tags=["Songs"])


@song_router.get("/", response_model=list[FastapiSong])
async def get_songs(use_case: GetSongsUseCase = Depends(get_sogs_service)):
    songs: list[Song] = await use_case()
    return [FastapiSong.from_domain(song) for song in songs]


@song_router.get("/playlist/{playlist_id}", response_model=list[FastapiSong])
async def get_songs_by_playlist_id(playlist_id: int, use_case: GetSongsByPlaylistIdUseCase = Depends(get_songs_by_playlist_id_service)):
    songs: list[Song] = await use_case(playlist_id)
    return [FastapiSong.from_domain(song) for song in songs]


@song_router.get("/{id_}", response_model=FastapiSong | None)
async def get_song_by_id(id_: int, use_case: GetSongsByIdUseCase = Depends(get_songs_by_id_service)):
    song: Song | None = await use_case(id_)
    return FastapiSong.from_domain(song) if song else None
