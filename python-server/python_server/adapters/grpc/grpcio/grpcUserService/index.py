import user_pb2
import user_pb2_grpc
from python_server.application.use_cases.user import GetUserByIdUseCaseSync, GetUsersUseCaseSync
from python_server.domain.entities import User as DomainUser
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
from punq import Container


class GrpcUserHelper:
    @staticmethod
    def timestamp_from_datetime(dt: datetime):
        ts = Timestamp()
        ts.FromDatetime(dt)
        return ts

    @staticmethod
    def from_domain(user: DomainUser) -> user_pb2.User:
        return user_pb2.User(id=user.id, created_at=GrpcUserHelper.timestamp_from_datetime(user.created_at), nome=user.nome, idade=user.idade)


class GrpcUserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self, container: Container):
        self.container: Container = container

    def GetUser(self, request, context) -> user_pb2.User:
        use_case: GetUserByIdUseCaseSync = self.container.resolve(GetUserByIdUseCaseSync)
        user: DomainUser = use_case(request.id)
        return GrpcUserHelper.from_domain(user)

    def GetAllUsers(self, request, context) -> user_pb2.UserList:
        get_users_use_case: GetUsersUseCaseSync = self.container.resolve(GetUsersUseCaseSync)
        users: list[DomainUser] = get_users_use_case()

        return user_pb2.UserList(
            users=[
                GrpcUserHelper.from_domain(u)
                for u in users
            ]
        )
