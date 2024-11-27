from flask import jsonify
from ..transfer import transfer_all


def migrate_data(mysql_db, mongo_db):
    try:
        tables = ["CARROS", "CLIENTES", "LOCACAO"]
        transfer_all(mysql_db, mongo_db, tables)
        return jsonify({"message": "Migração concluída com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": f"Erro durante a migração: {str(e)}"}), 500
