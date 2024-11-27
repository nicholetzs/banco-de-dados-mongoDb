# 1. Importações padrão
from flask import Flask, render_template

# 2. Importações de pacotes de terceiros (exemplo, se houver algum pacote externo)
# from somepackage import some_module

from .controllers.carro_controller import list_carros, add_carro, delete_carro, edit_carro, alugar_carro, devolver_carro
from .controllers.migracao_controller import migrate_data, list_reservas
from app.models.mongo import MongoDB


def init_app(app, mysql_db, mongo_db):
    @app.route('/')
    def index():
        return render_template('splash_screen.html')

    @app.route('/index')
    def list_carros_route():
        return list_carros(mongo_db)

    @app.route('/add_carro', methods=['POST'])
    def add_carro_route():
        return add_carro(mongo_db)

    @app.route('/delete_carro/<carro_id>', methods=['POST'])
    def delete_carro_route(carro_id):
        return delete_carro(mongo_db, carro_id)

    @app.route('/edit_carro/<carro_id>', methods=['GET', 'POST'])
    def edit_carro_route(carro_id):
        return edit_carro(mongo_db, carro_id)

    @app.route('/alugar_carro/<carro_id>', methods=['POST'])
    def alugar_carro_route(carro_id):
        return alugar_carro(mongo_db, carro_id)

    @app.route('/devolver_carro/<carro_id>', methods=['POST'])
    def devolver_carro_route(carro_id):
        return devolver_carro(mongo_db, carro_id)

    @app.route('/transfer', methods=['POST'])
    def migrate_data_route():
        return migrate_data(mysql_db, mongo_db)

    @app.route('/relatorios')
    def list_reservas_route():
        return list_reservas(mongo_db)
