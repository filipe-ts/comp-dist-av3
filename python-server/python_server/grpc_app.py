from python_server.adapters.grpc.grpcio.app import start_grpc_server, create_grpc_container


if __name__ == "__main__":
    container = create_grpc_container()
    start_grpc_server(container)
