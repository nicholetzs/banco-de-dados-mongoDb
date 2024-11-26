from flask import render_template, request, redirect, url_for
from flask import jsonify
from transfer import transfer_all
from bson.objectid import ObjectId


def init_app(app, mysql_db, mongo_db):
    @app.route('/')
    def index():
        # Exibindo a splash screen com informações sobre nossa locadora
        return render_template('splash_screen.html')

    @app.route('/index')
    def list_carros():
        # Buscando carros e clientes no MongoDB
        carros_collection = mongo_db.get_collection("carros")
        clientes_collection = mongo_db.get_collection("clientes")

        carros = list(carros_collection.find())
        clientes = list(clientes_collection.find())

        # Convertendo ObjectId para string para exibição
        for carro in carros:
            carro['_id'] = str(carro['_id'])

        return render_template('index.html', carros=carros, clientes=clientes)

    @app.route('/transfer', methods=['POST'])
    def migrate_data():
        """
        Rota para executar a migração de dados do MySQL para o MongoDB.
        """
        try:
            # Definindo as tabelas a serem migradas
            tables = ["CARROS", "CLIENTES", "LOCACAO"]
            # Executando a transferência
            transfer_all(mysql_db, mongo_db, tables)
            return jsonify({"message": "Migração concluída com sucesso!"}), 200
        except Exception as e:
            return jsonify({"error": f"Erro durante a migração: {str(e)}"}), 500

    @app.route('/add_carro', methods=['POST'])
    def add_carro():
        modelo = request.form['modelo']
        ano = request.form['ano']
        marca = request.form['marca']
        disponibilidade = request.form.get('disponibilidade', 'off') == 'on'

        # Inserindo carro na coleção CARROS do MongoDB
        carros_collection = mongo_db.get_collection("carros")
        carros_collection.insert_one({
            "MODELO": modelo,
            "ANO": ano,
            "MARCA": marca,
            "DISPONIBILIDADE": disponibilidade
        })

        return redirect(url_for('list_carros'))

    @app.route('/delete_carro/<carro_id>', methods=['POST'])
    def delete_carro(carro_id):
        # Convertendo carro_id para ObjectId
        carro_id = ObjectId(carro_id)

        # Deletando o carro da coleção CARROS e as locações associadas no MongoDB
        carros_collection = mongo_db.get_collection("carros")
        locacao_collection = mongo_db.get_collection("locacao")

        # Deletando locação associada ao carro
        locacao_collection.delete_many({'ID_CARRO': carro_id})

        # Deletando o carro
        carros_collection.delete_one({'_id': carro_id})

        return redirect(url_for('list_carros'))

    @app.route('/edit_carro/<carro_id>', methods=['GET', 'POST'])
    def edit_carro(carro_id):
        # Convertendo carro_id para ObjectId
        carro_id = ObjectId(carro_id)

        if request.method == 'POST':
            modelo = request.form['modelo']
            ano = request.form['ano']
            marca = request.form['marca']
            disponibilidade = request.form.get(
                'disponibilidade', 'off') == 'on'

            # Atualizando carro no MongoDB
            carros_collection = mongo_db.get_collection("carros")
            carros_collection.update_one(
                {'_id': carro_id},
                {'$set': {'MODELO': modelo, 'ANO': ano, 'MARCA': marca,
                          'DISPONIBILIDADE': disponibilidade}}
            )

            return redirect(url_for('list_carros'))

        # Buscando carro específico no MongoDB
        carros_collection = mongo_db.get_collection("carros")
        carro = carros_collection.find_one({'_id': carro_id})

        return render_template('edit.html', carro=carro)

    @app.route('/alugar_carro/<carro_id>', methods=['POST'])
    def alugar_carro(carro_id):
        # Convertendo carro_id para ObjectId
        carro_id = ObjectId(carro_id)

        # Coletando dados do formulário
        cliente_id = request.form.get('id_cliente')
        data_locacao = request.form.get('data_locacao')
        data_retorno = request.form.get('data_retorno')
        valor_diaria = request.form.get('valor_diaria')

        # Conectando às coleções
        carros_collection = mongo_db.get_collection("carros")
        locacao_collection = mongo_db.get_collection("locacao")

        # Verificando disponibilidade do carro
        carro = carros_collection.find_one({'_id': carro_id})
        if not carro:
            return "O carro não foi encontrado."
        if not carro['DISPONIBILIDADE']:
            return "O carro já está alugado ou indisponível."

        # Inserindo a locação no MongoDB
        locacao_collection.insert_one({
            'ID_CARRO': carro_id,  # Agora usa o ObjectId
            'ID_CLIENTE': cliente_id,
            'DATA_LOCACAO': data_locacao,
            'DATA_RETORNO': data_retorno,
            'VALOR_DIARIA': valor_diaria
        })

        # Atualizando a disponibilidade do carro
        carros_collection.update_one(
            {'_id': carro_id},
            {'$set': {'DISPONIBILIDADE': False}}
        )

        return redirect(url_for('list_carros'))

    @app.route('/devolver_carro/<carro_id>', methods=['POST'])
    def devolver_carro(carro_id):
        # Convertendo carro_id para ObjectId
        carro_id = ObjectId(carro_id)

        disponibilidade = request.form.get('disponibilidade') == 'on'

        # Atualizando disponibilidade do carro
        carros_collection = mongo_db.get_collection("carros")
        carros_collection.update_one(
            {'_id': carro_id},
            {'$set': {'DISPONIBILIDADE': disponibilidade}}
        )

        return redirect(url_for('list_carros'))

    @app.route('/relatorios')
    def list_reservas():
        # Buscando relatórios de locações no MongoDB
        locacao_collection = mongo_db.get_collection("locacao")
        carros_collection = mongo_db.get_collection("carros")
        clientes_collection = mongo_db.get_collection("clientes")

        reservas = list(locacao_collection.aggregate([
            {
                '$lookup': {
                    'from': 'carros',
                    'localField': 'ID_CARRO',
                    'foreignField': '_id',  # Usando _id para fazer lookup
                    'as': 'carro_info'
                }
            },
            {
                '$lookup': {
                    'from': 'clientes',
                    'localField': 'ID_CLIENTE',
                    'foreignField': '_id',  # Usando _id para fazer lookup
                    'as': 'cliente_info'
                }
            }
        ]))

        total_locacoes = locacao_collection.count_documents({})

        # Verifique a estrutura de 'reservas' no terminal
        print("Reservas: ", reservas)

        return render_template('relatorios.html', reservas=reservas, total_locacoes=total_locacoes)
