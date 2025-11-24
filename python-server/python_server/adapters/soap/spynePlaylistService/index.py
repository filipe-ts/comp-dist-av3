from datetime import datetime

import punq
from spyne import ComplexModel, DateTime, Integer, Iterable, ServiceBase, Unicode, rpc

from python_server.adapters.soap.util import SPYNECONSTS, SpyneContext
from python_server.application.use_cases.playlist import (
    GetPlaylistByIdUseCaseSync,
    GetPlaylistsBySongIdUseCaseSync,
    GetPlaylistsByUserIdUseCaseSync,
)
from python_server.domain.entities import Playlist


class SpynePlaylist(ComplexModel):
    id: int
    created_at: datetime
    nome: str | None
    usuario_id: int

    id = Integer
    created_at = DateTime
    nome = Unicode(nullable=True)
    usuario_id = Integer

    @classmethod
    def from_domain(cls, playlist: Playlist) -> "SpynePlaylist":
        return cls(
            id=playlist.id,
            created_at=playlist.created_at,
            nome=playlist.nome,
            usuario_id=playlist.usuario_id,
        )


class SpynePlaylistService(ServiceBase):
    @rpc(Integer, _returns=Iterable(SpynePlaylist))
    def get_playlists_by_song_id(
        ctx: SpyneContext, song_id: int
    ) -> list[SpynePlaylist]:
        container: punq.Container = ctx.udc[SPYNECONSTS.CONTAINER]
        get_playlists_by_song_id_use_case: GetPlaylistsBySongIdUseCaseSync = (
            container.resolve(GetPlaylistsBySongIdUseCaseSync)
        )

        playlists: list[Playlist] = get_playlists_by_song_id_use_case(song_id)

        return [SpynePlaylist.from_domain(playlist) for playlist in playlists]

    @rpc(Integer, _returns=Iterable(SpynePlaylist))
    def get_playlists_by_user_id(
        ctx: SpyneContext, user_id: int
    ) -> list[SpynePlaylist]:
        container: punq.Container = ctx.udc[SPYNECONSTS.CONTAINER]
        get_playlists_by_user_id_use_case: GetPlaylistsByUserIdUseCaseSync = (
            container.resolve(GetPlaylistsByUserIdUseCaseSync)
        )

        playlists: list[Playlist] = get_playlists_by_user_id_use_case(user_id)

        return [SpynePlaylist.from_domain(playlist) for playlist in playlists]

    @rpc(Integer, _returns=SpynePlaylist)
    def get_playlist_by_id(ctx: SpyneContext, id_: int) -> SpynePlaylist | None:
        container: punq.Container = ctx.udc[SPYNECONSTS.CONTAINER]
        get_playlist_by_id_use_case: GetPlaylistByIdUseCaseSync = container.resolve(
            GetPlaylistByIdUseCaseSync
        )

        playlist: Playlist | None = get_playlist_by_id_use_case(id_)

        return SpynePlaylist.from_domain(playlist) if playlist else None
