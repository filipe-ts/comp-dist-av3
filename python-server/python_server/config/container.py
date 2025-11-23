import punq
from psycopg_pool import AsyncConnectionPool

from python_server.adapters.adapters_entities import PostgresSchema
from python_server.adapters.db.Postgres.PostgresPlaylistRepository import (
    PostgresPlaylistRepository,
)
from python_server.adapters.db.Postgres.PostgresSongRepository import (
    PostgresSongRepository,
)
from python_server.adapters.db.Postgres.PostgresUserRepository import (
    PostgresUserRepository,
)
from python_server.application.ports import (
    IPlaylistRepository,
    ISongRepository,
    IUserRepository,
)
from python_server.application.use_cases.playlist import (
    GetPlaylistByIdUseCase,
    GetPlaylistsBySongIdUseCase,
    GetPlaylistsByUserIdUseCase,
)
from python_server.application.use_cases.song import (
    GetSongsByIdUseCase,
    GetSongsByPlaylistIdUseCase,
    GetSongsUseCase,
)
from python_server.application.use_cases.user import GetUserByIdUseCase, GetUsersUseCase


def create_container(
    postgres_pool: AsyncConnectionPool, postgres_schema: PostgresSchema
) -> punq.Container:
    container = punq.Container()
    container.register(AsyncConnectionPool, instance=postgres_pool)
    container.register(PostgresSchema, instance=postgres_schema)

    container.register(IPlaylistRepository, PostgresPlaylistRepository)
    container.register(IUserRepository, PostgresUserRepository)
    container.register(ISongRepository, PostgresSongRepository)

    container.register(GetPlaylistsByUserIdUseCase, GetPlaylistsByUserIdUseCase)
    container.register(GetPlaylistByIdUseCase, GetPlaylistByIdUseCase)
    container.register(GetPlaylistsBySongIdUseCase, GetPlaylistsBySongIdUseCase)
    container.register(GetSongsByIdUseCase, GetSongsByIdUseCase)
    container.register(GetSongsByPlaylistIdUseCase, GetSongsByPlaylistIdUseCase)
    container.register(GetSongsUseCase, GetSongsUseCase)
    container.register(GetUserByIdUseCase, GetUserByIdUseCase)
    container.register(GetUsersUseCase, GetUsersUseCase)

    return container
