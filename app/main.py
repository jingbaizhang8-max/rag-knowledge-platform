from fastapi import FastAPI
from  app.api.documents import router as documents_router
from app.api.search import router as search_router


app = FastAPI(
    title="RAG Knowledge Platform",
    version="0.1.0"
)

app.include_router(
    documents_router,
    prefix="/documents",
    tags=["Documents"]
)

app.include_router(
    search_router,
    prefix="/search",
    tags=["Search"]
)

@app.get("/health")
def health_check():
    return {
        "status": " ok "
    }




