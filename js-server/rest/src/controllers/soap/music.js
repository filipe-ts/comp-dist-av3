const { musicService } = require('../../services/music');
const { convertTypes } = require('../../helpers/types');

const service = {
  MusicService: {
    MusicPort: {
      GetMusic: async function (args, callback) {
        try {
          const id = parseInt(args.id, 10);
          const music = await musicService.getMusicById(id);

          callback(null, convertTypes(music));
        } catch (error) {
          callback({
            Fault: {
              Code: { Value: 'soap:Sender', Subcode: { value: 'rpc:BadArguments' } },
              Reason: { Text: error.message }
            }
          });
        }
      },
      GetAllMusic: async function (args, callback) {
        try {
          const musics = await musicService.getAllMusic();

          callback(null, { musics: musics.map(convertTypes) });
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
