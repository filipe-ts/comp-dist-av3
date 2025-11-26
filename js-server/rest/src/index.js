const express = require('express');
const soap = require('soap');
const fs = require('fs');

const usuariosController = require('./controllers/user');
const musicasController = require('./controllers/music');
const playlistsController = require('./controllers/playlist');

const app = express();
const port = process.env.PORT || 3000;

// REST
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

// SOAP
const userWsdl = fs.readFileSync('./soap/user.wsdl', 'utf8');
const userControllerSoap = require('./controllers/soap/user');

const musicWsdl = fs.readFileSync('./soap/music.wsdl', 'utf8');
const musicControllerSoap = require('./controllers/soap/music');

const playlistWsdl = fs.readFileSync('./soap/playlist.wsdl', 'utf8');
const playlistControllerSoap = require('./controllers/soap/playlist');

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);

  soap.listen(app, '/soap/usuarios', userControllerSoap, userWsdl, () => {
    console.log(`SOAP User service initialized at http://localhost:${port}/soap/usuarios`);
  });
  soap.listen(app, '/soap/musicas', musicControllerSoap, musicWsdl, () => {
    console.log(`SOAP Music service initialized at http://localhost:${port}/soap/musicas`);
  });
  soap.listen(app, '/soap/playlists', playlistControllerSoap, playlistWsdl, () => {
    console.log(`SOAP Playlist service initialized at http://localhost:${port}/soap/playlists`);
  });
});
