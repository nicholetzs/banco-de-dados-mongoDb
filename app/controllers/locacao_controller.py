from flask import redirect, url_for, request
from bson.objectid import ObjectId


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

    return redirect(url_for('list_carros'))


def devolver_carro(mongo_db, carro_id):
    carro_id = ObjectId(carro_id)
    disponibilidade = request.form.get('disponibilidade') == 'on'

    carros_collection = mongo_db.get_collection("carros")
    carros_collection.update_one(
        {'_id': carro_id}, {'$set': {'DISPONIBILIDADE': disponibilidade}})

    return redirect(url_for('list_carros'))
