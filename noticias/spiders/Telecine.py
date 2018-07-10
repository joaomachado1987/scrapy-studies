# -*- coding: utf-8 -*-
import scrapy
import imdb
from time import gmtime, strftime
import json
import datetime
import time
import noticias.modules.parse_grade
from noticias.items import FilmesItem

class TecnoblogSpider(scrapy.Spider):
    name = 'Telecine'
    allowed_domains = ['telecine.globo.com', 'telecine.img.estaticos.tv.br']
    start_urls = ['http://telecine.globo.com/programacao/']

    def parse(self, response):

      # for link in response.css('li.aba_dia::attr(data-href)').extract():
      #     print("###########################")
      #     print(link)
      #     request = scrapy.Request(link, callback=self.parse_filmes)
      #     yield request
      link = "http://telecine.img.estaticos.tv.br/rendered/static/grade_htmls/19_07_2018.html"
      request = scrapy.Request(link, callback=self.parse_filmes)
      yield request

    def parse_filmes(self, response):
        ia = imdb.IMDb()
        errors = []
        print("--------------INICIO-------------------")
        url = response.url.split('/')[-1:]

        data = url[0].strip('.html').replace('_', '/')
        data_now = strftime('%d/%m/%Y', gmtime())

        # print(data)
        # print(data_now)
        data = time.strptime(data, "%d/%m/%Y")
        data_now = time.strptime(data_now, "%d/%m/%Y")
        # print(data >= data_now)

        if data >= data_now:
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
                    href = li.css("article strong a::attr(href)").extract()
                    link = "http://telecine.globo.com" + str(href[0])

                    print(link)

                    request = scrapy.Request(link, callback=self.parse_filme)

                    yield request


    def parse_filme(self,response):

        filmes_errors = []

        titulo = response.css('hgroup h1 ::text').extract()
        titulo_original = response.css('hgroup h2 ::text').extract()
        faixa_etaria=response.css('span.cl-etaria ::text')[0].extract().replace('\n','').strip()
        genero=response.css('div.ficha-tecnica a ::text').extract()
        sinopse=response.css('div.box-sinopse p ::text')[1].extract()
        duracao,ano_lancamento,nacionalidade=response.css('div.ficha-tecnica p ::text')[0].extract().split('-')


        try:
            print( " ************** BOM " + titulo_original[0])
            titulo_original = titulo_original[0]
        except:
            print(" ************** RUIM" + titulo[0])
            titulo_original = titulo[0]
            print("Novo titulo original: " + titulo_original)


        ia = imdb.IMDb()
        movies = ia.search_movie(titulo_original)

        for filme in movies:
            dict_imdb = {}
            try:
                print("%%%")
                print(filme.data)
                print(str(ano_lancamento).strip())
                print(str(ano_lancamento).strip() == str(ano_lancamento))

                year = ""
                kind = ""

                try:
                    kind = filme.data['kind']
                    print("kind:" + kind)
                    year = str(filme.data['year'])
                    print("year:" + year)
                except:
                    print("No year or kind to filme: " + filme)

                if(year == str(ano_lancamento).strip() and (kind == "movie" or kind == 'video movie' or kind == 'tv movie')):

                    id = filme.getID()

                    movie = ia.get_movie(id)

                    elenco = []
                    diretores = []

                    try:
                        cast = movie.data['cast'][:3]
                    except:
                        cast=[]

                    try:
                        directors = movie.data['directors']
                    except:
                        diretores=[]
                    try:
                        rating = movie.data['rating']
                    except:
                        rating='-'

                    for person in cast[:5]:
                        cast_dict = {}
                        id = person.getID()
                        name = person.data['name']
                        cast_dict['name'] = name
                        cast_dict['id'] = id
                        elenco.append(cast_dict)

                    for person in directors:
                        cast_dict = {}
                        id = person.getID()
                        name = person.data['name']
                        cast_dict['name'] = name
                        cast_dict['id'] = id
                        diretores.append(cast_dict)

                    dict_imdb = {
                        "rating": rating,
                        "diretores": diretores,
                        "elenco": elenco
                    }

                    print(dict_imdb)

                    break
            except:
                print("error dump: " + titulo[0].strip())

        dict_filmes = {
            "titulo": titulo[0].strip(),
            "titulo_original": titulo_original.strip(),
            "faixa_etaria": faixa_etaria.strip(),
            "genero": genero,
            "sinopse":sinopse.strip(),
            "duracao":duracao.strip(),
            "ano_lancamento":ano_lancamento.strip(),
            "nacionalidade":nacionalidade.strip(),
            "dict_imdb":dict_imdb
        }

        yield dict_filmes