from app.database.base import engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Create a thread-local session factory
session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Session = scoped_session(session_factory)


def get_db():
    """
    Generator function that yields a new Session instance.
    Ensures the session is properly closed after each request.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()
