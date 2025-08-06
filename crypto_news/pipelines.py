# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from scrapy.exceptions import DropItem


class CryptoNewsPipeline:
    def process_item(self, item, spider):
        return item

class PostgresPipeline:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='-------', # host of the database
            user='------', # username of the database
            password='------', # password of the database
            dbname='------', # name of the database
        )
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""
                INSERT INTO crypto_news (url, title, date, content)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
            """, (
                item.get('url'),
                item.get('title'),
                item.get('date'),
                item.get('content')
            ))
            self.connection.commit()
            return item
        except psycopg2.Error as e:
            self.connection.rollback()
            raise DropItem(f"Error inserting item into database: {e}")

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
