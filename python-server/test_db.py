from psycopg_pool import ConnectionPool

from python_server.config.settings import Settings

settings = Settings()
pool = ConnectionPool(settings.db_uri_unwrapped, min_size=0, max_size=5)

with pool.connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        print(cur.fetchone())
