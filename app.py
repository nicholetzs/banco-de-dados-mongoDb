from flask import Flask
from mySql import MySql  # Classe para conexão MySQL
from mongo import MongoDB  # Classe para conexão MongoDB
from routes import init_app  # Rotas da aplicação
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

    # Inicializa as rotas, passando as conexões necessárias
    init_app(app, mysql_db, mongo_db)
    return app
