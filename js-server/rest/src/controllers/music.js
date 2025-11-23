const express = require('express');
const { prisma_client } = require('../prisma_client');

const router = express.Router();
const prisma = prisma_client();

router.get('/', async (req, res) => {
  try {
    const musicas = await prisma.musicas.findMany();
    res.json(musicas);
  } catch (error) {
    console.error('Error fetching musicas:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const musicas = await prisma.musicas.findUnique({
    where: { id: parseInt(id, 10) },
  });
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

router.post('/', express.json(), async (req, res) => {
  const { nome, idade } = req.body;
  const musicas = { nome, idade: parseInt(idade, 10) };
  const createdmusicas = await prisma.musicas.create({
    data: musicas,
  });
  res.status(201).json(createdmusicas);
});

router.put('/:id', express.json(), async (req, res) => {
  const { id } = req.params;
  try {
    await prisma.musicas.findUniqueOrThrow({
      where: { id: parseInt(id, 10) },
    });
    const { nome, idade } = req.body;
    const updatedmusicas = await prisma.musicas.update({
      where: { id: parseInt(id, 10) },
      data: { nome, idade: parseInt(idade, 10) },
    });
    res.json(updatedmusicas);
  } catch (error) {
    return res.status(404).json({ error: 'musicas not found' });
  }
});

router.delete('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    await prisma.musicas.findUniqueOrThrow({
      where: { id: parseInt(id, 10) },
    });
    await prisma.musicas.delete({
      where: { id: parseInt(id, 10) },
    });
    res.status(204).send();
  } catch (error) {
    return res.status(404).json({ error: 'musicas not found' });
  }
});

module.exports = router;
