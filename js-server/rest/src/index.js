const express = require('express');
const usuariosController = require('./controllers/user');
const musicasController = require('./controllers/music');
const playlistsController = require('./controllers/playlist');

const app = express();
const port = process.env.PORT || 3000;

BigInt.prototype.toJSON = function () {
  const int = Number.parseInt(this.toString());
  return int ?? this.toString();
};

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.use('/usuarios', usuariosController);
app.use('/musicas', musicasController);
app.use('/playlists', playlistsController);

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
