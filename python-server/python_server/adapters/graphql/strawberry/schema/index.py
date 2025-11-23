import strawberry
from python_server.adapters.graphql.strawberry.UserQuery import UserQuery
from python_server.adapters.graphql.strawberry.SongQuery import SongQuery
from python_server.adapters.graphql.strawberry.PlaylistQuery import PlaylistQuery


@strawberry.type
class Query(
    UserQuery, SongQuery, PlaylistQuery
):
    pass


graphql_schema: strawberry.Schema = strawberry.Schema(query=Query)
