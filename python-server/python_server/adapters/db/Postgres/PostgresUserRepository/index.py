from dataclasses import dataclass
from datetime import datetime

from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool

from python_server.adapters.adapters_entities import IAdapterEntity, IPostgresRepository, PostgresSchema
from python_server.application.ports.user_repository import IUserRepository
from python_server.domain.entities.user import User


@dataclass
class PostgresUser(IAdapterEntity):
    id: int
    created_at: datetime
    nome: str | None
    idade: int | None
    playlist_id: int | None

    def to_domain(self) -> User:
        return User(
            id=self.id,
            created_at=self.created_at,
            nome=self.nome,
            idade=self.idade,
            playlist_id=self.playlist_id,
        )


class PostgresUserRepository(IUserRepository, IPostgresRepository):
    def __init__(self, pool: AsyncConnectionPool, schema: PostgresSchema) -> None:
        super().__init__(pool, schema)

    async def get_by_id(self, id_: int) -> User | None:
        query: str = f"""
        SELECT
            id, created_at, nome, idade, playlist_id
        FROM
            {self.schema}.usuarios
        WHERE
            id = %s
        """

        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(PostgresUser)) as cur:
                await cur.execute(query, (id_,))
                row: PostgresUser | None = await cur.fetchone()
                return row.to_domain() if row else None

    async def get(self) -> list[User]:
        query: str = f"""
        SELECT
            id, created_at, nome, idade, playlist_id
        FROM
            {self.schema}.usuarios
        """

        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(PostgresUser)) as cur:
                await cur.execute(query)
                rows: list[PostgresUser] = await cur.fetchall()
                return [element.to_domain() for element in rows]
