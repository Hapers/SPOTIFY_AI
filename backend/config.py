# backend/config.py
from pathlib import Path
import torch

# spotify_ai/
BASE_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = BASE_DIR / "models"

AUTOENCODER_PATH = MODELS_DIR / "autoencoder.pt"
EMBEDDINGS_PATH = MODELS_DIR / "embeddings.pt"
SCALER_PATH = MODELS_DIR / "scaler.pkl"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TOP_K = 10


