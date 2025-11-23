import punq
import strawberry
from strawberry.asgi import GraphQL
from python_server.adapters.graphql.strawberry.Context import GraphQLContext
from python_server.config.container import create_container
from psycopg_pool import AsyncConnectionPool
from python_server.config.settings import Settings
from python_server.adapters.adapters_entities import PostgresSchema
from python_server.adapters.graphql.strawberry.schema.index import graphql_schema
from typing import Any
from starlette.requests import Request
from starlette.websockets import WebSocket


settings = Settings()
postgres_schema: PostgresSchema = PostgresSchema("public_test")
pool: AsyncConnectionPool = AsyncConnectionPool(settings.db_uri_unwrapped)

app_container: punq.Container = create_container(postgres_pool=pool, postgres_schema=postgres_schema)


class DIGraphQL(GraphQL):
    def __init__(self, schema: strawberry.Schema, container: punq.Container, **kwargs):
        super().__init__(schema=schema, **kwargs)
        self.container = container

    async def get_context(self, request: Request | WebSocket, response: Any):
        return GraphQLContext(container=self.container)


graphql_app: GraphQL = DIGraphQL(
    schema=graphql_schema,
    container=app_container,
)
