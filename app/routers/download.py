import os.path
from pathlib import Path
from typing import List

from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import crud
from constants import DOWNLOAD_PATH
from dependencies import get_db

download_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@download_router.get("/")
async def main(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})


class Video(BaseModel):
    title: str
    is_downloaded: bool
    resource_id: str

    class Config:
        from_attributes = True


@download_router.get("/download", response_model=List[Video])
async def get_download_list(db=Depends(get_db)):
    return [Video.model_validate(i) for i in crud.get_all_video(db)]


@download_router.get("/download/{file_name}")
async def download_file(file_name: str):
    filepath = str(DOWNLOAD_PATH) + str(Path(f"/{file_name}"))
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404)
    return FileResponse(filepath, media_type="video/mp4")


@download_router.patch("/video/{resource_id}")
async def edit_video_status(resource_id: str, status: bool, db=Depends(get_db)):
    crud.edit_video_downloaded_status(db=db, resource_id=resource_id, status=status)


if __name__ == "__main__":
    pass
