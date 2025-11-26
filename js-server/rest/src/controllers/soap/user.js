const { userService } = require('../../services/user');
const { convertTypes } = require('../../helpers/types');

const service = {
  UserService: {
    UserPort: {
      GetUser: async function (args, callback) {
        try {
          const id = parseInt(args.id, 10);
          const user = await userService.getUserById(id);

          callback(null, convertTypes(user));
        } catch (error) {
          callback({
            Fault: {
              Code: { Value: 'soap:Sender', Subcode: { value: 'rpc:BadArguments' } },
              Reason: { Text: error.message }
            }
          });
        }
      },
      GetAllUsers: async function (args, callback) {
        try {
          const users = await userService.getAllUsers();

          callback(null, users.map(convertTypes));
        } catch (error) {
          callback({
            Fault: {
              Code: { Value: 'soap:Sender', Subcode: { value: 'rpc:BadArguments' } },
              Reason: { Text: error.message }
            }
          });
        }
      },
    }
  }
};

module.exports = service;
