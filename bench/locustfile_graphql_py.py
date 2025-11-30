import random
from locust import HttpUser, task, between

# --- DEFINIÇÃO DAS QUERIES (Baseadas no seu schema.js) ---

# 1. Lista todos os usuários
# Schema: getAllUsers: [User]
Q_GET_USERS = """
query GetUsers {
  getUsers {
    id
    idade
    nome
    createdAt
  }
}
"""

# 2. Lista todas as músicas
# Schema: getAllMusics: [Music]
Q_GET_MUSICS = """
query GetSongs {
  getSongs {
    artista
    createdAt
    id
    nome
  }
}
"""

# 3. Playlists de um autor específico
# Schema: getPlaylistByUserId(userId: Int!): [Playlist]
Q_PLAYLISTS_BY_USER = """
query GetPlaylistByUserId($uid: Int!) {
  getPlaylistsByUserId(userId: $uid) {
    createdAt
    id
    nome
    usuarioId
  }
}
"""

# 4. Músicas dentro de uma playlist
# Schema: getSongsInPlaylist(id: Int!): [Music]
Q_SONGS_IN_PLAYLIST = """
query GetSongsInPlaylist($pid: Int!) {
  getPlaylistById(id_: $pid) {
    createdAt
    id
    nome
    usuarioId
  }
}
"""

# 5. Playlists que contêm uma música específica
# Schema: getPlaylistsWithSong(songId: Int!): [Playlist]
Q_PLAYLISTS_WITH_SONG = """
query GetPlaylistsWithSong($sid: Int!) {
  getPlaylistsBySongId(songId: $sid) {
    createdAt
    id
    nome
    usuarioId
  }
}
"""

class GraphQLUser(HttpUser):
    wait_time = between(1, 3)

    def post_graphql(self, query, operation_name, variables=None):
        """
        Envia a requisição POST formatada para GraphQL.
        Usa 'name' para garantir que o relatório do Locust fique legível.
        """
        payload = {
            "query": query,
            "operationName": operation_name,
            "variables": variables or {}
        }
        
        self.client.post(
            "/graphql",
            json=payload,
            name=operation_name # Agrupa estatísticas pelo nome da operação
        )

    @task
    def get_users(self):
        self.post_graphql(
            query=Q_GET_USERS,
            operation_name="GetAllUsers"
        )

    @task
    def get_musics(self):
        self.post_graphql(
            query=Q_GET_MUSICS,
            operation_name="GetAllMusics"
        )

    @task
    def get_playlists_by_author(self):
        # Constraint: 0 <= author_id <= 201
        author_id = random.randint(0, 201)
        
        self.post_graphql(
            query=Q_PLAYLISTS_BY_USER,
            operation_name="GetPlaylistByUserId",
            variables={"uid": author_id}
        )

    @task
    def get_playlist_songs(self):
        # Constraint: 0 <= playlist_id <= 246
        playlist_id = random.randint(0, 246)
        
        # Nota: No seu schema o argumento é 'id', não 'playlistId'
        self.post_graphql(
            query=Q_SONGS_IN_PLAYLIST,
            operation_name="GetSongsInPlaylist",
            variables={"pid": playlist_id}
        )

    @task
    def get_playlists_with_song(self):
        # Constraint: 0 <= song_id <= 94
        song_id = random.randint(0, 94)
        
        self.post_graphql(
            query=Q_PLAYLISTS_WITH_SONG,
            operation_name="GetPlaylistsWithSong",
            variables={"sid": song_id}
        )
