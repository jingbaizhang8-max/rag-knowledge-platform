from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    document_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        index=True,
        nullable=False
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    page_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    chunk_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )