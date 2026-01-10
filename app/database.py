import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
# )

# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


engine = create_engine("sqlite:///user.db", poolclass=NullPool)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()
