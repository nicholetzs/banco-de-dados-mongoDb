from flask import render_template
from app.models.mongo import MongoDB


def list_reservas(mongo_db):
    locacao_collection = mongo_db.get_collection("locacao")
    carros_collection = mongo_db.get_collection("carros")
    clientes_collection = mongo_db.get_collection("clientes")

    reservas = list(locacao_collection.aggregate([
        {
            '$addFields': {
                'ID_CLIENTE': {'$toObjectId': '$ID_CLIENTE'}
            }
        },
        {
            '$lookup': {
                'from': 'carros',
                'localField': 'ID_CARRO',
                'foreignField': '_id',
                'as': 'carro_info'
            }
        },
        {
            '$lookup': {
                'from': 'clientes',
                'localField': 'ID_CLIENTE',
                'foreignField': '_id',
                'as': 'cliente_info'
            }
        }
    ]))

    total_locacoes = locacao_collection.count_documents({})

    return render_template('relatorios.html', reservas=reservas, total_locacoes=total_locacoes)
