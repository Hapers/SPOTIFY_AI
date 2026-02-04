from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone

# Импортируй свои функции (убедись, что пути правильные)
from backend.spotify_api import search_tracks, get_track, create_spotify_playlist
from ai.recommend import recommend, has_track
from backend.auth import router as auth_router
from backend.history_store import add_history, get_history

app = FastAPI(title="Spotify AI")

# --- CORS (ОЧЕНЬ ВАЖНО: Должно быть в самом верху) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://bradley-semifine-amada.ngrok-free.dev" # Добавь это
    ], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

# --- Модели ---
class PlaylistRequest(BaseModel):
    name: str
    track_ids: List[str]
    token: str

class RecommendRequest(BaseModel):
    track_id: str
    top_k: int = 10
    mode: str = "base"
    user_id: Optional[str] = "demo_user"

# --- Эндпоинты ---

@app.get("/search")
def search(q: str, limit: int = 10):
    try:
        return search_tracks(q, limit)
    except Exception as e:
        print(f"Search Error: {e}")
        raise HTTPException(status_code=500, detail="Spotify Search Failed")

@app.get("/track/{track_id}")
def track(track_id: str):
    if not track_id or track_id == "undefined":
        raise HTTPException(status_code=400, detail="Invalid track ID")
    return get_track(track_id)

@app.get("/history")
def history(user_id: str = "demo_user"): # Параметр уже есть, фронтенд просто должен его присылать
    try:
        data = get_history(user_id)
        return data if data else []
    except Exception as e:
        print(f"History Error: {e}")
        return []

@app.post("/recommend")
def recommend_tracks(payload: RecommendRequest):
    # Проверка наличия трека в базе AI
    if not has_track(payload.track_id):
        raise HTTPException(status_code=404, detail="Track not found in AI database")

    try:
        # 1. ЗАПРОС С ЗАПАСОМ: Запрашиваем на 5 треков больше (например, 15 вместо 10)
        # Это гарантирует, что даже после фильтрации битых ссылок у нас останется нужное количество
        fetch_limit = payload.top_k + 5
        raw_recs = recommend(payload.track_id, fetch_limit, payload.mode)
        
        try:
            source_info = get_track(payload.track_id)
        except Exception:
            source_info = {"name": "Unknown Source", "image": "", "artist": "Unknown"}

        full_recs = []
        for r in raw_recs:
            if len(full_recs) >= payload.top_k:
                break
            try:
                tid = r["track_id"] if isinstance(r, dict) else r
                if tid == payload.track_id:
                    continue

                t_data = get_track(tid)
                
                # УЛУЧШЕННАЯ ПРОВЕРКА: 
                # Если нет имени или картинки — это "битый" трек, пропускаем его
                if not t_data or not t_data.get("name") or not t_data.get("image"):
                    continue

                full_recs.append({
                    "track_id": tid,
                    "id": tid,
                    "name": t_data["name"],
                    "artist": t_data.get("artist", "Unknown"),
                    "image": t_data["image"],
                    "spotify_url": t_data.get("spotify_url", "#")
                })
            except Exception:
                continue 

        # Сохраняем в историю MongoDB (используя ID пользователя из payload)
        add_history(
            user_id=payload.user_id,
            source_track_id=payload.track_id,
            source_track_name=source_info.get("name", "Unknown"),
            source_track_image=source_info.get("image", ""),
            mode=payload.mode, # Например: Chill, Energy или Popular
            recommended=full_recs
        )

        return {
            "track_id": payload.track_id,
            "recommendations": full_recs, 
        }

    except Exception as e:
        print(f"Critical Recommendation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/create-playlist")
async def make_playlist(payload: PlaylistRequest):
    try:
        url = create_spotify_playlist(payload.token, payload.track_ids, payload.name)
        return {"playlist_url": url}
    except Exception as e:
        print(f"Playlist API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))