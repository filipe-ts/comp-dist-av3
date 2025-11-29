from fastapi import APIRouter, Depends, Request
from python_server.application.use_cases.user import GetUserByIdUseCase, GetUsersUseCase
from python_server.domain.entities import User
from pydantic import BaseModel
from python_server.adapters.adapters_entities import IFromDomain
from datetime import datetime


class FastapiUser(BaseModel, IFromDomain):
    id: int
    created_at: datetime
    nome: str | None
    idade: int | None

    @classmethod
    def from_domain(cls, user: User) -> "FastapiUser":
        return FastapiUser(id=user.id, created_at=user.created_at, nome=user.nome, idade=user.idade)


user_router = APIRouter(prefix="/users", tags=["Users"])


def get_users_service(request: Request) -> GetUsersUseCase:
    return request.app.state.container.resolve(GetUsersUseCase)


def get_user_by_id_service(request: Request) -> GetUserByIdUseCase:
    return request.app.state.container.resolve(GetUserByIdUseCase)


@user_router.get("/{id_}", response_model=FastapiUser | None)
async def get_user_by_id(
    id_: int,
    use_case: GetUserByIdUseCase = Depends(get_user_by_id_service)
):
    user: User | None = await use_case(id_)
    return FastapiUser.from_domain(user) if user else None


@user_router.get("/", response_model=list[FastapiUser])
async def get_users(
    use_case: GetUsersUseCase = Depends(get_users_service)
):
    users: list[User] = await use_case()
    return [FastapiUser.from_domain(user) for user in users]
