import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

INPUT_FEATURES = 10
EMBEDDING_SIZE = 16
EPOCHS = 20
BATCH_SIZE = 128
LEARNING_RATE = 0.001

print("Using device:", DEVICE)