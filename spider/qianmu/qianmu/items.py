# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UniversityItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    myrank = scrapy.Field()
    country = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    undergraduate_num = scrapy.Field()
    postgraduate_num = scrapy.Field()
    website = scrapy.Field()
