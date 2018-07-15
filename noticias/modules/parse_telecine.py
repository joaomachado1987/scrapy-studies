import pymongo
import pymongo
from scrapy.conf import settings
from noticias.modules.parse_imdb import IMDB

imdb = IMDB()

class Telecine():

    def __init__(self):
        print("__INIT__")
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION_TELECINE']]

    def recovery_movie(self, response, play):
        titulo = response.css('hgroup h1 ::text').extract()

        titulo = titulo[0].strip()

        dict_filmes = self.collection.find_one({"titulo": titulo})

        if (dict_filmes is None):

            titulo_original = response.css('hgroup h2 ::text').extract()

            try:
                cartaz = response.css('figure.crop.fl img::attr(src)').extract()[0]
            except:
                cartaz = ''

            try:
                faixa_etaria = response.css('span.cl-etaria ::text')[0].extract().replace('\n', '').strip()
            except:
                faixa_etaria = ''

            try:
                genero = response.css('div.ficha-tecnica a ::text').extract()
            except:
                genero = ""

            try:
                elenco_diretoes_atores = response.css('div.box-artistas p ::text').extract()

                elenco_diretoes_atores = [e.strip() for e in elenco_diretoes_atores]

                diretores = []

                i = 0

                for a in elenco_diretoes_atores:
                    i = i + 1
                    if (a == 'Diretor:'):
                        continue
                    elif (a == 'Atores:'):
                        break
                    else:
                        diretores.append(a)

                atores = elenco_diretoes_atores[i::]

                diretores = [a.strip().strip(',') for a in diretores]
                diretores = [a for a in diretores if a != '']

                atores = [a.strip().strip(',') for a in atores]
                atores = [a for a in atores if a != '']
            except:
                diretores = []
                atores = []

            try:
                sinopse = response.css('div.box-sinopse p ::text')[1].extract()
            except:
                sinopse = 'sinopse não informada pela programação do telecine.'

            try:
                duracao, ano_lancamento, nacionalidade = response.css('div.ficha-tecnica p ::text')[0].extract().split(
                    '-')
            except:
                duracao, ano_lancamento = response.css('div.ficha-tecnica p ::text')[0].extract().split('-')
                nacionalidade = ""

            try:
                titulo_original = titulo_original[0]
            except:
                titulo_original = titulo[0]

            titulo_original = titulo_original.strip()

            dict_filmes = {
                "url": response._url,
                "titulo": titulo,
                "titulo_original": titulo_original,
                "faixa_etaria": faixa_etaria.strip(),
                "genero": genero,
                "sinopse": sinopse.strip(),
                "duracao": duracao.strip(),
                "ano_lancamento": ano_lancamento.strip(),
                "nacionalidade": nacionalidade.strip(),
                "diretor": diretores,
                "atores": atores,
                "cartaz": cartaz,
                "play": play,
                "dict_imdb": imdb.parse_imdb(titulo_original, ano_lancamento)
            }

            dict_filmes_base = self.collection.insert_one(dict(dict_filmes))

            return dict_filmes_base.inserted_id
        else:
            return dict_filmes["_id"]