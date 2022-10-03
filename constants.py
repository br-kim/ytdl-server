import os
from pathlib import Path

BASE_PATH = os.path.abspath(os.path.curdir)
DOWNLOAD_PATH = Path(BASE_PATH).joinpath(Path("download"))
print(BASE_PATH, DOWNLOAD_PATH)