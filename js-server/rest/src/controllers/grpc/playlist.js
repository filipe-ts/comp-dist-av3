const grpc = require('@grpc/grpc-js');
const { playlistService } = require('../../services/playlist');

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

const convertTypes = (data) => {
    if (!data) return null;
    return {
        ...data,
        id: Number(data.id),
        usuario_id: Number(data.usuario_id),
    }
}

const implementation = {
    GetAllPlaylists: async (call, callback) => {
        try {
            const playlists = await playlistService.getAllPlaylists();
            callback(null, { playlists: playlists.map(convertTypes) });
        } catch (err) {
            handleError(err, callback);
        }
    },

    GetPlaylist: async (call, callback) => {
        try {
            const playlist = await playlistService.getPlaylistById(call.request.id);
            callback(null, { ...convertTypes(playlist) });
        } catch (err) {
            handleError(err, callback);
        }
    },

    GetSongsInPlaylist: async (call, callback) => {
        try {
            const songs = await playlistService.getSongsInPlaylist(call.request.id);
            callback(null, { musics: songs.map(convertTypes) });
        } catch (err) {
            handleError(err, callback);
        }
    },

    GetPlaylistsByUser: async (call, callback) => {
        try {
            const playlists = await playlistService.getPlaylistByUserId(call.request.id);
            callback(null, { playlists: playlists.map(convertTypes) });
        } catch (err) {
            handleError(err, callback);
        }
    },

    GetPlaylistsWithSong: async (call, callback) => {
        try {
            const playlists = await playlistService.getPlaylistsWithSong(call.request.id);
            callback(null, { playlists: playlists.map(convertTypes) });
        } catch (err) {
            handleError(err, callback);
        }
    },
};

module.exports = implementation;
