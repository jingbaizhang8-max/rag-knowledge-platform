from fastapi import APIRouter

from app.schemas.search import SearchRequest,SearchResponse
from app.services.retrieval_service import retrieve_chunks

router = APIRouter()

@router.post("", response_model=SearchResponse)
def search(request: SearchRequest):
    results= retrieve_chunks(
        query=request.query,
        limit=request.limit
    )

    return {
        "query": request.query,
        "results": results
    }