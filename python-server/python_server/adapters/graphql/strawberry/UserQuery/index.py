from datetime import datetime

import strawberry
from strawberry.types import Info

from python_server.adapters.graphql.strawberry.Context import GraphQLContext
from python_server.application.use_cases.user import GetUserByIdUseCase, GetUsersUseCase
from python_server.domain.entities import User


@strawberry.type
class StrawberryUser:
    id: int
    created_at: datetime
    nome: str | None
    idade: int | None
    playlist_id: int | None

    @classmethod
    def from_domain(cls, user: User) -> "StrawberryUser":
        return cls(
            id=user.id,
            created_at=user.created_at,
            nome=user.nome,
            idade=user.idade,
            playlist_id=user.playlist_id,
        )


@strawberry.type
class UserQuery:
    @strawberry.field(
        name="getUserById", description="Get a user by id"
    )  # type: ignore[misc]
    async def get_user_by_id(
        self, info: Info[GraphQLContext], id_: int
    ) -> StrawberryUser | None:
        use_case: GetUserByIdUseCase = info.context.container.resolve(
            GetUserByIdUseCase
        )
        user: User | None = await use_case(id_)
        return StrawberryUser.from_domain(user) if user else None

    @strawberry.field(
        name="getUsers", description="Get all users from database"
    )  # type: ignore[misc]
    async def get_users(self, info: Info[GraphQLContext]) -> list[StrawberryUser]:
        use_case: GetUsersUseCase = info.context.container.resolve(GetUsersUseCase)
        users: list[User] = await use_case()
        return [StrawberryUser.from_domain(user) for user in users]
