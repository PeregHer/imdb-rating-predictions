import re
from pydantic import BaseModel, ValidationError, HttpUrl

from fastapi import FastAPI
from typing import List, Optional
import pandas as pd
import subprocess
import os


class Movie(BaseModel):
    title: str
    rating: Optional[float] = None
    year: Optional[int] = None
    duration: Optional[int] = None
    votes: Optional[int] = None
    certificate: Optional[str] = None
    image: Optional[HttpUrl] = 'https://m.media-amazon.com/images/S/sash/4FyxwxECzL-U1J8.png'
    synopsis: Optional[str] = None
    actor1: Optional[str] = None
    actor2: Optional[str] = None
    actor3: Optional[str] = None
    actor4: Optional[str] = None
    director1: Optional[str] = None
    director2: Optional[str] = None
    director3: Optional[str] = None
    genre1: Optional[str] = None
    genre2: Optional[str] = None
    genre3: Optional[str] = None


app = FastAPI()

@app.post("/predict")
def make_prediction(movies: List[Movie]):
    df_movies = pd.DataFrame([dict(s) for s in movies])
    df_movies.to_csv('tmp/to_predict.csv', index=False)
    
    subprocess.run(['java', '-jar', 'xgboost.jar', 'csv', '--input=tmp/to_predict.csv', '--output=tmp/predicted.csv'])
    
    df_predicted = pd.read_csv('tmp/predicted.csv')
    
    
    for rating, movie in zip(df_predicted.to_dict('records'), movies):
        try:
            movie.rating = rating['PREDICTION']
        except ValidationError:
            continue

    # os.remove('tmp/to_predict.csv')
    # os.remove('tmp/predicted.csv')

    return movies
    
