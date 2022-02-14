from datetime import datetime, timedelta

import pendulum
import prefect
from prefect import Flow, config, task
from prefect.run_configs import DockerRun
from prefect.schedules import CronSchedule
from prefect.storage import GitHub
from scrapy.crawler import CrawlerProcess
from sqlmodel import SQLModel, create_engine

from imdb_rating.dependencies.spiders import IMDBSpider


@task
def scrap_movies_from_imdb():
    """
    Scrap movies from IMDB and store them into a PostgreSQL database using SQLModel.
    Run a scrapy crawler process to launch a spider.
    """
    logger = prefect.context.get("logger")

    # engine = create_engine('postgresql://postgres:postgres@localhost:5432/imdb')
    engine = create_engine("sqlite:///imdb.db")
    SQLModel.metadata.create_all(engine)

    start = datetime.today() - timedelta(days=90)
    end = datetime.today() + timedelta(days=30)

    process = CrawlerProcess()

    process.crawl(IMDBSpider, start=start, end=end, engine=engine)
    process.start()


schedule = CronSchedule("0 0 * * *", start_date=pendulum.now(tz="Europe/Paris"))

storage = GitHub(repo="PeregHer/imdb-rating-predictions", path="workflow/flow.py")

run_config = DockerRun(image="imdb-scraping:latest")


with Flow(
    "imdb_scraping", schedule=schedule, storage=storage, run_config=config
) as flow:
    scrap_movies_from_imdb()


flow.run_config = DockerRun(
    image="imdb-scraping:latest",
)

flow.register(project_name="imdb")
# flow.run()
