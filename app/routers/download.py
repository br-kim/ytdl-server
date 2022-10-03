from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from yt_dlp import YoutubeDL

from constants import DOWNLOAD_PATH, get_download_file_list

download_router = APIRouter()


@download_router.get("/")
async def main(request: Request):
    return FileResponse("app/pages/main_page.html")


@download_router.get("/playlist")
async def get_playlist(request: Request):
    ydl_opts = {
        "ignoreerrors": True,
        "skip_download": True,
        "extractor_args": {"youtube": {"player_client": ["web"]}},
        "flat-playlist": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        res = ydl.extract_info(
            "https://www.youtube.com/playlist?list=PLX3CrwbL_r9andFCCGev0-R4ejxxWfQVH",
            download=False,
        )
        # for i in res["formats"]:
        #     if i["audio_ext"] != "none":
        #         if i["format_note"] == "medium":
        #             return HTMLResponse(f"""
        #             <html> <a href="{i['url']}">다운로드</a> </html>
        #             """)
        return res


@download_router.get("/download")
async def get_download_list():
    return get_download_file_list()


@download_router.get("/download/{file_name}")
async def download_file(file_name: str):
    filepath = str(DOWNLOAD_PATH) + str(Path(f"/{file_name}"))
    print(filepath)
    return FileResponse(filepath)


if __name__ == "__main__":

    def get_playlist():
        ydl_opts = {
            "ignoreerrors": True,
            "skip_download": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android"],
                    "max_comments": [0, 0, 0, 0],
                    "player_skip": ["webpage"],
                },
                # "youtubetab": {"skip": ["webpage"]},
            },
            "flat-playlist": True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            res = ydl.extract_info(
                "https://www.youtube.com/playlist?list=PLX3CrwbL_r9andFCCGev0-R4ejxxWfQVH",
                download=False,
            )

            # for i in res["formats"]:
            #     if i["audio_ext"] != "none":
            #         if i["format_note"] == "medium":
            #             return HTMLResponse(f"""
            #             <html> <a href="{i['url']}">다운로드</a> </html>
            #             """)

            return res

    res = get_playlist()
    print(res)
