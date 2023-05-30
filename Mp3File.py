from datetime import date
from pathlib import Path

from pydantic import BaseModel


class Mp3File(BaseModel):
    file_path: Path
    name: str
    description: str
    link: str
    guid: str
    image: str
    duration: int
    episode: int
    season = 1
    publishedDate: date
