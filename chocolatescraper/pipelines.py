# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from mysql.connector
import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item

class PriceToUSDPipeline:
    gbpToUSDRate = 1.3
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if adapter.get('price'):
            
            floatPrice = float(adapter['price'])
            adapter['price'] =  floatPrice * self.gbpToUSDRate
            return item
        else:
            raise DropItem(f"Missing price in {item}")

class DuplicatesPipeline:
    
    def __init__(self):
        self.names_seen = set()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter["name"])
            return item

class SavingToMysqlPipeline(object):
    
    def __init__(self):
        self.create_connection()
        self.id = 0
        
    def create_connection(self):
        self.connection = pyscopg2.connect(
            host= 'localhost',
            host = 'root',
            password = "",
            database = "",
            port = ""
        )
        self.curr = self.connection.cursor()
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        self.curr.execute(""" insert into chocolate_products  (name, price, url) values (%s, %s, %s)""", (
            item["name"],
            item["price"],
            item["url"]
        ))
        self.connection.commit()
        

class SavingToPostgresPipeline(object):
    
    
    def __init__(self):
        self.create_connection()
        
    def create_connection(self):
        self.connection = mysql.connector.connect(
            host= 'localhost',
            host = 'root',
            password = "",
            database = "",
            port = ""
        )
        self.curr = self.connection.cursor()
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        try:
            self.curr.execute(""" insert into chocolate_products  (name, price, url) values (%s, %s, %s)""", (
                item["name"],
                item["price"],
                item["url"]
            ))
        except BaseException as e:
            print(e)
        self.connection.commit()
        