from fastapi.security import HTTPBearer

from database import SessionLocal

authorization = HTTPBearer()


def get_db():
    db = SessionLocal()
    db.begin()
    try:
        yield db
    finally:
        db.close()
