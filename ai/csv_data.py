import pandas as pd
import torch

FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "valence",
    "tempo",
    "loudness",
    "acousticness",
    "instrumentalness",
    "speechiness",
    "liveness",
    "popularity"
]

def load_spotify_csv(path, limit=None):
    df = pd.read_csv(path)

    # Проверка фич
    missing = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    if limit:
        df = df.sample(limit, random_state=42)

    df = df.dropna(subset=FEATURE_COLUMNS)

    features = torch.tensor(
        df[FEATURE_COLUMNS].values,
        dtype=torch.float32
    )

    # Универсально обрабатываем ID
    if "id" in df.columns:
        track_ids = df["id"].astype(str).tolist()
    elif "track_id" in df.columns:
        track_ids = df["track_id"].astype(str).tolist()
    else:
        track_ids = None  # допустимо

    return features, track_ids
import pandas as pd
import torch

FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "valence",
    "tempo",
    "loudness",
    "acousticness",
    "instrumentalness",
    "speechiness",
    "liveness",
    "popularity"
]

def load_spotify_csv(path, limit=None):
    df = pd.read_csv(path)

    # Проверка фич
    missing = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    if limit:
        df = df.sample(limit, random_state=42)

    df = df.dropna(subset=FEATURE_COLUMNS)

    features = torch.tensor(
        df[FEATURE_COLUMNS].values,
        dtype=torch.float32
    )

    # Универсально обрабатываем ID
    if "id" in df.columns:
        track_ids = df["id"].astype(str).tolist()
    elif "track_id" in df.columns:
        track_ids = df["track_id"].astype(str).tolist()
    else:
        track_ids = None  # допустимо

    return features, track_ids
