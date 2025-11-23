from datetime import datetime
import strawberry
from python_server.domain.entities import Playlist
from python_server.application.use_cases.playlist import GetPlaylistByIdUseCase, GetPlaylistsByUserIdUseCase, GetPlaylistsBySongIdUseCase
from strawberry.types import Info
from python_server.adapters.graphql.strawberry.Context import GraphQLContext


@strawberry.type
class StrawberryPlaylist:
    id: int
    created_at: datetime
    nome: str | None

    @classmethod
    def from_domain(cls, playlist: Playlist) -> "StrawberryPlaylist":
        return cls(
            id=playlist.id,
            created_at=playlist.created_at,
            nome=playlist.nome
        )


@strawberry.type
class PlaylistQuery:
    @strawberry.field(name="getPlaylistsByUserId", description="Get all playlists by a user id")
    async def get_playlist_by_user_id(self, info: Info[GraphQLContext], user_id: int) -> StrawberryPlaylist | None:
        use_case: GetPlaylistsByUserIdUseCase = info.context.container.resolve(GetPlaylistsByUserIdUseCase)
        playlist: Playlist | None = await use_case(user_id)
        return StrawberryPlaylist.from_domain(playlist) if playlist else None

    @strawberry.field(name="getPlaylistsBySongId", description="Get all playlists by a song id")
    async def get_playlist_by_song_id(self, info: Info[GraphQLContext], song_id: int) -> list[StrawberryPlaylist]:
        use_case: GetPlaylistsBySongIdUseCase = info.context.container.resolve(GetPlaylistsBySongIdUseCase)
        playlists: list[Playlist] = await use_case(song_id)
        return [
            StrawberryPlaylist.from_domain(playlist)
            for playlist in playlists
        ]

    @strawberry.field(name="getPlaylistById", description="Get a playlist by id")
    async def get_playlist_by_id(self, info: Info[GraphQLContext], id_: int) -> StrawberryPlaylist | None:
        use_case: GetPlaylistByIdUseCase = info.context.container.resolve(GetPlaylistByIdUseCase)
        playlist: Playlist | None = await use_case(id_)
        return StrawberryPlaylist.from_domain(playlist) if playlist else None
