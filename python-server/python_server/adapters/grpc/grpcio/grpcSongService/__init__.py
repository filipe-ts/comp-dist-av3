from python_server.adapters.grpc.grpcio.grpcSongService import song_pb2_grpc
from .index import GrpcSongService


__all__ = ["GrpcSongService", "song_pb2_grpc"]
