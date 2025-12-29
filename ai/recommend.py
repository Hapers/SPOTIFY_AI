import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

EMBEDDINGS_PATH = "models/embeddings.pt"

class Recommender:
    def __init__(self):
        data = torch.load(EMBEDDINGS_PATH, weights_only=True)
        self.embeddings = data["embeddings"].numpy()
        self.track_ids = data["track_ids"]

    # ---------- CORE ----------
    def _similarity(self, query_vec):
        sims = cosine_similarity(
            query_vec.reshape(1, -1),
            self.embeddings
        )[0]
        return sims

    # ---------- MODES ----------
    def apply_mode(self, sims, mode, meta):
        if mode == "energy":
            return sims * (1 + meta["energy"])
        if mode == "popularity":
            return sims * (1 + meta["popularity"])
        return sims

    # ---------- TRACK ----------
    def recommend_from_track(self, track_index, top_n=10, mode="base"):
        query_vec = self.embeddings[track_index]
        sims = self._similarity(query_vec)

        meta = {
            "energy": 0.2,
            "popularity": 0.1
        }

        sims = self.apply_mode(sims, mode, meta)

        indices = np.argsort(sims)[::-1]
        indices = indices[indices != track_index][:top_n]

        return self._format(indices, sims)

    # ---------- PLAYLIST ----------
    def recommend_from_playlist(self, track_indices, top_n=20, mode="base"):
        playlist_vec = np.mean(self.embeddings[track_indices], axis=0)
        sims = self._similarity(playlist_vec)

        meta = {
            "energy": 0.2,
            "popularity": 0.1
        }

        sims = self.apply_mode(sims, mode, meta)

        indices = np.argsort(sims)[::-1]
        indices = [i for i in indices if i not in track_indices][:top_n]

        return self._format(indices, sims)

    # ---------- USER PROFILE ----------
    def recommend_from_profile(self, history_indices, top_n=20):
        profile_vec = np.mean(self.embeddings[history_indices], axis=0)
        sims = self._similarity(profile_vec)

        indices = np.argsort(sims)[::-1]
        indices = [i for i in indices if i not in history_indices][:top_n]

        return self._format(indices, sims)

    # ---------- FORMAT ----------
    def _format(self, indices, sims):
        return [
            {
                "track_id": self.track_ids[i],
                "similarity": float(sims[i])
            }
            for i in indices
        ]


if __name__ == "__main__":
    rec = Recommender()

    print("=== BASE TRACK ===")
    print(rec.recommend_from_track(0, mode="base"))

    print("=== ENERGY PLAYLIST ===")
    print(rec.recommend_from_playlist([0, 1, 2], mode="energy"))

    print("=== USER PROFILE ===")
    print(rec.recommend_from_profile([10, 11, 12]))
