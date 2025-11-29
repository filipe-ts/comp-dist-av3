from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from python_server.adapters.graphql.strawberry import graphql_app
from python_server.adapters.soap.soap_app import get_soap_app
from python_server.adapters.adapters_entities import PostgresSchema
from python_server.config.container import create_container
from python_server.config.settings import Settings
from psycopg_pool import AsyncConnectionPool
from python_server.adapters.http.fastapi.fastapiSongController import song_router
from python_server.adapters.http.fastapi.fastapiUserController import user_router
from python_server.adapters.http.fastapi.fastapiPlaylistController import playlist_router


settings = Settings()
postgres_schema = PostgresSchema("public_test")
pool = AsyncConnectionPool(settings.db_uri_unwrapped)

container = create_container(
    postgres_pool=pool,
    postgres_schema=postgres_schema
)

app = FastAPI()

app.state.container = container

# Mount GraphQL under /graphql
app.mount("/graphql", graphql_app)
app.mount("/soap", WSGIMiddleware(get_soap_app()))
app.include_router(user_router)
app.include_router(song_router)
app.include_router(playlist_router)