const prisma_client = require('../prisma_client');

const prisma = prisma_client();

const getAllPlaylists = async (author, has_song) => {
    const query = {};
    if (author !== undefined) {
      query.usuario_id = parseInt(author, 10);
    }
    if (has_song !== undefined) {
      const songId = parseInt(has_song, 10);
      query.musicas_em_playlist = {
        some: {
          musica_id: songId,
        },
      };
    }

    const playlists = await prisma.playlists.findMany({
      where: query,
    });
  return playlists;
};

const getPlaylistsWithSong = async (songId) => {
  return await prisma.playlists.findMany({
    where: {
      musicas_em_playlist: {
        some: {
          musica_id: songId,
        },
      },
    },
  });
};

const getPlaylistById = async (id) => {
  return await prisma.playlists.findUnique({
    where: { id: parseInt(id, 10) },
  });
};

const getSongsInPlaylist = async (playlistId) => {
  const playlist = await prisma.playlists.findUnique({
    where: { id: parseInt(playlistId, 10) },
    include: { musicas_em_playlist: { include: { musicas: true } } },
  });
  return playlist ? playlist.musicas_em_playlist.map(item => item.musicas) : [];
};

const getPlaylistByUserId = async (userId) => {
  return await prisma.playlists.findMany({
    where: { usuario_id: parseInt(userId, 10) },
  });
};

module.exports = {
  getAllPlaylists,
  getPlaylistById,
  getPlaylistsWithSong,
  getSongsInPlaylist,
  getPlaylistByUserId,
};
