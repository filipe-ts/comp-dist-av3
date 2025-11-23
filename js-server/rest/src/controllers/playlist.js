const express = require('express');
const { playlistService } = require('../services/playlist');

const router = express.Router();

router.get('/', async (req, res) => {
  try {
    const { has_song, author } = req.query;
    const playlists = await playlistService.getAllPlaylists(author, has_song);
    res.json(playlists);
  } catch (error) {
    console.error('Error fetching playlists:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const playlists = await playlistService.getPlaylistById(id);
    res.json(playlists);
  } catch (error) {
    console.error('Error fetching playlists:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/:id/musicas', async (req, res) => {
  const { id } = req.params;
  // try {
  //   const musicasInPlaylist = await prisma.musicas_em_playlist.findMany({
  //     where: { playlist_id: parseInt(id, 10) },
  //     include: { musicas: true },
  //   });
  //   const musicas = musicasInPlaylist.map((entry) => entry.musicas);
  //   res.json(musicas);
  try {
    const musicas = await playlistService.getSongsInPlaylist(id);
    res.json(musicas);
  } catch (error) {
    console.error('Error fetching musicas for playlist:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

module.exports = router;
