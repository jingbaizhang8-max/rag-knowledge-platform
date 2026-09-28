from fastapi import FastAPI
from  app.api.documents import router as documents_router



app = FastAPI(
    title="RAG Knowledge Platform",
    version="0.1.0"
)

app.include_router(
    documents_router,
    prefix="/documents",
    tags=["Documents"]
)

@app.get("/health")
def health_check():
    return {
        "status": " ok "
    }




