# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    """
    In this class, we define all the items that we want to scrape
    from the webpage. We define every item as a Scrapy Field.
    """
    id = scrapy.Field()
    uni = scrapy.Field()
    name = scrapy.Field()
    department = scrapy.Field()
    department_id = scrapy.Field()
    level = scrapy.Field()
    language = scrapy.Field()
    ects = scrapy.Field()
    prerequisites = scrapy.Field()
    description = scrapy.Field()
    valid_from = scrapy.Field()
    valid_to = scrapy.Field()
    link = scrapy.Field()
    link_type = scrapy.Field()
