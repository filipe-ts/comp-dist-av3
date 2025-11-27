const grpc = require('@grpc/grpc-js');
const { userService } = require('../../services/user');
const { convertTypes } = require('../../helpers/types');

const handleError = (err, callback) => {
//   if (err.message === 'USER_NOT_FOUND') {
//     return callback({
//       code: grpc.status.NOT_FOUND,
//       details: 'User not found'
//     });
//   }
//   if (err.message === 'INVALID_AGE') {
//     return callback({
//       code: grpc.status.INVALID_ARGUMENT,
//       details: 'User must be 18 or older'
//     });
//   }
  return callback({
    code: grpc.status.INTERNAL,
    details: err.message
  });
};

const implementation = {
  GetAllUsers: async (call, callback) => {
    try {
      const users = await userService.getAllUsers();
      callback(null, { users: users.map(convertTypes) });
    } catch (err) {
      handleError(err, callback);
    }
  },

  GetUser: async (call, callback) => {
    try {
      const user = await userService.getUserById(call.request.id);
      callback(null, { ...convertTypes(user) });
    } catch (err) {
      handleError(err, callback);
    }
  },
};

module.exports = implementation;
