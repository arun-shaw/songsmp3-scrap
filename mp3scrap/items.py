# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Mp3MovieItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    M_Director = scrapy.Field()
    Composer = scrapy.Field()
    Singer = scrapy.Field()


class Mp3SongsItem(scrapy.Item):
    Mov_Name = scrapy.Field()
    Title = scrapy.Field()
    url = scrapy.Field()
    Artist = scrapy.Field()
    Size = scrapy.Field()
