from dataclasses import dataclass
from datetime import datetime

from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool, ConnectionPool

from python_server.adapters.adapters_entities import (
    IPostgresRepository,
    IPostgresRepositorySync,
    IToDomain,
    PostgresSchema,
)
from python_server.application.ports.playlist_repository import (
    IPlaylistRepository,
    IPlaylistRepositorySync,
)
from python_server.domain.entities.playlist import Playlist


@dataclass
class PostgresPlaylist(IToDomain):
    id: int
    created_at: datetime
    nome: str | None
    usuario_id: int

    def to_domain(self) -> Playlist:
        return Playlist(
            id=self.id,
            created_at=self.created_at,
            nome=self.nome,
            usuario_id=self.usuario_id,
        )


class PostgresPlaylistRepository(IPlaylistRepository, IPostgresRepository):
    def __init__(self, pool: AsyncConnectionPool, schema: PostgresSchema) -> None:
        super().__init__(pool, schema)

    async def get_by_id(self, id_: int) -> Playlist | None:
        query: str = f"""
        SELECT
            id, created_at, nome, usuario_id
        FROM
            {self.schema}.playlists
        WHERE
            id = %s
        """

        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(PostgresPlaylist)) as cur:
                await cur.execute(query, (id_,))
                row: PostgresPlaylist | None = await cur.fetchone()
                return row.to_domain() if row else None

    async def get_by_song_id(self, song_id: int) -> list[Playlist]:
        query: str = f"""
        SELECT
            p.id,
            p.created_at,
            p.nome,
            p.usuario_id
        FROM {self.schema}.playlists AS p
        INNER JOIN {self.schema}.musica_em_playlist AS mp
            ON p.id = mp.playlist_id
        WHERE
            mp.musica_id = %s
        """

        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(PostgresPlaylist)) as cur:
                await cur.execute(query, (song_id,))
                rows: list[PostgresPlaylist] = await cur.fetchall()
                return [element.to_domain() for element in rows]

    async def get_by_user_id(self, user_id: int) -> list[Playlist]:
        query: str = f"""
        SELECT
            p.id,
            p.created_at,
            p.nome,
            p.usuario_id
        FROM {self.schema}.playlists AS p
        INNER JOIN {self.schema}.usuarios AS u
            ON p.usuario_id = u.id
        WHERE
            u.id = %s
        """

        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(PostgresPlaylist)) as cur:
                await cur.execute(query, (user_id,))
                rows: list[PostgresPlaylist] = await cur.fetchall()
                return [element.to_domain() for element in rows]


class PostgresPlaylistRepositorySync(IPlaylistRepositorySync, IPostgresRepositorySync):
    def __init__(self, pool: ConnectionPool, schema: PostgresSchema) -> None:
        super().__init__(pool, schema)

    def get_by_id(self, id_: int) -> Playlist | None:
        query: str = f"""
        SELECT
            id, created_at, nome, usuario_id
        FROM
            {self.schema}.playlists
        WHERE
            id = %s
        """

        with self.pool.connection() as conn:
            with conn.cursor(row_factory=class_row(PostgresPlaylist)) as cur:
                cur.execute(query, (id_,))
                row: PostgresPlaylist | None = cur.fetchone()
                return row.to_domain() if row else None

    def get_by_song_id(self, song_id: int) -> list[Playlist]:
        query: str = f"""
        SELECT
            p.id,
            p.created_at,
            p.nome,
            p.usuario_id
        FROM {self.schema}.playlists AS p
        INNER JOIN {self.schema}.musica_em_playlist AS mp
            ON p.id = mp.playlist_id
        WHERE
            mp.musica_id = %s
        """

        with self.pool.connection() as conn:
            with conn.cursor(row_factory=class_row(PostgresPlaylist)) as cur:
                cur.execute(query, (song_id,))
                rows: list[PostgresPlaylist] = cur.fetchall()
                return [element.to_domain() for element in rows]

    def get_by_user_id(self, user_id: int) -> list[Playlist]:
        query: str = f"""
        SELECT
            p.id,
            p.created_at,
            p.nome,
            p.usuario_id
        FROM {self.schema}.playlists AS p
        INNER JOIN {self.schema}.usuarios AS u
            ON p.usuario_id = u.id
        WHERE
            u.id = %s
        """

        with self.pool.connection() as conn:
            with conn.cursor(row_factory=class_row(PostgresPlaylist)) as cur:
                cur.execute(query, (user_id,))
                rows: list[PostgresPlaylist] = cur.fetchall()
                return [element.to_domain() for element in rows]
