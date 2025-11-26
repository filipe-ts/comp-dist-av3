const { buildSchema } = require('graphql');

const schema = buildSchema(`
  type User {
    id: Int
    nome: String
    idade: Int
  }

  type Music {
    id: Int
    nome: String
    artista: String
  }

  type Playlist {
    id: Int
    nome: String
    usuarioId: Int
  }

  type Query {
    getAllUsers: [User]
    getUser(id: Int!): User

    getAllMusics: [Music]

    getAllPlaylists(author: Int, has_song: Int): [Playlist]
    getPlaylist(id: Int!): Playlist
    getPlaylistsWithSong(songId: Int!): [Playlist]
    getSongsInPlaylist(id: Int!): [Music]
    getPlaylistByUserId(userId: Int!): [Playlist]
  }
`);

module.exports = schema;