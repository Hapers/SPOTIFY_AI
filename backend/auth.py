import os
import base64
import requests
import urllib.parse
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth")

# Переменные окружения
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI") # Твой https://...ngrok-free.dev/auth/callback
FRONTEND_URL = os.getenv("FRONTEND_URL")

# Реальные эндпоинты Spotify
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

SCOPES = "user-read-email user-read-private playlist-modify-public playlist-modify-private"

@router.get("/login")
def login():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope": SCOPES,
        "redirect_uri": REDIRECT_URI,
        "show_dialog": "true"
    }
    
    # Формируем корректную ссылку на настоящую страницу логина Spotify
    url = f"{SPOTIFY_AUTH_URL}?" + urllib.parse.urlencode(params)
    return RedirectResponse(url)

@router.get("/callback")
def callback(code: str):
    # Кодируем credentials для авторизации
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()

    # Запрос на обмен кода на реальный токен
    response = requests.post(
        SPOTIFY_TOKEN_URL,
        headers={
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
    )

    data = response.json()
    
    if "access_token" not in data:
        # Если Spotify вернул ошибку, выводим её для отладки
        return {"error": "Failed to get token", "details": data}

    token = data["access_token"]

    # Перенаправляем пользователя на фронтенд с токеном
    return RedirectResponse(
        f"{FRONTEND_URL}/login-success?token={token}"
    )

print("🔥 Auth router fully fixed and loaded")