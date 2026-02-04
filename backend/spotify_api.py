import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE = "https://api.spotify.com/v1"


def get_token():
    auth = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    encoded = base64.b64encode(auth.encode()).decode()

    r = requests.post(
        TOKEN_URL,
        headers={"Authorization": f"Basic {encoded}"},
        data={"grant_type": "client_credentials"},
    )
    r.raise_for_status()
    return r.json()["access_token"]


def auth_headers():
    return {"Authorization": f"Bearer {get_token()}"}


def search_tracks(query: str, limit: int = 10):
    r = requests.get(
        f"{API_BASE}/search",
        headers=auth_headers(),
        params={"q": query, "type": "track", "limit": limit},
    )
    r.raise_for_status()

    tracks = []
    for t in r.json()["tracks"]["items"]:
        tracks.append({
            "track_id": t["id"],
            "name": t["name"],
            "artist": ", ".join(a["name"] for a in t["artists"]),
            "image": t["album"]["images"][0]["url"] if t["album"]["images"] else None,
        })
    return tracks


def get_track(track_id: str):
    r = requests.get(
        f"{API_BASE}/tracks/{track_id}",
        headers=auth_headers()
    )
    r.raise_for_status()
    t = r.json()

    return {
        "track_id": t["id"],
        "name": t["name"],
        "artist": ", ".join(a["name"] for a in t["artists"]),
        "image": t["album"]["images"][0]["url"] if t["album"]["images"] else None,
        "spotify_url": t["external_urls"]["spotify"],
    }

def create_spotify_playlist(user_token: str, track_ids: list, playlist_name: str = "AI Recommendations"):

    headers = {"Authorization": f"Bearer {user_token}"}

    user_res = requests.get("https://api.spotify.com/v1/me", headers=headers)
    user_res.raise_for_status()
    user_id = user_res.json()["id"]

    create_res = requests.post(
        f"https://api.spotify.com/v1/users/{user_id}/playlists",
        headers=headers,
        json={
            "name": playlist_name,
            "description": "Created by Spotify AI Assistant",
            "public": False
        }
    )
    create_res.raise_for_status()
    playlist_data = create_res.json()
    playlist_id = playlist_data["id"]
    playlist_url = playlist_data["external_urls"]["spotify"]

    uris = [f"spotify:track:{tid}" for tid in track_ids]
    
    add_res = requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers,
        json={"uris": uris}
    )
    add_res.raise_for_status()
    
    return playlist_url