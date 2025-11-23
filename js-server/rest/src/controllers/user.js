const express = require('express');
const { userService } = require('../services/user');

const router = express.Router();

router.get('/', async (req, res) => {
  try {
    const usuarios = await userService.getAllUsers();
    res.json(usuarios);
  } catch (error) {
    console.error('Error fetching usuarios:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const usuarios = await userService.getUserById(id);
    if (usuarios) {
      res.json(usuarios);
    } else {
      res.status(404).json({ error: 'usuarios not found' });
    }
  } catch (error) {
    console.error('Error fetching usuarios:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/:id/playlists', async (req, res) => {
  const { id } = req.params;
  try {
    const playlists = await userService.getUserPlaylists(id);
    res.json(playlists);
  } catch (error) {
    console.error('Error fetching playlists for usuario:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

module.exports = router;
