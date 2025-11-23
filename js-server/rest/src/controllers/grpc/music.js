const grpc = require('@grpc/grpc-js');
const { musicService } = require('../../services/music');
const { toGrpc } = require('../../helpers/types');

const handleError = (err, callback) => {
//   if (err.message === 'USER_NOT_FOUND') {
//     return callback({
//       code: grpc.status.NOT_FOUND,
//       details: 'User not found'
//     });
//   }
//   if (err.message === 'INVALID_AGE') {
//     return callback({
//       code: grpc.status.INVALID_ARGUMENT,
//       details: 'User must be 18 or older'
//     });
//   }
  return callback({
    code: grpc.status.INTERNAL,
    details: err.message
  });
};

const implementation = {
    GetAllMusic: async (call, callback) => {
        try {
            const music = await musicService.getAllMusic();
            console.log(music);
            callback(null, { musics: music.map(toGrpc) });
        } catch (err) {
            handleError(err, callback);
        }
    },

    GetMusic: async (call, callback) => {
        try {
            const music = await musicService.getMusicById(call.request.id);
            callback(null, { ...toGrpc(music) });
        } catch (err) {
            handleError(err, callback);
        }
    },
};

module.exports = implementation;
