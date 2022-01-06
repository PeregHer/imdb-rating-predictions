import scrapy
from scrapy.crawler import CrawlerProcess


class IMDBSpier(scrapy.Spider):
    name = 'imdb'
    custom_settings = {
        'FEED_EXPORT_ENCODING' : 'utf-8'
        }
    
    def start_requests(self):
        yield scrapy.Request(url=f'https://www.imdb.com/search/title/?genres={self.genre}&title_type=feature&explore=genres&start=1', callback=self.parse)
    
    
    def parse(self, response):
        for film in response.xpath('//*[@id="main"]/div/div[3]/div/div'):
            
            try: title = film.xpath('.//div[3]/h3/a/text()').get()
            except: title = None
            
            try: year = int(film.xpath('.//div[3]/h3/span[2]/text()').get().replace('(', '').replace(')', ''))
            except: year = None
            
            try: rating = float(film.xpath('.//div[3]/div/div/strong/text()').get())
            except: rating = None
            
            try: duration = int(film.css('span.runtime::text').get().replace(' min', ''))
            except: duration = None
            
            try: 
                genres = film.css('span.genre::text').get().split(', ')
                genres = [genre.strip() for genre in genres]
            except: genres = []
            
            try: certificate = film.css('span.certificate::text').get()
            except: certificate = None
        
            try: synopsis = film.xpath('.//div[3]/p[2]/text()').get().strip()
            except: synopsis = None
            
            try: votes = int(film.xpath('.//div[3]/p[4]/span[2]/text()').get().replace(',', '').strip())
            except: votes = None
            
            try: 
                cast = film.xpath('.//div[3]/p[3]/*/text()').getall()
                split = cast.index('|')
                directors = cast[:split]
                actors = cast[split+1:]
            except: 
                directors = []
                actors = []
            
            
            yield {
                'title': title,
                'year': year,
                'rating': rating,
                'votes': votes,
                'duration': duration,
                'genres': genres,
                'certificate': certificate,
                'synopsis': synopsis,
                'directors': directors,
                'actors': actors
            }
        
        next_page = response.css('a.next-page::attr(href)').get()
        yield response.follow(next_page, callback=self.parse)

process = CrawlerProcess({
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'output/result_all.csv'
    })

for genre in ['action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama', 'family', 'fantasy', 'game-show', 'history', 'horror', 'music', 'musical', 'mystery', 'news', 'reality-tv', 'romance', 'sci-fi', 'sport', 'superhero', 'thriller', 'war', 'western']:
    process.crawl(IMDBSpier, genre=genre)
        
    process.start()