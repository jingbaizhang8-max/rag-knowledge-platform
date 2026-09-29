from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=3, ge=1, le=10)

class SearchResult(BaseModel):
    score: float
    document_id: str
    chunk_index: int
    source: str
    page:int | None
    text: str

class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]