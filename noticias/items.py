# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FilmesItem(scrapy.Item):
    title = scrapy.Field()
    hora = scrapy.Field()
    canal = scrapy.Field()
    sinopse = scrapy.Field()
    play = scrapy.Field()
    data = scrapy.Field()
    cast = scrapy.Field()
    directors = scrapy.Field()
    year = scrapy.Field()
    rating = scrapy.Field()
    writer = scrapy.Field()
    genres = scrapy.Field()
