import song_pb2
import song_pb2_grpc
from python_server.domain.entities import Song as DomainSong
from python_server.application.use_cases.song import (
    GetSongsByIdUseCaseSync,
    GetSongsUseCaseSync,
    GetSongsByPlaylistIdUseCaseSync
)
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
from punq import Container


class GrpcSongHelper:
    @staticmethod
    def timestamp_from_datetime(dt: datetime):
        ts = Timestamp()
        ts.FromDatetime(dt)
        return ts

    @staticmethod
    def from_domain(song: DomainSong) -> song_pb2.Song:
        return song_pb2.Song(
            id=song.id,
            created_at=GrpcSongHelper.timestamp_from_datetime(song.created_at),
            nome=song.nome,
            artista=song.artista
        )


class GrpcSongService(song_pb2_grpc.SongServiceServicer):
    def __init__(self, container: Container):
        self.container: Container = container

    def GetAllSong(self, request, context) -> song_pb2.SongList:
        get_songs_use_case: GetSongsUseCaseSync = self.container.resolve(GetSongsUseCaseSync)
        songs: list[DomainSong] = get_songs_use_case()
        return song_pb2.SongList(
            songs=
            [
                GrpcSongHelper.from_domain(song)
                for song in songs
            ]
        )

    def GetSong(self, request, context) -> song_pb2.Song:
        get_songs_by_id_use_case: GetSongsByIdUseCaseSync = self.container.resolve(GetSongsByIdUseCaseSync)
        song: DomainSong | None = get_songs_by_id_use_case(request.id)
        return GrpcSongHelper.from_domain(song) if song else song_pb2.Song()

    def GetSongByPlaylistId(self, request, context) -> song_pb2.SongList:
        get_songs_by_playlist_id_use_case: GetSongsByPlaylistIdUseCaseSync = self.container.resolve(GetSongsByPlaylistIdUseCaseSync)
        songs: list[DomainSong] = get_songs_by_playlist_id_use_case(request.playlist_id)
        return song_pb2.SongList(
            songs=
            [
                GrpcSongHelper.from_domain(song)
                for song in songs
            ]
        )
