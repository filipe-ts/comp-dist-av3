import datetime

import punq
from spyne import ComplexModel, DateTime, Integer, Iterable, ServiceBase, Unicode, rpc

from python_server.adapters.soap.util import SPYNECONSTS, SpyneContext
from python_server.application.use_cases.user import (
    GetUserByIdUseCaseSync,
    GetUsersUseCaseSync,
)
from python_server.domain.entities import User


class SpyneUser(ComplexModel):
    # ---------- Mypy type hints ----------
    id: int
    created_at: datetime.datetime
    nome: str | None
    idade: int | None

    # ---------- Spyne definitions ----------
    id = Integer
    created_at = DateTime
    nome = Unicode(nullable=True)
    idade = Integer(nullable=True)

    @classmethod
    def from_domain(cls, user: User) -> "SpyneUser":
        return SpyneUser(
            id=user.id, created_at=user.created_at, nome=user.nome, idade=user.idade
        )


class SpyneUserService(ServiceBase):
    @rpc(Integer, _returns=SpyneUser)
    def get_user_by_id(ctx: SpyneContext, id_: int) -> SpyneUser | None:
        container: punq.Container = ctx.udc[SPYNECONSTS.CONTAINER]
        get_user_by_id_use_case: GetUserByIdUseCaseSync = container.resolve(
            GetUserByIdUseCaseSync
        )

        user: User | None = get_user_by_id_use_case(id_)

        return SpyneUser.from_domain(user) if user else None

    @rpc(_returns=Iterable(SpyneUser))
    def get_users(ctx: SpyneContext) -> list[SpyneUser]:
        container: punq.Container = ctx.udc[SPYNECONSTS.CONTAINER]
        get_users_use_case: GetUsersUseCaseSync = container.resolve(GetUsersUseCaseSync)

        users: list[User] = get_users_use_case()

        return [SpyneUser.from_domain(user) for user in users]
