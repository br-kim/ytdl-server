import os.path
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, Response
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

import crud
from constants import DOWNLOAD_PATH
from dependencies import get_db
from schema import Video

video_router = APIRouter()


@video_router.get("/video", response_model=List[Video])
async def get_downloaded_video_list(db=Depends(get_db)):
    """
    DB에 저장된 다운로드 된 비디오 목록 API
    :param db:
    :return:
    """
    return [Video.model_validate(i) for i in crud.get_all_video(db)]


@video_router.get("/video/{resource_id}")
async def download_video(resource_id: str, db=Depends(get_db)):
    """
    비디오 다운로드 API
    :param resource_id:
    :param db:
    :return:
    """
    video = crud.get_video_by_resource_id(db=db, resource_id=resource_id)
    file_name = video.file_path
    filepath = str(DOWNLOAD_PATH) + str(Path(f"/{file_name}"))
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404)
    return FileResponse(filepath, media_type="video/mp3")


@video_router.patch("/video/{resource_id}")
async def edit_video_status(resource_id: str, status: bool, db=Depends(get_db)):
    """
    비디오 다운로드 여부 수정 API
    :param resource_id:
    :param status:
    :param db:
    :return:
    """
    crud.edit_video_downloaded_status(db=db, resource_id=resource_id, status=status)
    return Response(status_code=200)
