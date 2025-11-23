const prisma_client = require('../prisma_client');

const prisma = prisma_client();

const getAllMusic = async () => {
  return await prisma.musicas.findMany();
};

const getMusicById = async (id) => {
  return await prisma.musicas.findUnique({
    where: { id: parseInt(id, 10) },
  });
};

module.exports = {
  getAllMusic,
  getMusicById,
};
