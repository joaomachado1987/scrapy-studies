import time
from ensurepip import __main__

import imdb
import datetime
import json
from time import strftime, gmtime
from noticias.items import FilmesItem

def parse_grade(self, response):
    ia = imdb.IMDb()
    errors = []
    print("--------------INICIO-------------------")
    url = response.url.split('/')[-1:]

    data = url[0].strip('.html').replace('_', '/')
    data_now = strftime('%d/%m/%Y', gmtime())

    print(data)
    print(data_now)
    data = time.strptime(data, "%d/%m/%Y")
    data_now = time.strptime(data_now, "%d/%m/%Y")
    print(data >= data_now)

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

                try:
                    movies = ia.search_movie(str(title))
                    first_movie = movies[0]
                    id = first_movie.getID()

                    movie = ia.get_movie(id)

                    elenco = []
                    diretores = []

                    cast = movie.data['cast'][:3]
                    directors = movie.data['directors']
                    year = movie.data['year']
                    rating = movie.data['rating']
                    # writer = movie.data['writer']
                    genres = movie.data['genres']

                    print(cast)

                    for person in cast:
                        cast_dict = {}
                        id = person.getID()
                        name = person.data['name']
                        cast_dict['name'] = name
                        cast_dict['id'] = id
                        print(cast_dict)
                        elenco.append(cast_dict)

                    for person in directors:
                        cast_dict = {}
                        id = person.getID()
                        name = person.data['name']
                        cast_dict['name'] = name
                        cast_dict['id'] = id
                        print(cast_dict)
                        diretores.append(cast_dict)

                    print(elenco)
                    print(title)
                    print(sinopse)
                    print(canal)
                    print(play)
                    print(data)
                    print(elenco)
                    print(diretores)
                    print(year)
                    print(rating)
                    # print(writer)
                    print(genres)

                    yield FilmesItem(title=title,
                                     hora=horario,
                                     canal=canal,
                                     sinopse=sinopse,
                                     play=play,
                                     data=data,
                                     cast=elenco,
                                     directors=diretores,
                                     year=year,
                                     rating=rating,
                                     # writer = writer,
                                     genres=genres
                                     )
                except:
                    print(" $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ")
                    errors.append(str(title))
                    print(errors)
                    print(" $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ")

                print("*****************************")

        with open("errors-" + str(datetime.datetime.now()).replace(':', '-') + ".txt", "w") as file:
            json.dump(errors, file, ensure_ascii=False)

def teste():
    ia = imdb.IMDb()
    movies = ia.search_movie('furious 6')

    for filme in movies:
        if(str(filme.data['year']) == '2013' and filme.data['kind'] == "movie"):
            id = filme.getID()

            movie = ia.get_movie(id)

            elenco = []
            diretores = []

            cast = movie.data['cast'][:3]
            directors = movie.data['directors']
            rating = movie.data['rating']

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

            dict_imdb ={
                "rating":rating,
                "diretores":diretores,
                "elenco":elenco
            }

            print(rating)
            print(diretores)
            print(elenco)

            return dict_imdb

if __name__ == '__main__':
    teste()
