from datetime import datetime, timedelta
from pathlib import Path

import pendulum
import prefect
from prefect import Flow, task
from prefect.schedules import CronSchedule
from scrapy.crawler import CrawlerProcess

from components.spider import IMDBSpider
from sqlmodel import create_engine, SQLModel


@task
def scrap_movies_from_imdb():
    """
    Scrap movies from IMDB and store them into a PostgreSQL database using SQLModel.
    Run a scrapy crawler process to launch a spider.
    """
    logger = prefect.context.get("logger")
    
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/imdb')
    SQLModel.metadata.create_all(engine)
    
    start = datetime.today() - timedelta(days=90)
    end = datetime.today() + timedelta(days=30)
    
    process = CrawlerProcess()

    process.crawl(IMDBSpider, start=start, end=end, engine=engine)
    process.start()

schedule = CronSchedule("0 0 * * *", start_date=pendulum.now(tz="Europe/Paris"))

with Flow("imdb_scraping", schedule=schedule) as flow:
    scrap_movies_from_imdb()

flow.register(project_name="imdb")
# flow.run()
