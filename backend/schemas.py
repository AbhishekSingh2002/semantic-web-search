from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class SearchRequest(BaseModel):
    url: str
    query: str

class SearchResult(BaseModel):
    content: str
    token_count: int
    relevance_score: float
    chunk_id: str

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_chunks: int
    url: str
    query: str