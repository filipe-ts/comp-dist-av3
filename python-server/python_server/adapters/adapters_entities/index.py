from abc import ABC, abstractmethod
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel


class IAdapterEntity(ABC):
    @abstractmethod
    def to_domain(self) -> BaseModel:
        pass


class PostgresSchema:
    def __init__(self, schema: str) -> None:
        self.schema_name: str = schema


class IPostgresRepository(ABC):
    def __init__(self, pool: AsyncConnectionPool, schema: PostgresSchema) -> None:
        self.pool: AsyncConnectionPool = pool
        self.schema: str = schema.schema_name
