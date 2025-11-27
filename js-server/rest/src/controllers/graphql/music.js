const { musicService } = require('../../services/music');

const convertTypes = (music) => {
  if (!music) return null;
  return {
    ...music,
    id: Number(music.id),
    artista: String(music.artista)
  };
};

const resolvers = {
  getAllMusics: async () => {
    const musics = await musicService.getAllMusic();
    return musics.map(convertTypes);
  },
};

module.exports = resolvers;