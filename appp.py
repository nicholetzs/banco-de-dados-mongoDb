from flask import Flask
from app.models.mySql import MySql  # Classe para conexão MySQL
from app.models.mongo import MongoDB  # Classe para conexão MongoDB
from app.routes import init_app  # Inicialização das rotas
from app.models.config import Config  # Configurações da aplicação


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
