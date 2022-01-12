from datetime import datetime

from loguru import logger
from sqlmodel import Session, create_engine, select

from film import Film

logger.add(f"logs/{datetime.now():%Y-%m-%d}.log")

class IMDbPipeline(object):
    def __init__(self):
        sqlite_file_name = "../database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"

        engine = create_engine()
        
        self.session = Session(engine)

    def process_item(self, item):
        item_exists = self.session.exec(select(Film).where(Film.name == item.name).where(Film.year == item.year))
        
        if item_exists:
            item_exists = item
            print('Item {} updated.'.format(item.title))

        else:     
            new_item = Film(**item)
            self.session.add(new_item)
            print('New item {} added to DB.'.format(item.title))
        return item    

    def close_spider(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
