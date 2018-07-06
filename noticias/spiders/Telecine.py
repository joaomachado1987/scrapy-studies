# -*- coding: utf-8 -*-
import scrapy
from noticias.items import FilmesItem

class TecnoblogSpider(scrapy.Spider):
    name = 'Telecine'
    allowed_domains = ['telecine.globo.com', 'telecine.img.estaticos.tv.br']
    start_urls = ['http://telecine.globo.com/programacao/']

    def parse(self, response):
      # for section in response.css("section.clearfix.cl"):
      #   title = section.css("ul li strong a::attr(title)").extract_first()
      #   hora = section.css("span.horario-grade ::text").extract_first()
      #   canal = section.css("li.canal.clearfix figure img::attr(title)").extract_first()
      #   sinopse = section.css("p.sinopse ::text").extract_first()
      #
      #   # print("###############################################")
      #   # print(title)
      #   # print(hora)
      #   # print(canal)
      #   # print(sinopse)
      #   # print("###############################################")
      #
      #   yield FilmesItem(title=title, hora=hora, canal=canal, sinopse=sinopse)

      for link in response.css('li.aba_dia::attr(data-href)').extract():
          print("###########################")
          print(link)
          request = scrapy.Request(link, callback=self.parse_grade)
          yield request

    def parse_grade(self, response):
        print("--------------INICIO-------------------")
        url = response.url.split('/')[-1:]
        data = url[0].strip('.html').replace('_','/')
        print("--------------FIM-------------------")
        for section in response.css("section.clearfix"):
            print("*****************************")
            horario = section.css("section span.horario-grade ::text").extract()
            print(horario)

            for li in section.css("ul li"):
                title = li.css("article strong ::text").extract()
                sinopse = li.css("article p.sinopse ::text").extract()
                canal = li.css("::attr(data-canal)").extract()
                play = li.css(".box-assista-no-play").extract()
                print(title)
                print(sinopse)
                print(canal)
                print(play)
                print(data)
                yield FilmesItem(title=title, hora=horario, canal=canal, sinopse=sinopse, play=play, data=data)
            print("*****************************")

# response.css('div.ratingValue strong::attr("title")').extract()

