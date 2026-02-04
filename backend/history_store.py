from datetime import datetime, timezone
from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient(
    "mongodb://127.0.0.1:27017/",
    serverSelectionTimeoutMS=2000, # Ждать максимум 2 секунды
    connectTimeoutMS=2000
)
try:
    client.admin.command('ping')
    print("✅ MongoDB подключена успешно (History Module)!")
except Exception as e:
    print(f"❌ Ошибка подключения к MongoDB: {e}")
    
db = client["spotify_ai"]
history_collection = db["history"]

def add_history(user_id, source_track_id, source_track_name, source_track_image, mode, recommended):
    entry = {
        "user_id": user_id,
        "source_track_id": source_track_id,
        "source_track_name": source_track_name,
        "source_track_image": source_track_image,
        "mode": mode,
        "recommended": recommended,
        # Исправляем депрекацию здесь:
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    history_collection.insert_one(entry)

def get_history(user_id):
    # Добавляем сортировку, чтобы новые рекомендации были сверху
    cursor = history_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(20)
    history = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        history.append(doc)
    return history
