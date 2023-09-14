from pydantic import BaseModel


class Video(BaseModel):
    title: str
    is_downloaded: bool
    resource_id: str

    class Config:
        from_attributes = True
