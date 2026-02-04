from pydantic import BaseModel
from typing import List, Optional

class SearchResponse(BaseModel):
    id: str
    name: str
    artist: str
    image: Optional[str]

class RecommendRequest(BaseModel):
    source_type: str
    track_index: int
    mode: str
    genres: List[str] = []
    

class RecommendItem(BaseModel):
    track_id: str
    similarity: float
