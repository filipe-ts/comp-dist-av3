const {
  getAllPlaylists,
  getPlaylistById,
  getPlaylistsWithSong,
  getSongsInPlaylist,
  getPlaylistByUserId,
} = require('../repositories/playlist');

class playlistService {
    constructor() {
        this.getAllPlaylists = async (author, has_song) => {
            return await getAllPlaylists(author, has_song);
        };

        this.getPlaylistById = async (id) => {
            return await getPlaylistById(id);
        };

        this.getPlaylistsWithSong = async (songId) => {
            return await getPlaylistsWithSong(songId);
        };

        this.getSongsInPlaylist = async (playlistId) => {
            return await getSongsInPlaylist(playlistId);
        };

        this.getPlaylistByUserId = async (userId) => {
            return await getPlaylistByUserId(userId);
        };
    }
}

module.exports = {
    playlistService: new playlistService(),
};
