import grpc
from concurrent import futures
from punq import Container
# Import your generated gRPC modules
from python_server.adapters.grpc.grpcio.grpcUserService import user_pb2_grpc
from python_server.adapters.grpc.grpcio.grpcSongService import song_pb2_grpc
from python_server.adapters.grpc.grpcio.grpcPlaylistService import playlist_pb2_grpc
# Import your service implementations
from python_server.adapters.grpc.grpcio.grpcUserService import GrpcUserService
from python_server.adapters.grpc.grpcio.grpcSongService import GrpcSongService
from python_server.adapters.grpc.grpcio.grpcPlaylistService import GrpcPlaylistService
from python_server.config.container import create_container_sync
from python_server.config.settings import Settings
from psycopg_pool import ConnectionPool
from python_server.adapters.adapters_entities import PostgresSchema


def start_grpc_server(container: Container, host="0.0.0.0", port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register each service, injecting the container
    user_pb2_grpc.add_UserServiceServicer_to_server(
        GrpcUserService(container), server
    )
    song_pb2_grpc.add_SongServiceServicer_to_server(
        GrpcSongService(container), server
    )
    playlist_pb2_grpc.add_PlaylistServiceServicer_to_server(
        GrpcPlaylistService(container), server
    )

    server.add_insecure_port(f"{host}:{port}")
    print(f"🚀 gRPC server running at {host}:{port}")
    server.start()
    server.wait_for_termination()


def create_grpc_container() -> Container:
    settings = Settings()
    postgres_schema: PostgresSchema = PostgresSchema("public_test")
    pool: ConnectionPool = ConnectionPool(
        settings.db_uri_unwrapped, min_size=0, max_size=10
    )
    return create_container_sync(
            postgres_pool=pool, postgres_schema=postgres_schema
        )
