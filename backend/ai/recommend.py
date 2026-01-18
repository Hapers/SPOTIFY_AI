import torch
import torch.nn.functional as F

from config import (
    EMBEDDINGS_PATH,
    AUTOENCODER_PATH,
    DEVICE,
    TOP_K,
)

# =========================
# LOAD DATA ON STARTUP
# =========================

print("🔄 Loading embeddings...")
def has_track(track_id: str) -> bool:
    exists = track_id in TRACK_INDEX
    print(f"🔍 has_track({track_id}) = {exists}")
    return exists
data = torch.load(EMBEDDINGS_PATH, map_location="cpu")
embeddings = data["embeddings"]          # Tensor [N, embedding_dim]
track_ids = data["track_ids"]             # List[str]

# Normalize embeddings for cosine similarity
embeddings = F.normalize(embeddings, dim=1)

print(f"✅ Loaded {len(track_ids)} embeddings")

# =========================
# RECOMMEND FUNCTION
# =========================
def has_track(track_id: str) -> bool:
    return track_id in track_ids


def recommend_tracks(track_id: str, top_k: int = 10):
    # твоя логика с embeddings
    return {
        "track_id": track_id,
        "recommendations": results
    }

def recommend(track_id: str, top_k: int = TOP_K):
    """
    Recommend similar tracks based on embedding cosine similarity
    """

    if track_id not in track_ids:
        raise ValueError("Track ID not found in dataset")

    # Index of query track
    idx = track_ids.index(track_id)

    query_embedding = embeddings[idx].unsqueeze(0)  # [1, D]

    # Cosine similarity with all tracks
    similarities = torch.matmul(query_embedding, embeddings.T).squeeze(0)

    # Exclude the same track
    similarities[idx] = -1.0

    # Top-K most similar
    values, indices = torch.topk(similarities, top_k)

    results = []
    for score, i in zip(values.tolist(), indices.tolist()):
        results.append({
            "track_id": track_ids[i],
            "similarity": round(score, 4)
        })

    return results