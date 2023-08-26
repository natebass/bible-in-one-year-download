from pathlib import Path

from pydantic import BaseModel


class CommandLineArguments(BaseModel):
    download_all: bool = True
    episode: str | None
    number_of_episodes: int | None
    cache_enabled: bool = True
    remove_cache: bool = False
    feed_url: str | None
    audio_files_directory: Path | None
