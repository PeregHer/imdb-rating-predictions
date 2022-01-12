from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from sqlmodel import Field, SQLModel


class FilmSQL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    rating: float = None
    year: int = None
    duration: int = None
    votes: int = None
    certificate: str = None
    image: HttpUrl = 'https://m.media-amazon.com/images/S/sash/4FyxwxECzL-U1J8.png'
    synopsis: str = None
    actors: str = None
    directors: str = None
    genres: str = None


class Film(BaseModel):
    title: str
    rating: float = None
    year: int = None
    duration: int = None
    votes: int = None
    certificate: str = None
    image: HttpUrl = 'https://m.media-amazon.com/images/S/sash/4FyxwxECzL-U1J8.png'
    synopsis: str = None
    actors: List[str] = []
    directors: List[str] = []
    genres: List[str] = []
