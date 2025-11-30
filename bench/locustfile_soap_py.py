import re
import os
from pathlib import Path
import random
from locust import HttpUser, task, between


BASE_DIR = Path(os.path.abspath(__file__)).parent / "soap"

requests = ["musicas_de_playlist", "musicas", "usuarios", "playlists_do_autor", "playlists_com_musica"]
schemas = {}
headers = {"Content-Type": "application/xml"}

for request in requests:
    with open(BASE_DIR / f"py/{request}.xml", "r") as f:
        schemas[request] = f.read()

fill_schema = lambda text, key, value: re.sub(f"{{{{{key}}}}}", value, text)

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_usuarios(self):
        self.client.post("/soap/users", data=schemas["usuarios"], headers=headers)

    @task
    def get_musicas(self):
        self.client.post("/soap/songs", data=schemas["musicas"], headers=headers)

    @task
    def get_playlists_by_author(self):
        author_id = str(random.randint(0, 201))
        
        self.client.post(
            "/soap/playlists",
            data=fill_schema(schemas["playlists_do_autor"], "user_id", author_id),
            headers=headers
        )

    @task
    def get_playlist_songs(self):
        playlist_id = str(random.randint(0, 246))
        
        self.client.post(
            "/soap/playlists", 
            name="Músicas em playlist",
            data=fill_schema(schemas["musicas_de_playlist"], "playlist_id", playlist_id),
            headers=headers
        )

    @task
    def get_playlists_with_song(self):
        song_id = str(random.randint(0, 94))

        self.client.post(
            "/soap/playlists", 
            name="Playlists com música",
            data=fill_schema(schemas["playlists_com_musica"], "song_id", song_id),
            headers=headers
        )
