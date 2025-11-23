const express = require('express');
const { musicService } = require('../services/music');

const router = express.Router();

router.get('/', async (req, res) => {
  try {
    const musicas = await musicService.getAllMusic();
    res.json(musicas);
  } catch (error) {
    console.error('Error fetching musicas:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const musicas = await musicService.getMusicById(id);
    if (musicas) {
      res.json(musicas);
    } else {
      res.status(404).json({ error: 'musicas not found' });
    }
  } catch (error) {
    console.error('Error fetching musicas:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

module.exports = router;
