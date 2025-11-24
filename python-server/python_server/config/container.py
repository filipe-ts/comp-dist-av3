import punq
from psycopg_pool import AsyncConnectionPool, ConnectionPool

from python_server.adapters.adapters_entities import PostgresSchema
from python_server.adapters.db.Postgres.postgresPlaylistRepository import (
    PostgresPlaylistRepository,
    PostgresPlaylistRepositorySync,
)
from python_server.adapters.db.Postgres.postgresSongRepository import (
    PostgresSongRepository,
    PostgresSongRepositorySync,
)
from python_server.adapters.db.Postgres.postgresUserRepository import (
    PostgresUserRepository,
    PostgresUserRepositorySync,
)
from python_server.application.ports import (
    IPlaylistRepository,
    IPlaylistRepositorySync,
    ISongRepository,
    ISongRepositorySync,
    IUserRepository,
    IUserRepositorySync,
)
from python_server.application.use_cases.playlist import (
    GetPlaylistByIdUseCase,
    GetPlaylistByIdUseCaseSync,
    GetPlaylistsBySongIdUseCase,
    GetPlaylistsBySongIdUseCaseSync,
    GetPlaylistsByUserIdUseCase,
    GetPlaylistsByUserIdUseCaseSync,
)
from python_server.application.use_cases.song import (
    GetSongsByIdUseCase,
    GetSongsByIdUseCaseSync,
    GetSongsByPlaylistIdUseCase,
    GetSongsByPlaylistIdUseCaseSync,
    GetSongsUseCase,
    GetSongsUseCaseSync,
)
from python_server.application.use_cases.user import (
    GetUserByIdUseCase,
    GetUserByIdUseCaseSync,
    GetUsersUseCase,
    GetUsersUseCaseSync,
)


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


def create_container_sync(
    postgres_pool: ConnectionPool, postgres_schema: PostgresSchema
) -> punq.Container:
    container = punq.Container()
    container.register(ConnectionPool, instance=postgres_pool)
    container.register(PostgresSchema, instance=postgres_schema)

    container.register(IPlaylistRepositorySync, PostgresPlaylistRepositorySync)
    container.register(IUserRepositorySync, PostgresUserRepositorySync)
    container.register(ISongRepositorySync, PostgresSongRepositorySync)

    container.register(GetPlaylistsByUserIdUseCaseSync, GetPlaylistsByUserIdUseCaseSync)
    container.register(GetPlaylistByIdUseCaseSync, GetPlaylistByIdUseCaseSync)
    container.register(GetPlaylistsBySongIdUseCaseSync, GetPlaylistsBySongIdUseCaseSync)
    container.register(GetSongsByIdUseCaseSync, GetSongsByIdUseCaseSync)
    container.register(GetSongsByPlaylistIdUseCaseSync, GetSongsByPlaylistIdUseCaseSync)
    container.register(GetSongsUseCaseSync, GetSongsUseCaseSync)
    container.register(GetUserByIdUseCaseSync, GetUserByIdUseCaseSync)
    container.register(GetUsersUseCaseSync, GetUsersUseCaseSync)

    return container
