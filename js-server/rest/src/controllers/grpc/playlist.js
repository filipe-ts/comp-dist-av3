const grpc = require('@grpc/grpc-js');
const { playlistService } = require('../../services/playlist');
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
    GetAllPlaylists: async (call, callback) => {
        try {
            const playlists = await playlistService.getAllPlaylists();
            callback(null, { playlists: playlists.map(toGrpc) });
        } catch (err) {
            handleError(err, callback);
        }
    },

    GetPlaylist: async (call, callback) => {
        try {
            const playlist = await playlistService.getPlaylistById(call.request.id);
            callback(null, { ...toGrpc(playlist) });
        } catch (err) {
            handleError(err, callback);
        }
    },

    GetSongsInPlaylist: async (call, callback) => {
        try {
            const songs = await playlistService.getSongsInPlaylist(call.request.id);
            callback(null, { musics: songs.map(toGrpc) });
        } catch (err) {
            handleError(err, callback);
        }
    },

    GetPlaylistsByUser: async (call, callback) => {
        try {
            const playlists = await playlistService.getPlaylistByUserId(call.request.userId);
            callback(null, { playlists: playlists.map(toGrpc) });
        } catch (err) {
            handleError(err, callback);
        }
    },

    GetPlaylistsWithSong: async (call, callback) => {
        try {
            const playlists = await playlistService.getPlaylistsWithSong(call.request.songId);
            callback(null, { playlists: playlists.map(toGrpc) });
        } catch (err) {
            handleError(err, callback);
        }
    },
};

module.exports = implementation;
