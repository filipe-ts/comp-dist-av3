from dataclasses import dataclass
from datetime import datetime

from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool

from python_server.adapters.adapters_entities import (
    IAdapterEntity,
    IPostgresRepository,
    PostgresSchema,
)
from python_server.application.ports.playlist_repository import IPlaylistRepository
from python_server.domain.entities.playlist import Playlist


@dataclass
class PostgresPlaylist(IAdapterEntity):
    id: int
    created_at: datetime
    nome: str | None

    def to_domain(self) -> Playlist:
        return Playlist(id=self.id, created_at=self.created_at, nome=self.nome)


class PostgresPlaylistRepository(IPlaylistRepository, IPostgresRepository):
    def __init__(self, pool: AsyncConnectionPool, schema: PostgresSchema) -> None:
        super().__init__(pool, schema)

    async def get_by_id(self, id_: int) -> Playlist | None:
        query: str = f"""
        SELECT
            id, created_at, nome
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
            p.nome
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

    async def get_by_user_id(self, user_id: int) -> Playlist | None:
        query: str = f"""
        SELECT
            p.id,
            p.created_at,
            p.nome
        FROM {self.schema}.playlists AS p
        INNER JOIN {self.schema}.usuarios AS u
            ON p.id = u.playlist_id
        WHERE
            u.id = %s
        """

        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(PostgresPlaylist)) as cur:
                await cur.execute(query, (user_id,))
                rows: PostgresPlaylist | None = await cur.fetchone()
                return rows.to_domain() if rows else None
