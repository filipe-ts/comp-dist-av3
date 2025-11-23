const express = require('express');
const prisma_client = require('../prisma_client');

const router = express.Router();
const prisma = prisma_client();

router.get('/', async (req, res) => {
  try {
    const { has_song } = req.query;
    let playlists;
    if (has_song !== undefined) {
      const songId = parseInt(has_song, 10);
      playlists = await prisma.playlists.findMany({
        where: {
          musicas_em_playlist: {
            some: {
              musica_id: songId,
            },
          },
        },
      });
    } else {
      playlists = await prisma.playlists.findMany();
    }
    res.json(playlists);
  } catch (error) {
    console.error('Error fetching playlists:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const playlists = await prisma.playlists.findUnique({
    where: { id: parseInt(id, 10) },
  });
    if (playlists) {
      res.json(playlists);
    } else {
      res.status(404).json({ error: 'playlists not found' });
    }
  } catch (error) {
    console.error('Error fetching playlists:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/:id/musicas', async (req, res) => {
  const { id } = req.params;
  try {
    const musicasInPlaylist = await prisma.musicas_em_playlist.findMany({
      where: { playlist_id: parseInt(id, 10) },
      include: { musicas: true },
    });
    const musicas = musicasInPlaylist.map((entry) => entry.musicas);
    res.json(musicas);
  } catch (error) {
    console.error('Error fetching musicas for playlist:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

module.exports = router;
