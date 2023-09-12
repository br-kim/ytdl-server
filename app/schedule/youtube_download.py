import os
import pprint

from yt_dlp import YoutubeDL
import requests

from constants import get_download_file_list


def download_playlist(playlist_id):
    ydl_opts = {
        "ignoreerrors": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android"],
                "max_comments": [0, 0, 0, 0],
                "player_skip": ["webpage"],
            },
        },
        "flat-playlist": True,
    }
    dl_opts = {"outtmpl": "/home/ii/PycharmProjects/ytdl-server/app/download/%(title)s.%(id)s.%(ext)s"}
    process_opts = {
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }
    ydl_opts.update(dl_opts)
    ydl_opts.update(process_opts)
    print(ydl_opts)
    with YoutubeDL(ydl_opts) as ydl:
        # res = ydl.extract_info(
        #     "https://www.youtube.com/playlist?list=PLX3CrwbL_r9andFCCGev0-R4ejxxWfQVH",
        #     download=False,
        # )
        # res = ydl.extract_info("PLX3CrwbL_r9b133VmN1YGLX7v7hhjSM0E", download=True)
        playlist = get_playlist_items(playlist_id)
        video_ids = [p["resource_id"] for p in playlist]
        already_downloaded_file_ids = get_downloaded_ids()

        download_video_list = list(set(video_ids) - set(already_downloaded_file_ids))
        print(download_video_list)
        if not download_video_list:
            print("새로운 동영상 없음")
        res = ydl.download(download_video_list)
        print("download completed")
        return res


def get_playlist_items(playlist_id = None):
    if not playlist_id:
        raise ValueError
    api_key = os.getenv("YOUTUBE_API_KEY")
    next_page_token = True
    result = []
    while next_page_token:
        request_url = "https://youtube.googleapis.com/youtube/v3/playlistItems?"\
                      f"part=snippet&playlistId={playlist_id}&key={api_key}&maxResults=50"
        if next_page_token is not True:
            request_url += f"&pageToken={next_page_token}"
        res = requests.get(request_url)
        res_json = res.json()
        res_items = res_json.get("items")
        if res_items:
            for _item in res_items:
                snippet = _item["snippet"]
                resource_id = snippet["resourceId"]["videoId"]
                title = snippet["title"]
                item_dict = dict(title=title, resource_id=resource_id)
                result.append(item_dict)
        next_page_token = res_json.get("nextPageToken")
        # next_page_token = None

    pprint.pprint(result)
    return result

def get_downloaded_ids():
    path = get_download_file_list()
    # path = "/home/ii/PycharmProjects/ytdl-server/app/download"
    file_list = os.listdir(path)
    file_ids = [file_name.split(".")[-2] for file_name in file_list]
    print(file_list, file_ids)
    return file_ids
#
# if __name__ == "__main__":
#     download_playlist()
