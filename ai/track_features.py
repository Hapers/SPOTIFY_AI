import pandas as pd

CSV_PATH = "data/spotify_tracks_clean.csv"  # ← твой очищенный CSV

df = pd.read_csv(CSV_PATH)

FEATURES = {}

for _, row in df.iterrows():
    FEATURES[row["track_id"]] = {
        "energy": row.get("energy"),
        "tempo": row.get("tempo"),
        "acousticness": row.get("acousticness"),
        "popularity": row.get("popularity"),
    }

print(f"🎛️ Loaded features for {len(FEATURES)} tracks")
