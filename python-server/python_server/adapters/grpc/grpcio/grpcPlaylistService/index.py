import playlist_pb2
import playlist_pb2_grpc
from python_server.domain.entities import Playlist as DomainPlaylist
from python_server.application.use_cases.playlist import GetPlaylistByIdUseCaseSync, GetPlaylistsByUserIdUseCaseSync, GetPlaylistsBySongIdUseCaseSync
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
from punq import Container


class GrpcPlaylistHelper:
    @staticmethod
    def timestamp_from_datetime(dt: datetime):
        ts = Timestamp()
        ts.FromDatetime(dt)
        return ts

    @staticmethod
    def from_domain(playlist: DomainPlaylist) -> playlist_pb2.Playlist:
        return playlist_pb2.Playlist(
            id=playlist.id,
            created_at=GrpcPlaylistHelper.timestamp_from_datetime(playlist.created_at),
            nome=playlist.nome
        )


class GrpcPlaylistService(playlist_pb2_grpc.PlaylistServiceServicer):
    def __init__(self, container: Container):
        self.container: Container = container

    def GetPlaylist(self, request, context) -> playlist_pb2.Playlist:
        get_playlist_use_case: GetPlaylistByIdUseCaseSync = self.container.resolve(GetPlaylistByIdUseCaseSync)
        playlist: DomainPlaylist = get_playlist_use_case(request.id)
        return GrpcPlaylistHelper.from_domain(playlist)

    def GetPlaylistsByUser(self, request, context) -> playlist_pb2.PlaylistList:
        get_playlists_by_user_id_use_case: GetPlaylistsByUserIdUseCaseSync = self.container.resolve(GetPlaylistsByUserIdUseCaseSync)
        playlists: list[DomainPlaylist] = get_playlists_by_user_id_use_case(request.id)
        return playlist_pb2.PlaylistList(
            playlists=[
                GrpcPlaylistHelper.from_domain(playlist)
                for playlist in playlists
            ]
        )

    def GetPlaylistsBySongId(self, request, context) -> playlist_pb2.PlaylistList:
        get_playlists_by_song_id_use_case: GetPlaylistsBySongIdUseCaseSync = self.container.resolve(GetPlaylistsBySongIdUseCaseSync)
        playlists: list[DomainPlaylist] = get_playlists_by_song_id_use_case(request.song_id)
        return playlist_pb2.PlaylistList(
            playlists=[
                GrpcPlaylistHelper.from_domain(playlist)
                for playlist in playlists
            ]
        )
