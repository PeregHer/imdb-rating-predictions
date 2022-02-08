from sqlmodel import Session, create_engine, select

from components.movie import Movie

engine = create_engine('postgresql://postgres:postgres@localhost:5432/imdb', echo=True)

# SQLModel.metadata.create_all(engine)

movie1 = Movie(
    title='The Shawshank Redemption',
    actual_rating=9.3,
    year=1994,
    duration=142,
    votes=936_943,
    certificate='R',
    image='https://m.media-amazon.com/images/S/sash/4FyxwxECzL-U1J8.png',
    synopsis='Two imprisoned',
    actor1='Tim Robbins',
    actor2='Morgan Freeman',
    actor3='Bob Gunton',
    director1='Frank Darabont',
    genre1='Drama',
    genre2='Crime',
    genre3='Thriller'
)

with Session(engine) as session:
    # session.add(movie1)
    # session.commit()
    
    statement = select(Movie)
    results = session.exec(statement)
    movies = results.all()
    for movie in movies:
        print(movie.dict())
