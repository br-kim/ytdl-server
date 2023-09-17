from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(String, unique=True)
    title = Column(String)
    is_downloaded = Column(Boolean, default=False)
    file_path = Column(String)
