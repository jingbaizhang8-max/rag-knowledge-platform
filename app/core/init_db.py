from app.core.database import Base, engine

from app.models.document import Document
from app.models.query_history import QueryHistory

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created.")
