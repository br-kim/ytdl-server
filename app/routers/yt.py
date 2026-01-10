from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl

# /root/ytdl-server/app/routers/yt.py
"""
기본적인 FastAPI router 파일 구조 (yt 관련 엔드포인트)
- 라우터 생성
- 간단한 GET/POST 예시
- Pydantic 모델 사용 예시
"""


router = APIRouter(
    prefix="/yt",
    tags=["yt"],
    responses={404: {"description": "Not found"}},
)


# 요청/응답 모델 예시
class YTDownloadRequest(BaseModel):
    url: HttpUrl
    format: Optional[str] = "mp4"  # 예: mp4, mp3
    quality: Optional[str] = "best"


class YTDownloadResponse(BaseModel):
    task_id: str
    status: str
    message: Optional[str] = None

class YTPlaylistResponse(BaseModel):
    pass

# 간단한 헬스체크 엔드포인트
@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> dict:
    """
    yt 라우터 헬스 체크
    """
    return {"status": "ok", "service": "yt"}


# 다운로드 작업을 백그라운드로 수행하는 예시 엔드포인트
async def _fake_download_task(url: str, fmt: str, quality: str) -> None:
    """
    실제 다운로드 로직을 이곳에 구현하세요.
    현재는 예시용으로 비워둡니다.
    """
    # TODO: youtube-dl / yt-dlp 호출, 파일 저장 등 구현
    return


@router.post("/download", response_model=YTDownloadResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_download(
    payload: YTDownloadRequest,
    background: BackgroundTasks,
) -> YTDownloadResponse:
    """
    다운로드 요청을 받고 백그라운드로 처리합니다.
    실제 다운로드 구현은 _fake_download_task를 대체하세요.
    """
    # 간단한 유효성 검사 예시
    if not payload.url:
        raise HTTPException(status_code=400, detail="url is required")

    # task_id 생성 (간단 예시)
    task_id = f"yt-{hash((payload.url, payload.format, payload.quality)) & 0xFFFFFFFF:08x}"

    # 백그라운드 작업 등록
    background.add_task(_fake_download_task, str(payload.url), payload.format, payload.quality)

    return YTDownloadResponse(task_id=task_id, status="queued", message="Download started in background.")


# (선택) 특정 태스크 상태 조회 엔드포인트 예시
@router.get("/tasks/{task_id}", response_model=YTDownloadResponse)
async def get_task_status(task_id: str) -> YTDownloadResponse:
    """
    task_id 기반 상태 조회 (실제 상태 추적 로직 필요)
    """
    # TODO: 실제 작업 상태 스토어(예: DB, Redis)에서 상태 조회
    # 현재는 모의 응답
    return YTDownloadResponse(task_id=task_id, status="unknown", message="Task tracking not implemented.")