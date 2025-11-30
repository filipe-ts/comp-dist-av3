import sys
import os
import random
import time
import grpc
from locust import User, task, between, events

# --- CORREÇÃO 1: Aponte para a pasta EXATA onde estão os arquivos .py ---
# Isso permite que o Python ache "user_pb2" diretamente, satisfazendo tanto
# o seu código quanto os imports internos dos arquivos gerados.
sys.path.append(os.path.join(os.getcwd(), "protos", "py"))

# --- CORREÇÃO 2: Importe SEM O PREFIXO da pasta ---
# Agora que o sys.path está apontando para lá, você não deve usar "protos.py."
import protos.py.user_pb2_grpc as u_pb2_grpc, protos.py.user_pb2 as u_pb2
import protos.py.song_pb2_grpc as s_pb2_grpc, protos.py.song_pb2 as s_pb2
import protos.py.playlist_pb2_grpc as pl_pb2_grpc, protos.py.playlist_pb2 as pl_pb2

class GrpcClient:
    """Cliente wrapper para medir tempo e reportar ao Locust"""
    def __init__(self, environment):
        self.env = environment

    def call(self, name, method, request):
        start_time = time.perf_counter()
        exception = None
        response_length = 0
        
        try:
            response = method(request)
            response_length = response.ByteSize()
        except grpc.RpcError as e:
            exception = e
        finally:
            total_time = (time.perf_counter() - start_time) * 1000
            self.env.events.request.fire(
                request_type="gRPC",
                name=name,
                response_time=total_time,
                response_length=response_length,
                exception=exception,
            )

class GrpcUser(User):
    wait_time = between(1, 3)
    # Lembre-se: gRPC não usa http:// prefixo
    host = "localhost:50051"

    def on_start(self):
        # Remove prefixos HTTP caso venham da interface web
        target = self.host.replace("http://", "").replace("https://", "")
        self.channel = grpc.insecure_channel(target)
        
        # CORREÇÃO 3: Atualize as referências para usar os nomes curtos
        self.user_stub = u_pb2_grpc.UserServiceStub(self.channel)
        self.music_stub = s_pb2_grpc.SongServiceStub(self.channel)
        self.playlist_stub = pl_pb2_grpc.PlaylistServiceStub(self.channel)
        
        self.client = GrpcClient(self.environment)

    def on_stop(self):
        self.channel.close()

    # --- TESTES DO USER SERVICE ---
    @task
    def get_all_users(self):
        self.client.call(
            name="GetAllUsers",
            method=self.user_stub.GetAllUsers,
            request=u_pb2.Empty() # Referência direta
        )

    # --- TESTES DO MUSIC SERVICE ---
    @task
    def get_all_music(self):
        self.client.call(
            name="GetAllSong",
            method=self.music_stub.GetAllSong,
            request=s_pb2.Empty()
        )

    # --- TESTES DO PLAYLIST SERVICE ---
    @task
    def get_playlists_by_user(self):
        author_id = random.randint(0, 201)
        self.client.call(
            name="GetPlaylistsByUser",
            method=self.playlist_stub.GetPlaylistsByUser,
            request=u_pb2.UserId(id=author_id)
        )

    @task
    def get_songs_in_playlist(self):
        playlist_id = random.randint(0, 246)
        self.client.call(
            name="GetSongsByPlaylistId",
            method=self.music_stub.GetSongByPlaylistId,
            request=pl_pb2.PlaylistId(id=playlist_id)
        )

    @task
    def get_playlists_with_song(self):
        song_id = random.randint(0, 94)
        self.client.call(
            name="GetPlaylistsBySongId",
            method=self.playlist_stub.GetPlaylistsBySongId,
            request=s_pb2.SongId(id=song_id)
        )
