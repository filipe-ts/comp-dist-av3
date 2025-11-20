from abc import ABC, abstractmethod

from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel


class IAdapterEntity(ABC):
    @abstractmethod
    def to_domain(self) -> BaseModel:
        pass


class IPostgresRepository(ABC):
    def __init__(self, pool: AsyncConnectionPool, schema: str) -> None:
        self.pool: AsyncConnectionPool = pool
        self.schema: str = schema
