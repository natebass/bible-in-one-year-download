from pathlib import Path
from pydantic import BaseModel


class CommandLineArguments(BaseModel):
    """Handle arguments passed by the user to the command line interface.
    :var download_all: bool
    :var episode: str | None
    :var number_of_episodes [int] for days. 1 is one day ahead and back. -1 is behind. +1 is future.
    :var cache_enabled: bool
    :var remove_cache: bool
    :var feed_url: str | None
    :var audio_files_directory: Path | None
    """
    download_all: bool = True
    episode: str | None
    number_of_episodes: int | None
    cache_enabled: bool = True
    remove_cache: bool = False
    feed_url: str | None
    audio_files_directory: Path | None
