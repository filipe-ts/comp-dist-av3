from abc import ABC, abstractmethod
from python_server.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id_: int) -> User:
        pass

    @abstractmethod
    async def get(self) -> list[User]:
        pass
