import os

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from routers import download
from schedule.youtube_download import download_playlist

app = FastAPI()
app.include_router(download.download_router)


@app.on_event("startup")
async def setting_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(download_playlist, "cron", args=["https://www.youtube.com/playlist?list=PLX3CrwbL_r9bWZLNNSokkCyglMYs1uEzn"], hour=4)
    scheduler.print_jobs()
    scheduler.start()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", 8000), reload=True)
