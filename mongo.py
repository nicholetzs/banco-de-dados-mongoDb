from pymongo import MongoClient


class MongoDB:
    def __init__(self, uri, database):
        """
        Inicializa a conexão com o MongoDB.
        :param uri: URI de conexão do MongoDB.
        :param database: Nome do banco de dados no MongoDB.
        """
        self.client = MongoClient(uri)
        self.database = self.client[database]

    def get_collection(self, collection_name):
        """
        Retorna uma coleção do MongoDB.
        :param collection_name: Nome da coleção.
        :return: Instância da coleção no MongoDB.
        """
        return self.database[collection_name]
