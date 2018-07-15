import scrapy
from time import gmtime, strftime
import time
from noticias.modules.parse_telecine import Telecine
from noticias.modules.parse_programacao import Programacao

programacao = Programacao()
telecine = Telecine()

class TelecineSpider(scrapy.Spider):

    name = 'Telecine'
    allowed_domains = ['telecine.globo.com', 'telecine.img.estaticos.tv.br']
    start_urls = ['http://telecine.globo.com/programacao/']
    dict_data_hora_link = {}

    def parse(self, response):

      for link in response.css('li.aba_dia::attr(data-href)').extract():
          request = scrapy.Request(link, callback=self.parse_filmes)
          yield request

    def parse_filmes(self, response):

        url = response.url.split('/')[-1:]

        data = url[0].strip('.html').replace('_', '/')
        data_now = strftime('%d/%m/%Y', gmtime())
        data = time.strptime(data, "%d/%m/%Y")
        data_now = time.strptime(data_now, "%d/%m/%Y")

        if data >= data_now:
            for section in response.css("section.clearfix"):

                horario = section.css("section span.horario-grade ::text").extract()

                for li in section.css("ul li"):
                    title = li.css("article strong ::text").extract()
                    sinopse = li.css("article p.sinopse ::text").extract()
                    canal = li.css("::attr(data-canal)").extract()

                    try:
                        play = li.css(".box-assista-no-play a::attr(href)").extract()[0]
                    except:
                        play=""

                    href = li.css("article strong a::attr(href)").extract()
                    link = "http://telecine.globo.com" + str(href[0])

                    request = scrapy.Request(link, callback=self.parse_filme)

                    request.meta['horario'] = horario[0]
                    request.meta['data'] = data
                    request.meta['play'] = play

                    yield request

    def parse_filme(self,response):
        data = response.meta['data']

        horario = response.meta['horario']
        data = time.strftime('%d-%m-%y', data)
        movie_id = telecine.recovery_movie(response, response.meta['play'])

        programacao.insert_programacao(horario, data, movie_id)