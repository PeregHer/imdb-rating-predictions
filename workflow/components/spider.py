import scrapy
from pydantic import ValidationError
from scrapy.crawler import CrawlerProcess
from sqlmodel import Session, select

from components.movie import Movie


class IMDBSpider(scrapy.Spider):
    name = 'imdb'
    custom_settings = {
        'FEED_EXPORT_ENCODING' : 'utf-8'
        }
    
    def start_requests(self):
        self.start = self.start.strftime('%Y-%m-%d')
        self.end = self.end.strftime('%Y-%m-%d')
        yield scrapy.Request(url=f'https://www.imdb.com/search/title/?title_type=feature&year={self.start},{self.end}&start=1', callback=self.parse)
    
    
    def parse(self, response):
        for film in response.xpath('//*[@id="main"]/div/div[3]/div/div'):
            
            try: title = film.xpath('.//div[3]/h3/a/text()').get()
            except: title = None
            
            try: year = film.xpath('.//div[3]/h3/span[2]/text()').get().split(' ')[-1].replace('(', '').replace(')', '')
            except: year = None
            
            try: rating = film.xpath('.//div[3]/div/div/strong/text()').get()
            except: rating = None
            
            try: duration = film.css('span.runtime::text').get().replace(' min', '')
            except: duration = None
            
            try: votes = film.css('.//div[3]/p[4]/span[2]/@data-value').get()
            except: votes = None
            
            try: 
                genres = film.css('span.genre::text').get().split(', ')
                genres = [genre.strip() for genre in genres]
                genres.extend([None for _ in range(3-len(genres))])
                genre1, genre2, genre3 = genres[:3]
            except: genre1, genre2, genre3 = None, None, None
            
            try: certificate = film.css('span.certificate::text').get()
            except: certificate = None
        
            try: synopsis = film.xpath('.//div[3]/p[2]/text()').get().strip()
            except: synopsis = None
            
            try: image = film.xpath('.//div[2]/a/img/@loadlate').get().split('._V1_')[0]
            except: image = None
            
            try: 
                cast = film.xpath('.//div[3]/p[3]/*/text()').getall()
                split = cast.index('|')
                directors = cast[:split]
                directors.extend([None for _ in range(3-len(directors))])
                director1, director2, director3 = directors[:3]
                
                actors = cast[split+1:]
                actors.extend([None for _ in range(3-len(actors))])
                actor1, actor2, actor3 = actors[:3]
            except:
                actor1, actor2, actor3 = None, None, None
                director1, director2, director3 = None, None, None
            
            try:
                movie = Movie.validate(
                    dict(
                        title=title,
                        year=year,
                        actual_rating=rating,
                        votes=votes,
                        duration=duration,
                        certificate=certificate,
                        synopsis=synopsis,
                        image=image,
                        actor1=actor1,
                        actor2=actor2,
                        actor3=actor3,
                        director1=director1,
                        director2=director2,
                        director3=director3,
                        genre1=genre1,
                        genre2=genre2,
                        genre3=genre3
                    )
                )
            
                with Session(self.engine) as session:
                    statement = select(Movie).where(Movie.title == movie.title and Movie.year == movie.year)
                    results = session.exec(statement)
                    movie_orig = results.first()

                    if movie_orig:
                        movie_orig_values = dict(movie_orig)
                        movie_orig_values.pop('id')
                        movie_new_values = dict(movie)
                        movie_new_values.pop('id')
                        
                        if movie_orig_values != movie_new_values:
                            for key, value in movie_new_values.items():
                                setattr(movie_orig, key, value)
                            session.add(movie_orig)
                            session.commit()

                    else:
                        session.add(movie)
                        session.commit()
                    
            except ValidationError:
                continue
        
        try:
            next_page = response.css('a.next-page::attr(href)').get()
            yield response.follow(next_page, callback=self.parse)
        except:
            pass


if __name__ == '__main__':
    from datetime import datetime, timedelta
    
    start = datetime.today() - timedelta(days=90)
    end = datetime.today() + timedelta(days=30)
    
    process = CrawlerProcess({
        'FEED_FORMAT': 'json',
        'FEED_URI': f'data/test.json'
        })

    process.crawl(IMDBSpider, start=start, end=end)
    process.start()
