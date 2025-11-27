const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const { PROTOS } = require('./protos/protos');
const userController = require('./controllers/grpc/user');
const musicController = require('./controllers/grpc/music');
const playlistController = require('./controllers/grpc/playlist');

const packageDefinition = {
  user: protoLoader.loadSync(PROTOS.USER, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
  }),
  music: protoLoader.loadSync(PROTOS.MUSIC, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
  }),
  playlist: protoLoader.loadSync(PROTOS.PLAYLIST, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
  }),
};

const userProto = grpc.loadPackageDefinition(packageDefinition.user).user_package;
const musicProto = grpc.loadPackageDefinition(packageDefinition.music).music_package;
const playlistProto = grpc.loadPackageDefinition(packageDefinition.playlist).playlist_package;

function main() {
  const server = new grpc.Server();

  server.addService(userProto.UserService.service, userController);
  server.addService(musicProto.MusicService.service, musicController);
  server.addService(playlistProto.PlaylistService.service, playlistController);

  const address = '127.0.0.1:50051';
  server.bindAsync(address, grpc.ServerCredentials.createInsecure(), () => {
    console.log(`gRPC Server running at ${address}`);
  });
}

main();
