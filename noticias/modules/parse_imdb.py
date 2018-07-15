import imdb
import pymongo
from scrapy.conf import settings

ia = imdb.IMDb()

class IMDB():

    def __init__(self):
        print("__INIT__ IMDB ******************")
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION_IMDB']]

    def parse_imdb(self, titulo_original, ano_lancamento):

        dict_imdb_movie = self.collection.find_one({"titulo_original": titulo_original})

        if(dict_imdb_movie is None):

            movies = ia.search_movie(titulo_original)

            for filme in movies:

                try:

                    year = ""
                    kind = ""

                    try:
                        kind = filme.data['kind']
                        year = str(filme.data['year'])
                    except:
                        print("No year or kind to filme: " + filme.data['title'])

                    if (year == str(ano_lancamento).strip() and (
                            kind == "movie" or kind == 'video movie' or kind == 'tv movie')):

                        idImdb = filme.getID()

                        movie = ia.get_movie(idImdb)

                        movie.data

                        elenco = []
                        diretores = []

                        try:
                            cast = movie.data['cast'][:3]
                        except:
                            cast = []

                        try:
                            directors = movie.data['directors']
                        except:
                            diretores = []
                        try:
                            rating = movie.data['rating']
                        except:
                            rating = ''

                        try:
                            cast = movie.data['cast']
                        except:
                            cast = ''

                        try:
                            synopsis = movie.data['synopsis']
                        except:
                            synopsis = ''

                        try:
                            plot = movie.data['plot']
                        except:
                            plot = ''

                        try:
                            cover_url = movie.data['cover url']
                        except:
                            cover_url= ''

                        try:
                            votes = movie.data['votes']
                        except:
                            votes = ''

                        try:
                            countries = movie.data['countries']
                        except:
                            countries = ''

                        try:
                            fullSizeURL = movie.get_fullsizeURL()
                        except:
                            fullSizeURL = ''

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


                        dict_imdb_movie = {
                            "titulo_original" : titulo_original,

                            "dict_imdb" : {
                                "id_film_imdb":idImdb,
                                "title":filme.data['title'],
                                "rating": rating,
                                "diretores": diretores,
                                "elenco": elenco,
                                "synopsis": synopsis,
                                "plot":plot,
                                "cover_url":cover_url,
                                "votes":votes,
                                "countries": countries,
                                "fullSizeURL":fullSizeURL
                            }
                        }

                        dict_imdb_movie = self.collection.insert_one(dict(dict_imdb_movie))

                        return dict_imdb_movie.inserted_id
                except:
                    print("error dump: " + filme.data['title'])
        else:
            return dict_imdb_movie['_id']