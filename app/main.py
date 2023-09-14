import os

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from config import get_settings
from database import engine, Base
from routers import index, video
from schedule.youtube_download import download_playlist

app = FastAPI()
app.include_router(index.index_router)
app.include_router(video.video_router)


@app.on_event("startup")
async def setting_scheduler():
    Base.metadata.create_all(engine)
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        download_playlist,
        "cron",
        args=[get_settings().JOB_PLAYLIST],
        **get_settings().JOB_INTERVAL,
    )
    scheduler.print_jobs()
    scheduler.start()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", 8000), reload=True)
