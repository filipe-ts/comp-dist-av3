const { userService } = require('../../services/user');

const convertTypes = (user) => {
  if (!user) return null;
  return {
    ...user,
    id: Number(user.id),
    idade: Number(user.idade)
  };
};

const resolvers = {
  getAllUsers: async () => {
    const users = await userService.getAllUsers();
    return users.map(convertTypes);
  },

  getUser: async ({ id }) => {
    const user = await userService.getUserById(id);
    return convertTypes(user);
  },
};

module.exports = resolvers;