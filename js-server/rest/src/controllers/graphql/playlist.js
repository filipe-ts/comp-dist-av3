const { playlistService } = require('../../services/playlist');

const convertTypes = (playlist) => {
  if (!playlist) return null;
  return {
    ...playlist,
    id: Number(playlist.id),
    usuario_id: Number(playlist.usuario_id)
  };
};

const resolvers = {
  getAllPlaylists: async () => {
    const playlists = await playlistService.getAllPlaylists();
    return playlists.map(convertTypes);
  },

  getPlaylist: async ({ id }) => {
    const playlist = await playlistService.getPlaylistById(id);
    return convertTypes(playlist);
  },

  getPlaylistsWithSong: async ({ songId }) => {
    const playlists = await playlistService.getPlaylistsWithSong(songId);
    return playlists.map(convertTypes);
  },

  getSongsInPlaylist: async ({ id }) => {
    const songs = await playlistService.getSongsInPlaylist(id);
    return songs.map(convertTypes);
  },

  getPlaylistByUserId: async ({ userId }) => {
    const playlists = await playlistService.getPlaylistByUserId(userId);
    return playlists.map(convertTypes);
  },
};

module.exports = resolvers;