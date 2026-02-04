import torch
import torch.nn.functional as F

from ai.config import EMBEDDINGS_PATH, TOP_K
from ai.track_features import FEATURES

print("Loading embeddings...")

data = torch.load(EMBEDDINGS_PATH, map_location="cpu")

embeddings = data["embeddings"]
track_ids = data["track_ids"]

embeddings = F.normalize(embeddings, dim=1)

print(f" Loaded {len(track_ids)} embeddings")


def has_track(track_id: str) -> bool:
    return track_id in track_ids


def recommend(
    track_id: str,
    top_k: int = TOP_K,
    mode: str = "base",
):
    if track_id not in track_ids:
        raise ValueError("Track ID not found")

    idx = track_ids.index(track_id)
    query = embeddings[idx].unsqueeze(0)

    similarities = torch.matmul(query, embeddings.T).squeeze(0)
    similarities[idx] = -1.0

    base_features = FEATURES.get(track_id, {})

    scores = []

    for i, sim in enumerate(similarities.tolist()):
        tid = track_ids[i]
        score = sim

        feats = FEATURES.get(tid, {})

        if mode == "energy":
            e1 = base_features.get("energy")
            e2 = feats.get("energy")
            if e1 is not None and e2 is not None:
                score += 0.15 * (1 - abs(e1 - e2))

        elif mode == "chill":
            score += feats.get("acousticness", 0) * 0.3
            score -= feats.get("energy", 0) * 0.2
            score -= feats.get("tempo", 120) / 300 * 0.2

        elif mode == "popular":
            pop = feats.get("popularity", 0)
            score *= (1 + pop / 100)

        scores.append((score, tid))

    scores.sort(reverse=True, key=lambda x: x[0])

    return [
        {"track_id": tid, "similarity": float(score)}
        for score, tid in scores[:top_k]
    ]
