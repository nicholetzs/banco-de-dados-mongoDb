# app.py ou __init__.py

from flask import Flask
from mySqlConnection import MySql  # Classe para conexão MySQL
from mongo import MongoDB  # Classe para conexão MongoDB
from transfer import transfer_all  # Funções de transferência
from config import Config  # Configurações gerais


def create_app():
    """
    Cria e configura a aplicação Flask com as dependências necessárias.
    :return: Instância da aplicação Flask
    """
    # Criando a instância do Flask
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuração do banco de dados MySQL
    mysql_db = MySql(app.config['DB_CONFIG'])

    # Configuração do MongoDB
    mongo_db = MongoDB(
        uri=app.config['MONGO_URI'],
        database=app.config['MONGO_DATABASE']
    )

    # Transferindo dados entre MySQL e MongoDB
    tables = ["CARROS", "CLIENTES", "LOCACAO"]
    transfer_all(mysql_db, mongo_db, tables)

    return app
