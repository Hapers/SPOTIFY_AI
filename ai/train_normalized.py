import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import joblib
from sklearn.preprocessing import StandardScaler

from model import AutoEncoder
from csv_data import load_spotify_csv
from config import *

import os

os.makedirs("models", exist_ok=True)


CSV_PATH = "data/spotify_tracks.csv"

def train():
    # 1️⃣ Load CSV
    features, track_ids = load_spotify_csv(CSV_PATH, limit=10000)

    # 2️⃣ Normalize
    scaler = StandardScaler()
    features_np = scaler.fit_transform(features.numpy())
    features = torch.tensor(features_np, dtype=torch.float32)

    # Save scaler
    joblib.dump(scaler, "models/scaler.pkl")

    # 3️⃣ Training
    features = features.to(DEVICE)
    dataset = TensorDataset(features)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    model = AutoEncoder(INPUT_FEATURES, EMBEDDING_SIZE).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    loss_fn = nn.MSELoss()

    print("🚀 Training normalized autoencoder")

    for epoch in range(EPOCHS):
        total_loss = 0
        for (batch,) in loader:
            optimizer.zero_grad()
            out = model(batch)
            loss = loss_fn(out, batch)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {total_loss:.4f}")

    # 4️⃣ Save model
    torch.save(model.state_dict(), "models/autoencoder.pt")

    # 5️⃣ Generate embeddings
    with torch.no_grad():
        embeddings = model.encode(features).cpu()

    torch.save(
        {
            "embeddings": embeddings,
            "track_ids": track_ids
        },
        "models/embeddings.pt"
    )

    print("✅ Model, scaler and embeddings saved")

if __name__ == "__main__":
    train()
