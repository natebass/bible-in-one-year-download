from datetime import date
from pathlib import Path

from pydantic import BaseModel


class Mp3File(BaseModel):
    """Model for Mp3 file
    """
    file_path: Path | None
    name: str | None
    description: str | None
    link: str | None
    guid: str | None
    image: str | None
    duration: int | None
    episode: int | None
    season: int = 1
    publishedDate: date | None
