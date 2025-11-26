const { playlistService } = require('../../services/playlist');
const { convertTypes } = require('../../helpers/types');

const service = {
  PlaylistService: {
    PlaylistPort: {
      GetAllPlaylists: async function (args, callback) {
        try {
          const playlists = await playlistService.getAllPlaylists();
          callback(null, { playlists: playlists.map(convertTypes) });
        } catch (error) {
          callback({
            Fault: {
              Code: { Value: 'soap:Sender', Subcode: { value: 'rpc:BadArguments' } },
              Reason: { Text: error.message }
            }
          });
        }
      },
      GetPlaylist: async function (args, callback) {
        try {
          const id = parseInt(args.id, 10);
          const playlist = await playlistService.getPlaylistById(id);
          callback(null, convertTypes(playlist));
        } catch (error) {
          callback({
            Fault: {
              Code: { Value: 'soap:Sender', Subcode: { value: 'rpc:BadArguments' } },
              Reason: { Text: error.message }
            }
          });
        }
      },
      GetSongsInPlaylist: async function (args, callback) {
        try {
          console.log(args);
          const id = parseInt(args.id, 10);
          const songs = await playlistService.getSongsInPlaylist(id);
          callback(null, { musics: songs.map(convertTypes) });
        } catch (error) {
          callback({
            Fault: {
              Code: { Value: 'soap:Sender', Subcode: { value: 'rpc:BadArguments' } },
              Reason: { Text: error.message }
            }
          });
        }
      },
      GetPlaylistsByUser: async function (args, callback) {
        try {
          const userId = parseInt(args.userId, 10);
          const playlists = await playlistService.getPlaylistByUserId(userId);
          callback(null, { playlists: playlists.map(convertTypes) });
        } catch (error) {
          callback({
            Fault: {
              Code: { Value: 'soap:Sender', Subcode: { value: 'rpc:BadArguments' } },
              Reason: { Text: error.message }
            }
          });
        }
      },
      GetPlaylistsWithSong: async function (args, callback) {
        try {
          const songId = parseInt(args.songId, 10);
          const playlists = await playlistService.getPlaylistsWithSong(songId);
          callback(null, { playlists: playlists.map(convertTypes) });
        } catch (error) {
          callback({
            Fault: {
              Code: { Value: 'soap:Sender', Subcode: { value: 'rpc:BadArguments' } },
              Reason: { Text: error.message }
            }
          });
        }
      },
    }
  }
};

module.exports = service;
