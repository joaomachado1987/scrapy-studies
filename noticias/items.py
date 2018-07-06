# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NoticiasItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
    link = scrapy.Field()

class FilmesItem(scrapy.Item):
    title = scrapy.Field()
    hora = scrapy.Field()
    canal = scrapy.Field()
    sinopse = scrapy.Field()
    play = scrapy.Field()
    data=scrapy.Field()
