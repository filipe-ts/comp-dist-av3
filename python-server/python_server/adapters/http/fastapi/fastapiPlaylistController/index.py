from fastapi import APIRouter, Depends, Request
from python_server.application.use_cases.playlist import GetPlaylistsBySongIdUseCase, GetPlaylistByIdUseCase, GetPlaylistsByUserIdUseCase
from python_server.domain.entities import Playlist
from pydantic import BaseModel
from python_server.adapters.adapters_entities import IFromDomain
from datetime import datetime


class FastapiPlaylist(BaseModel, IFromDomain):
    id: int
    created_at: datetime
    nome: str | None
    usuario_id: int

    @classmethod
    def from_domain(cls, playlist: Playlist) -> "FastapiPlaylist":
        return FastapiPlaylist(id=playlist.id, created_at=playlist.created_at, nome=playlist.nome, usuario_id=playlist.usuario_id)


playlist_router = APIRouter(prefix="/playlists", tags=["Playlists"])


def get_playlists_by_song_id_service(request: Request) -> GetPlaylistsBySongIdUseCase:
    return request.app.state.container.resolve(GetPlaylistsBySongIdUseCase)


def get_playlist_by_id_service(request: Request) -> GetPlaylistByIdUseCase:
    return request.app.state.container.resolve(GetPlaylistByIdUseCase)


def get_playlists_by_user_id_service(request: Request) -> GetPlaylistsByUserIdUseCase:
    return request.app.state.container.resolve(GetPlaylistsByUserIdUseCase)


@playlist_router.get("/{id}", response_model=FastapiPlaylist | None)
async def get_playlist_by_id(
    id_: int,
    use_case: GetPlaylistByIdUseCase = Depends(get_playlist_by_id_service)
):
    playlist: Playlist | None = await use_case(id_)
    return FastapiPlaylist.from_domain(playlist) if playlist else None


@playlist_router.get("/song/{id_}", response_model=list[FastapiPlaylist])
async def get_playlist_by_song_id(
        id_: int,
        use_case: GetPlaylistsBySongIdUseCase = Depends(get_playlists_by_song_id_service)
) -> list[FastapiPlaylist]:
    playlists: list[Playlist] = await use_case(id_)
    return [FastapiPlaylist.from_domain(playlist) for playlist in playlists]


@playlist_router.get("/user/{id_}", response_model=list[FastapiPlaylist])
async def get_playlists_by_user_id(
        id_: int,
        use_case: GetPlaylistsByUserIdUseCase = Depends(get_playlists_by_user_id_service)
) -> list[FastapiPlaylist]:
    playlists: list[Playlist] = await use_case(id_)
    return [FastapiPlaylist.from_domain(playlist) for playlist in playlists]
