from collections.abc import Generator

from sqlalchemy.orm import Session

from app.infrastructure.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Create a database session for each request.
    Automatically closes the session when the request ends.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()