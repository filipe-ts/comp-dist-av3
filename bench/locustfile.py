import random
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_usuarios(self):
        self.client.get("/usuarios")

    @task
    def get_musicas(self):
        self.client.get("/musicas")

    @task
    def get_playlists_by_author(self):
        author_id = random.randint(0, 201)
        
        self.client.get(
            f"/playlists?author={author_id}", 
            name="Playlists de usuário"
        )

    @task
    def get_playlist_songs(self):
        playlist_id = random.randint(0, 246)
        
        self.client.get(
            f"/playlists/{playlist_id}/musicas", 
            name="Músicas em playlist"
        )

    @task
    def get_playlists_with_song(self):
        song_id = random.randint(0, 94)
        
        self.client.get(
            f"/playlists?has_song={song_id}", 
            name="Playlists com música"
        )
