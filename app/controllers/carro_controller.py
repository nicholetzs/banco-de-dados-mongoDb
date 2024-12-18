from datetime import datetime
from flask import request, redirect, url_for
from bson import ObjectId
from flask import render_template, request, redirect, url_for
from bson.objectid import ObjectId
from app.models.mongo import MongoDB


def list_carros(mongo_db):
    carros_collection = mongo_db.get_collection("carros")
    clientes_collection = mongo_db.get_collection("clientes")

    carros = list(carros_collection.find())
    clientes = list(clientes_collection.find())

    for carro in carros:
        carro['_id'] = str(carro['_id'])

    return render_template('index.html', carros=carros, clientes=clientes)


def add_carro(mongo_db):
    modelo = request.form['modelo']
    ano = request.form['ano']
    marca = request.form['marca']
    disponibilidade = request.form.get('disponibilidade', 'on') == 'on'

    carros_collection = mongo_db.get_collection("carros")
    carros_collection.insert_one({
        "MODELO": modelo,
        "ANO": ano,
        "MARCA": marca,
        "DISPONIBILIDADE": disponibilidade
    })

    return redirect(url_for('list_carros_route'))


def delete_carro(mongo_db, carro_id):
    carro_id = ObjectId(carro_id)
    carros_collection = mongo_db.get_collection("carros")
    locacao_collection = mongo_db.get_collection("locacao")

    locacao_collection.delete_many({'ID_CARRO': carro_id})
    carros_collection.delete_one({'_id': carro_id})

    return redirect(url_for('list_carros_route'))


def edit_carro(mongo_db, carro_id):
    carro_id = ObjectId(carro_id)

    # Quando o formulário for submetido (POST)
    if request.method == 'POST':
        modelo = request.form['modelo']
        ano = request.form['ano']
        marca = request.form['marca']

        # Verifica se a disponibilidade foi marcada como 'on'
        disponibilidade = request.form.get('disponibilidade', 'off') == 'on'

        carros_collection = mongo_db.get_collection("carros")
        locacao_collection = mongo_db.get_collection("locacao")

        # Atualiza as informações do carro na coleção de carros
        carros_collection.update_one(
            {'_id': carro_id},
            {'$set': {'MODELO': modelo, 'ANO': ano, 'MARCA': marca,
                      'DISPONIBILIDADE': disponibilidade}}
        )

        # Se o carro foi marcado como disponível, exclui a locação associada
        if disponibilidade:
            # Remove todas as locações onde o ID do carro seja igual ao carro editado
            locacao_collection.delete_many({'ID_CARRO': carro_id})

        # Redireciona para a lista de carros após a edição
        return redirect(url_for('list_carros_route'))

    # Caso o método seja GET, apenas exibe a página de edição
    carros_collection = mongo_db.get_collection("carros")
    carro = carros_collection.find_one({'_id': carro_id})

    return render_template('edit.html', carro=carro)


def alugar_carro(mongo_db, carro_id):
    carro_id = ObjectId(carro_id)
    cliente_id = request.form.get('id_cliente')
    data_locacao = request.form.get('data_locacao')
    data_retorno = request.form.get('data_retorno')
    valor_diaria = request.form.get('valor_diaria')

    carros_collection = mongo_db.get_collection("carros")
    locacao_collection = mongo_db.get_collection("locacao")

    carro = carros_collection.find_one({'_id': carro_id})
    if not carro:
        return "O carro não foi encontrado."
    if not carro['DISPONIBILIDADE']:
        return "O carro já está alugado ou indisponível."

    locacao_collection.insert_one({
        'ID_CARRO': carro_id,
        'ID_CLIENTE': cliente_id,
        'DATA_LOCACAO': data_locacao,
        'DATA_RETORNO': data_retorno,
        'VALOR_DIARIA': valor_diaria
    })

    carros_collection.update_one(
        {'_id': carro_id}, {'$set': {'DISPONIBILIDADE': False}})

    return redirect(url_for('list_carros_route'))
