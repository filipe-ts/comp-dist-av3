from datetime import datetime

import strawberry
from strawberry.types import Info

from python_server.adapters.graphql.strawberry.Context import GraphQLContext
from python_server.application.use_cases.song import (
    GetSongsByIdUseCase,
    GetSongsByPlaylistIdUseCase,
    GetSongsUseCase,
)
from python_server.domain.entities import Song


@strawberry.type
class StrawberrySong:
    id: int
    created_at: datetime
    nome: str | None
    artista: str | None

    @classmethod
    def from_domain(cls, song: Song) -> "StrawberrySong":
        return cls(
            id=song.id, created_at=song.created_at, nome=song.nome, artista=song.artista
        )


@strawberry.type
class SongQuery:
    @strawberry.field(
        name="getSongs", description="Get all songs from database"
    )  # type: ignore[misc]
    async def get_songs(self, info: Info[GraphQLContext]) -> list[StrawberrySong]:
        use_case: GetSongsUseCase = info.context.container.resolve(GetSongsUseCase)
        songs: list[Song] = await use_case()
        return [StrawberrySong.from_domain(song) for song in songs]

    @strawberry.field(
        name="getSongById", description="Get a song by id"
    )  # type: ignore[misc]
    async def get_song_by_id(
        self, info: Info[GraphQLContext], id_: int
    ) -> StrawberrySong | None:
        use_case: GetSongsByIdUseCase = info.context.container.resolve(
            GetSongsByIdUseCase
        )
        song: Song | None = await use_case(id_)
        return StrawberrySong.from_domain(song) if song else None

    @strawberry.field(
        name="getSongsByPlaylistId",
        description="Get all songs in a playlist by the playlist`s id",
    )  # type: ignore[misc]
    async def get_songs_by_playlist_id(
        self, info: Info[GraphQLContext], playlist_id: int
    ) -> list[StrawberrySong]:
        use_case: GetSongsByPlaylistIdUseCase = info.context.container.resolve(
            GetSongsByPlaylistIdUseCase
        )
        songs: list[Song] = await use_case(playlist_id)
        return [StrawberrySong.from_domain(song) for song in songs]
