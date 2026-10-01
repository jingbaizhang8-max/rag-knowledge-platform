from pydantic import BaseModel, Field, ConfigDict


class AskRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=3,ge=1,le=10)
    document_id: str | None=None

    model_config = ConfigDict(
        extra="forbid"
    )

class SourceInfo(BaseModel):
    source: str
    page: int |None

class AskResponse(BaseModel):
    query: str
    answer: str
    sources: list[SourceInfo]