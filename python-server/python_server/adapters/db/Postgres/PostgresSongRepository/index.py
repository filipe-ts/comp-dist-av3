from dataclasses import dataclass
from datetime import datetime
from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool
from python_server.adapters.adapters_entities import IAdapterEntity, IPostgresRepository, PostgresSchema
from python_server.application.ports.song_repository import ISongRepository
from python_server.domain.entities.song import Song


@dataclass
class PostgresSong(IAdapterEntity):
    id: int
    created_at: datetime
    nome: str | None
    artista: str | None

    def to_domain(self) -> Song:
        return Song(
            id=self.id, created_at=self.created_at, nome=self.nome, artista=self.artista
        )


class PostgresSongRepository(ISongRepository, IPostgresRepository):
    def __init__(self, pool: AsyncConnectionPool, schema: PostgresSchema) -> None:
        super().__init__(pool, schema)

    async def get(self) -> list[Song]:
        query: str = f"""
        SELECT
            id, created_at, nome, artista
        FROM
            {self.schema}.musicas
        """

        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(PostgresSong)) as cur:
                await cur.execute(query)
                rows: list[PostgresSong] = await cur.fetchall()
                return [element.to_domain() for element in rows]

    async def get_by_id(self, id_: int) -> Song | None:
        query: str = f"""
                SELECT
                    id, created_at, nome, artista
                FROM
                    {self.schema}.musicas
                WHERE
                    id = %s
                """

        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(PostgresSong)) as cur:
                await cur.execute(query, (id_,))
                row: PostgresSong | None = await cur.fetchone()
                return row.to_domain() if row else None

    async def get_by_playlist_id(self, playlist_id: int) -> list[Song]:
        query: str = f"""
        SELECT
            m.id,
            m.created_at,
            m.nome,
            m.artista
        FROM {self.schema}.musica_em_playlist AS mp
        LEFT JOIN {self.schema}.musicas AS m
            ON mp.musica_id = m.id
        WHERE mp.playlist_id = %s
        """

        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(PostgresSong)) as cur:
                await cur.execute(query, (playlist_id,))
                rows: list[PostgresSong] = await cur.fetchall()
                return [element.to_domain() for element in rows]
