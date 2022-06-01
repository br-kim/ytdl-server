from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from yt_dlp import YoutubeDL

download_router = APIRouter()


@download_router.get("/")
async def main(request: Request):
    return FileResponse("pages/main_page.html")


@download_router.get("/playlist")
async def get_playlist(request: Request):
    ydl_opts = {
        'ignoreerrors': True,
    }
    with YoutubeDL(ydl_opts) as ydl:

        res = ydl.extract_info("https://www.youtube.com/watch?v=r97Wb-KLiKU", download=False)
        for i in res["formats"]:
            if i["audio_ext"] != "none":
                if i["format_note"] == "medium":
                    return HTMLResponse(f"""
                    <html> <a href="{i['url']}">다운로드</a> </html>
                    """)


        return res["formats"]
