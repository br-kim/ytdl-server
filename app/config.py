import os
from functools import lru_cache
from typing import List, Dict

from pydantic_settings import BaseSettings

from constants import YTDL_SERVER_ENVIRON


class LocalSettings(BaseSettings):
    JOB_PLAYLIST: List[str] = os.getenv("YOUTUBE_PLAYLIST").split("|")
    JOB_INTERVAL: Dict[str, int] = {"second": 30}


class ProductionSettings(BaseSettings):
    JOB_PLAYLIST: List[str] = os.getenv("YOUTUBE_PLAYLIST").split("|")
    JOB_INTERVAL: Dict[str, int] = {"hour": 4}


@lru_cache()
def get_settings():
    if YTDL_SERVER_ENVIRON == "local":
        return LocalSettings()
    elif YTDL_SERVER_ENVIRON == "prod":
        return ProductionSettings()
