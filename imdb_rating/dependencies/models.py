from typing import Optional

from pydantic import HttpUrl
from sqlmodel import Field, SQLModel


class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    actual_rating: Optional[float] = None
    predicted_rating: Optional[float] = None
    year: int
    duration: Optional[int] = None
    votes: Optional[int] = None
    certificate: Optional[str] = None
    image: Optional[
        HttpUrl
    ] = "https://m.media-amazon.com/images/S/sash/4FyxwxECzL-U1J8.png"
    synopsis: Optional[str] = None
    genre1: Optional[str] = None
    genre2: Optional[str] = None
    genre3: Optional[str] = None
    actor1: Optional[str] = None
    actor2: Optional[str] = None
    actor3: Optional[str] = None
    director1: Optional[str] = None
    director2: Optional[str] = None
    director3: Optional[str] = None
