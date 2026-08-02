from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Every database model in the application should inherit
    from this class so SQLAlchemy and Alembic can discover
    the application's schema.
    """
    pass