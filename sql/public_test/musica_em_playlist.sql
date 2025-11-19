DROP TABLE IF EXISTS public_test.musica_em_playlist;

CREATE TABLE IF NOT EXISTS public_test.musica_em_playlist (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    playlist_id BIGINT REFERENCES public_test.playlists(id),
    musica_id BIGINT REFERENCES public_test.musicas(id)
);

CREATE INDEX IF NOT EXISTS idx_musica_em_playlist_playlist_id
    ON public_test.musica_em_playlist (playlist_id);

CREATE INDEX IF NOT EXISTS idx_musica_em_playlist_musica_id
    ON public_test.musica_em_playlist (musica_id);

INSERT INTO public_test.musica_em_playlist (playlist_id, musica_id)
WITH playlist_sizes AS (
    SELECT id AS playlist_id,
           (3 + floor(random() * 28))::int AS song_count
    FROM public_test.playlists
    ORDER BY id
    LIMIT 200
)
SELECT
    p.playlist_id,
    m.id AS musica_id
FROM playlist_sizes p
CROSS JOIN LATERAL (
    SELECT id
    FROM public_test.musicas
    ORDER BY random()
    LIMIT p.song_count
) m;
