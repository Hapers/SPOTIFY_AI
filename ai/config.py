import os
import torch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMBEDDINGS_PATH = os.path.join(BASE_DIR, "models", "embeddings.pt")

TOP_K = 10
DEVICE = torch.device("cpu")
