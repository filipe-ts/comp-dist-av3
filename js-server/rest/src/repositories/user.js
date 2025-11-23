const prisma_client = require('../prisma_client');

const prisma = prisma_client();

const getAllUsers = async () => {
  return await prisma.usuarios.findMany();
};

const getUserById = async (id) => {
  return await prisma.usuarios.findUnique({
    where: { id: parseInt(id, 10) },
  });
};

const getUserPlaylists = async (userId) => {
  return await prisma.playlists.findMany({
    where: { usuarioId: parseInt(userId, 10) },
  });
};

module.exports = {
  getAllUsers,
  getUserById,
  getUserPlaylists,
};
