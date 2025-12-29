import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri="http://localhost:8000/callback",
        scope="user-read-private"
    )
)

def get_track_genres(track_id):
    track = sp.track(track_id)
    artist_id = track["artists"][0]["id"]

    artist = sp.artist(artist_id)
    return artist["genres"]


def filter_by_genre(candidates, allowed_genres):
    """
    candidates: list of {track_id, similarity}
    allowed_genres: list[str]
    """
    filtered = []

    for item in candidates:
        genres = get_track_genres(item["track_id"])

        if any(g in genres for g in allowed_genres):
            filtered.append(item)

    return filtered
