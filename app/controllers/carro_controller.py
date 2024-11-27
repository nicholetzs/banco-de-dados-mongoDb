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
    disponibilidade = request.form.get('disponibilidade', 'off') == 'on'

    carros_collection = mongo_db.get_collection("carros")
    carros_collection.insert_one({
        "MODELO": modelo,
        "ANO": ano,
        "MARCA": marca,
        "DISPONIBILIDADE": disponibilidade
    })

    return redirect(url_for('list_carros'))


def delete_carro(mongo_db, carro_id):
    carro_id = ObjectId(carro_id)
    carros_collection = mongo_db.get_collection("carros")
    locacao_collection = mongo_db.get_collection("locacao")

    locacao_collection.delete_many({'ID_CARRO': carro_id})
    carros_collection.delete_one({'_id': carro_id})

    return redirect(url_for('list_carros'))


def edit_carro(mongo_db, carro_id):
    carro_id = ObjectId(carro_id)

    if request.method == 'POST':
        modelo = request.form['modelo']
        ano = request.form['ano']
        marca = request.form['marca']
        disponibilidade = request.form.get('disponibilidade', 'off') == 'on'

        carros_collection = mongo_db.get_collection("carros")
        carros_collection.update_one(
            {'_id': carro_id},
            {'$set': {'MODELO': modelo, 'ANO': ano, 'MARCA': marca,
                      'DISPONIBILIDADE': disponibilidade}}
        )

        return redirect(url_for('list_carros'))

    carros_collection = mongo_db.get_collection("carros")
    carro = carros_collection.find_one({'_id': carro_id})

    return render_template('edit.html', carro=carro)
