from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerProcess

from film import Film


class IMDBSpier(scrapy.Spider):
    name = 'imdb'
    custom_settings = {
        'FEED_EXPORT_ENCODING' : 'utf-8'
        }
    
    def start_requests(self):
        yield scrapy.Request(url=f'https://www.imdb.com/search/title/?title_type=feature&year={self.start},{self.end}&start=1', callback=self.parse)
    
    
    def parse(self, response):
        for film in response.xpath('//*[@id="main"]/div/div[3]/div/div'):
            
            try: title = film.xpath('.//div[3]/h3/a/text()').get()
            except: title = None
            
            try: year = film.xpath('.//div[3]/h3/span[2]/text()').get().replace('(', '').replace(')', '')
            except: year = None
            
            try: duration = film.css('span.runtime::text').get().replace(' min', '')
            except: duration = None
            
            try: 
                genres = film.css('span.genre::text').get().split(', ')
                genres = [genre.strip() for genre in genres]
            except: genres = []
            
            try: certificate = film.css('span.certificate::text').get()
            except: certificate = None
        
            try: synopsis = film.xpath('.//div[3]/p[2]/text()').get().strip()
            except: synopsis = None
            
            try: image = film.xpath('.//div[2]/a/img/@loadlate').get().split('._V1_')[0]
            except Exception as e: 
                image = None
                print(e)
            
            try: 
                cast = film.xpath('.//div[3]/p[3]/*/text()').getall()
                split = cast.index('|')
                directors = cast[:split]
                actors = cast[split+1:]
            except: 
                directors = []
                actors = []
            
            film = Film(
                title=title,
                year=year,
                duration=duration,
                genres=genres,
                certificate=certificate,
                synopsis=synopsis,
                image=image,
                directors=directors,
                actors=actors
            )
            
            yield film.dict()
        
        try:
            next_page = response.css('a.next-page::attr(href)').get()
            yield response.follow(next_page, callback=self.parse)
        except:
            pass

if __name__ == '__main__':
    process = CrawlerProcess({
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'data/upcoming.csv'
        })

    start = '2022-01-01'
    end = '2022-01-31'

    process.crawl(IMDBSpier, start=start, end=end)
    process.start()
