from psycopg_pool import ConnectionPool
from punq import Container
from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from python_server.adapters.adapters_entities import PostgresSchema
from python_server.adapters.soap.spynePlaylistService import SpynePlaylistService
from python_server.adapters.soap.spyneSongService import SpyneSongService
from python_server.adapters.soap.spyneUserService import SpyneUserService
from python_server.adapters.soap.util import SPYNECONSTS
from python_server.config.container import create_container_sync
from python_server.config.settings import Settings


class DIWsgi:
    def __init__(self, soap_app: Application, container_factory):
        self.soap_app: Application = soap_app
        self._container_factory = container_factory
        self._container: Container | None = None
        self.wsgi_app: WsgiApplication = WsgiApplication(soap_app)

    @property
    def container(self):
        if self._container is None:
            self._container = self._container_factory()
        return self._container

    def __call__(self, environ, start_response):
        environ["udc"] = {SPYNECONSTS.CONTAINER: self.container}
        return self.wsgi_app(environ, start_response)


def _on_method_call(ctx):
    if ctx.udc is None:
        ctx.udc = {}
    ctx.udc.update(ctx.transport.req["udc"])


def get_soap_app() -> DIWsgi:
    soap_app = Application(
        [SpyneUserService, SpynePlaylistService, SpyneSongService],
        tns="http://localhost:8000/soap/",
        in_protocol=Soap11(validator="lxml"),
        out_protocol=Soap11(),
    )
    soap_app.event_manager.add_listener("method_call", _on_method_call)
    settings = Settings()
    postgres_schema: PostgresSchema = PostgresSchema("public_test")
    pool: ConnectionPool = ConnectionPool(
        settings.db_uri_unwrapped, min_size=0, max_size=10
    )

    def foo() -> Container:
        return create_container_sync(
            postgres_pool=pool, postgres_schema=postgres_schema
        )

    wsgi_app = DIWsgi(soap_app, foo)

    return wsgi_app
