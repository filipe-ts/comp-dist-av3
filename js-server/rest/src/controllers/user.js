const express = require('express');
const { prisma_client } = require('../prisma_client');

const router = express.Router();
const prisma = prisma_client();

router.get('/', async (req, res) => {
  try {
    const usuarios = await prisma.usuarios.findMany();
    res.json(usuarios);
  } catch (error) {
    console.error('Error fetching usuarios:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const usuarios = await prisma.usuarios.findUnique({
    where: { id: parseInt(id, 10) },
  });
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
    const playlists = await prisma.playlists.findMany({
      where: { usuarioId: parseInt(id, 10) },
    });
    res.json(playlists);
  } catch (error) {
    console.error('Error fetching playlists for usuario:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

module.exports = router;
