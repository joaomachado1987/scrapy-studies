import pymongo
from scrapy.conf import settings

class Programacao():

    def __init__(self):
        print("__INIT__")
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION_PROGRAMACAO']]

    def insert_programacao(self, horario, data, movie_id):

        horario = str(horario)
        dict_programacao = self.collection.find_one({"date": data})

        if(dict_programacao is None):
            movie_id_list = []
            movie_id_list.append(movie_id)
            dict_programacao ={
                "date": data,
                horario: movie_id_list
            }

            self.collection.insert_one(dict_programacao)

        else:
            if(dict_programacao.keys().__contains__(horario)):
                movie_list = dict_programacao[horario]

                if(not movie_list.__contains__(movie_id)):
                    dict_programacao[horario].append(movie_id)
                    self.collection.find_one_and_update({'_id': dict_programacao['_id']}, {"$set": dict_programacao},upsert=False)

            else:
                movie_list = []
                movie_list.append(movie_id)
                dict_programacao[horario] = movie_list
                self.collection.find_one_and_update({'_id': dict_programacao['_id']}, {"$set": dict_programacao}, upsert=False)
