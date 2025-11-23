from python_server.application.ports.user_repository import IUserRepository
from python_server.domain.entities.user import User


class GetUserByIdUseCase:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    async def __call__(self, id_: int) -> User | None:
        return await self.repo.get_by_id(id_)


class GetUsersUseCase:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    async def __call__(self) -> list[User]:
        return await self.repo.get()

