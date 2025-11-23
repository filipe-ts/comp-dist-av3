const path = require('path');

const PROTOS = {
  USER: path.join(__dirname, './user.proto'),
  PLAYLIST: path.join(__dirname, './playlist.proto'),
  MUSIC: path.join(__dirname, './music.proto'),
};

module.exports = {
  PROTOS,
};
