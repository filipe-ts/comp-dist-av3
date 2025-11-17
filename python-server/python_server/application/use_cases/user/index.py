from python_server.application.ports.user_repository import IUserRepository
from python_server.domain.entities.user import User


async def get_user_by_id(user_repository: IUserRepository, id_: int) -> User:
    return await user_repository.get_by_id(id_)


async def get_users(user_repository: IUserRepository) -> list[User]:
    return await user_repository.get()
