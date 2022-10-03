import os
from pathlib import Path

BASE_PATH = os.path.abspath(os.path.curdir)
DOWNLOAD_PATH = Path(BASE_PATH).joinpath(Path("download"))

# DOWNLOAD_FILE_LIST = os.listdir(DOWNLOAD_PATH)


def get_download_file_list():
    return os.listdir(DOWNLOAD_PATH)


print(BASE_PATH, DOWNLOAD_PATH, get_download_file_list())
