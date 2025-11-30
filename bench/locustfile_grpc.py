import sys
import os
import random
import time
import grpc
from locust import User, task, between, events

# Adiciona o diretório atual ao path para encontrar os arquivos gerados
sys.path.append(os.getcwd())

# Import dos arquivos gerados pelo protoc
import user_pb2_grpc, user_pb2
import music_pb2_grpc, music_pb2
import playlist_pb2_grpc, playlist_pb2

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
    host = "localhost:50051"

    def on_start(self):
        self.channel = grpc.insecure_channel(self.host)
        
        # Inicialização dos 3 Stubs (Clientes)
        self.user_stub = user_pb2_grpc.UserServiceStub(self.channel)
        self.music_stub = music_pb2_grpc.MusicServiceStub(self.channel)
        self.playlist_stub = playlist_pb2_grpc.PlaylistServiceStub(self.channel)
        
        self.client = GrpcClient(self.environment)

    def on_stop(self):
        self.channel.close()

    # --- TESTES DO USER SERVICE ---
    @task
    def get_all_users(self):
        # Rota: /usuarios
        self.client.call(
            name="GetAllUsers",
            method=self.user_stub.GetAllUsers,
            request=user_pb2.Empty() # [cite: 8]
        )

    # --- TESTES DO MUSIC SERVICE ---
    @task
    def get_all_music(self):
        # Rota: /musicas
        self.client.call(
            name="GetAllMusic",
            method=self.music_stub.GetAllMusic,
            request=music_pb2.Empty() # [cite: 5]
        )

    # --- TESTES DO PLAYLIST SERVICE ---
    
    @task
    def get_playlists_by_user(self):
        # Rota: /playlists?author=<id>
        author_id = random.randint(0, 201)
        
        # O método está no PlaylistStub, mas o argumento é do UserPackage 
        self.client.call(
            name="GetPlaylistsByUser",
            method=self.playlist_stub.GetPlaylistsByUser,
            request=user_pb2.UserId(id=author_id)
        )

    @task
    def get_songs_in_playlist(self):
        # Rota: /playlists/<id>/musicas
        playlist_id = random.randint(0, 246)
        
        # Argumento definido no próprio playlist.proto 
        self.client.call(
            name="GetSongsInPlaylist",
            method=self.playlist_stub.GetSongsInPlaylist,
            request=playlist_pb2.PlaylistId(id=playlist_id)
        )

    @task
    def get_playlists_with_song(self):
        # Rota: /playlists?has_song=<id>
        song_id = random.randint(0, 94)
        
        # O método está no PlaylistStub, mas o argumento é do MusicPackage 
        self.client.call(
            name="GetPlaylistsWithSong",
            method=self.playlist_stub.GetPlaylistsWithSong,
            request=music_pb2.MusicId(id=song_id)
        )