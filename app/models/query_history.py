from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class QueryHistory(Base):
    __tablename__ = "query_history"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    query: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    answer: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    document_id: Mapped[str | None] = mapped_column(
        String(36),
        nullable=True,
        index=True
    )

    sources: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )