from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from spotify_api import search_tracks, get_track
from ai.recommend import recommend, has_track

app = FastAPI(title="Spotify AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendRequest(BaseModel):
    track_id: str
    top_k: int = 10


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/search")
def search(q: str, limit: int = 10):
    return search_tracks(q, limit)


@app.get("/track/{track_id}")
def track(track_id: str):
    return get_track(track_id)


@app.post("/recommend")
def recommend_tracks(payload: RecommendRequest):
    if not has_track(payload.track_id):
        return {"recommendations": []}

    recs = recommend(payload.track_id, payload.top_k)
    return {"recommendations": recs}
