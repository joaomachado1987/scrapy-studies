# -*- coding: utf-8 -*-
import scrapy
from noticias.items import FilmesItem
import json

class TecnoblogSpider(scrapy.Spider):
    url ='https://www.imdb.com/find?ref_=nv_sr_fn&q='
    url_final = '&s=all'
    name = 'Imdb'
    allowed_domains = ['www.imdb.com']

    start_urls = []

    with open("filmes-teste.json", "r") as read_file:
        datas = json.load(read_file)
        titulosJson = [data for data in datas['filmes']]
        titulos_esp = [data['title'] for data in titulosJson]
        titulos = [str(titulo).replace(" ", "+") for titulo in titulos_esp]
        # [start_urls.append(url+titulo) for titulo in titulos]
        # start_urls.append(url+titulos)
        for tit in titulos:
            start_urls.append(url + tit + url_final)
    print(start_urls)

    def parse(self, response):
      for section in response.css("span.home_img_holder"):
        print("##################")
        print(section)