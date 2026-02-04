import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
import joblib

from ai.csv_data import load_spotify_csv, FEATURE_COLUMNS
from ai.model import AutoEncoder

# ======================
# CONFIG
# ======================

CSV_PATH = "data/spotify_tracks_clean.csv"
MODELS_DIR = "models"

INPUT_DIM = len(FEATURE_COLUMNS)
EMBEDDING_DIM = 16
BATCH_SIZE = 128
EPOCHS = 30
LR = 1e-3

os.makedirs(MODELS_DIR, exist_ok=True)

# ======================
# LOAD DATA
# ======================

print("📂 Loading CSV...")
X, track_ids = load_spotify_csv(CSV_PATH)

print(f"✅ Loaded {len(X)} tracks with {INPUT_DIM} features")

# ======================
# NORMALIZE
# ======================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X.numpy())
X_scaled = torch.tensor(X_scaled, dtype=torch.float32)

joblib.dump(scaler, f"{MODELS_DIR}/scaler.pkl")

# ======================
# DATASET
# ======================

dataset = TensorDataset(X_scaled)
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# ======================
# MODEL
# ======================

model = AutoEncoder(INPUT_DIM, EMBEDDING_DIM)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)
loss_fn = nn.MSELoss()

# ======================
# TRAIN
# ======================

print("🧠 Training autoencoder...")

for epoch in range(EPOCHS):
    total_loss = 0.0

    for (batch,) in loader:
        optimizer.zero_grad()
        recon = model(batch)
        loss = loss_fn(recon, batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {total_loss/len(loader):.6f}")

# ======================
# SAVE MODEL
# ======================

torch.save(model.state_dict(), f"{MODELS_DIR}/autoencoder.pt")

# ======================
# SAVE EMBEDDINGS
# ======================

with torch.no_grad():
    embeddings = model.encode(X_scaled)

torch.save(
    {
        "embeddings": embeddings,
        "track_ids": track_ids
    },
    f"{MODELS_DIR}/embeddings.pt"
)

print("✅ Training finished")
print("📦 Saved:")
print(" - models/autoencoder.pt")
print(" - models/embeddings.pt")
print(" - models/scaler.pkl")
