const { getUserById, getAllUsers } = require('../repositories/user');

class userService {
    constructor() {
        this.getUserById = async (id) => {
            return await getUserById(id);
        }
        this.getAllUsers = async () => {
            return await getAllUsers();
        }
    }
}

module.exports = {
    userService: new userService()
};
