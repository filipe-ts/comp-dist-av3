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
from python_server.application.ports.user_repository import (
    IUserRepository,
    IUserRepositorySync,
)
from python_server.domain.entities.user import User


@dataclass
class PostgresUser(IToDomain):
    id: int
    created_at: datetime
    nome: str | None
    idade: int | None

    def to_domain(self) -> User:
        return User(
            id=self.id,
            created_at=self.created_at,
            nome=self.nome,
            idade=self.idade,
        )


class PostgresUserRepository(IUserRepository, IPostgresRepository):
    def __init__(self, pool: AsyncConnectionPool, schema: PostgresSchema) -> None:
        super().__init__(pool, schema)

    async def get_by_id(self, id_: int) -> User | None:
        query: str = f"""
        SELECT
            id, created_at, nome, idade
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
            id, created_at, nome, idade
        FROM
            {self.schema}.usuarios
        """

        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(PostgresUser)) as cur:
                await cur.execute(query)
                rows: list[PostgresUser] = await cur.fetchall()
                return [element.to_domain() for element in rows]


class PostgresUserRepositorySync(IUserRepositorySync, IPostgresRepositorySync):
    def __init__(self, pool: ConnectionPool, schema: PostgresSchema) -> None:
        super().__init__(pool, schema)

    def get_by_id(self, id_: int) -> User | None:
        query: str = f"""
        SELECT
            id, created_at, nome, idade
        FROM
            {self.schema}.usuarios
        WHERE
            id = %s
        """

        with self.pool.connection() as conn:
            with conn.cursor(row_factory=class_row(PostgresUser)) as cur:
                cur.execute(query, (id_,))
                row: PostgresUser | None = cur.fetchone()
                return row.to_domain() if row else None

    def get(self) -> list[User]:
        query: str = f"""
        SELECT
            id, created_at, nome, idade
        FROM
            {self.schema}.usuarios
        """

        with self.pool.connection() as conn:
            with conn.cursor(row_factory=class_row(PostgresUser)) as cur:
                cur.execute(query)
                rows: list[PostgresUser] = cur.fetchall()
                return [element.to_domain() for element in rows]
