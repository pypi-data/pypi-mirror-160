# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# Useful for handling different item types with a single interface

import scrapy
import sqlite3
from pathlib import Path

main_dir: Path = Path(__file__).parents[2]


# noinspection PyUnusedLocal, PyMethodMayBeStatic
class CrawlerPipeline:
    """A pipeline to store the scraped data into an SQLite DB"""
    def __init__(self) -> None:
        """Create a connection and a cursor to the DB"""
        self.con: sqlite3.Connection = sqlite3.connect(f'{main_dir}/database/digital_uni.db')
        self.cur: sqlite3.Cursor = self.con.cursor()
        self.create_table()

    def open_spider(self, spider: scrapy.Spider) -> None:
        spider.logger.info('Opening DB connection')

    def create_table(self) -> None:
        """Create a table in the DB if it does not already exist"""
        # self.cur.execute('DROP TABLE MODULES;')
        self.cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS MODULES (
                ID TEXT,
                NAME TEXT,
                UNI TEXT,
                DEPT TEXT,
                DEPT_ID TEXT,
                LEVEL TEXT,
                LANG TEXT,
                ECTS TEXT,
                PREREQ TEXT,
                DESCRIPTION TEXT,
                VALID_FROM TEXT,
                VALID_TO TEXT,
                LINK TEXT,
                LINK_TYPE TEXT,
                PRIMARY KEY (ID, NAME, UNI, VALID_FROM, VALID_TO)
            );
            '''
        )

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """Preprocess and store the scraped items in the DB"""
        for field in item.fields:
            item.setdefault(field, None)
            if isinstance(item[field], str):
                item[field] = item[field].strip()
            if not item[field]:
                item[field] = None

        self.cur.execute(
            '''
            INSERT OR IGNORE INTO MODULES 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''',
            (
                item['id'],
                item['name'],
                item['uni'],
                item['department'],
                item['department_id'],
                item['level'],
                item['language'],
                item['ects'],
                item['prerequisites'],
                item['description'],
                item['valid_from'],
                item['valid_to'],
                item['link'],
                item['link_type']
            )
        )
        self.con.commit()
        return item

    def close_spider(self, spider: scrapy.Spider) -> None:
        """Close the DB connection after the scraping process"""
        spider.logger.info('Closing DB connection')
        self.con.close()
