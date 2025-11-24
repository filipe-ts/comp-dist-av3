from datetime import datetime

import punq
from pydantic import BaseModel
from spyne import ComplexModel, DateTime, Integer, Iterable, ServiceBase, Unicode, rpc

from python_server.adapters.soap.util import SPYNECONSTS, SpyneContext
from python_server.application.use_cases.song import (
    GetSongsByIdUseCaseSync,
    GetSongsByPlaylistIdUseCaseSync,
    GetSongsUseCaseSync,
)
from python_server.domain.entities import Song


class SpyneSong(ComplexModel):
    id: int
    created_at: datetime
    nome: str | None
    artista: str | None

    id = Integer
    created_at = DateTime
    nome = Unicode(nullable=True)
    artista = Unicode(nullable=True)

    @classmethod
    def from_domain(cls, domain_entity: BaseModel) -> "SpyneSong":
        return cls(
            id=domain_entity.id,
            created_at=domain_entity.created_at,
            nome=domain_entity.nome,
            artista=domain_entity.artista,
        )


class SpyneSongService(ServiceBase):
    @rpc(_returns=Iterable(SpyneSong))
    def get_songs(ctx: SpyneContext) -> list[SpyneSong]:
        container: punq.Container = ctx.udc[SPYNECONSTS.CONTAINER]
        get_songs_use_case: GetSongsUseCaseSync = container.resolve(GetSongsUseCaseSync)

        songs: list[Song] = get_songs_use_case()

        return [SpyneSong.from_domain(song) for song in songs]

    @rpc(Integer, _returns=Iterable(SpyneSong))
    def get_songs_by_playlist_id(
        ctx: SpyneContext, playlist_id: int
    ) -> list[SpyneSong]:
        container: punq.Container = ctx.udc[SPYNECONSTS.CONTAINER]
        get_songs_by_playlist_id_use_case: GetSongsByPlaylistIdUseCaseSync = (
            container.resolve(GetSongsByPlaylistIdUseCaseSync)
        )

        songs: list[Song] = get_songs_by_playlist_id_use_case(playlist_id)

        return [SpyneSong.from_domain(song) for song in songs]

    @rpc(Integer, _returns=SpyneSong)
    def get_song_by_id(ctx: SpyneContext, id_: int) -> SpyneSong | None:
        container: punq.Container = ctx.udc[SPYNECONSTS.CONTAINER]
        get_songs_by_id_use_case: GetSongsByIdUseCaseSync = container.resolve(
            GetSongsByIdUseCaseSync
        )

        song: Song | None = get_songs_by_id_use_case(id_)

        return SpyneSong.from_domain(song) if song else None
