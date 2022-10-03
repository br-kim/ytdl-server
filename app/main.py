import os

import uvicorn
from fastapi import FastAPI

from routers import download

app = FastAPI()
app.include_router(download.download_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", 8000), reload=True)
