const {
    getMusicById,
    getAllMusic,
} = require('../repositories/music');

class musicService {
    constructor() {
        this.getMusicById = async (id) => {
            return await getMusicById(id);
        };

        this.getAllMusic = async () => {
            return await getAllMusic();
        };
    }
}

module.exports = {
    musicService: new musicService(),
};
