from datetime import datetime, date
from decimal import Decimal


def convert_data_types(record):
    """
    Converte os tipos de dados de um registro para os tipos compatíveis com MongoDB.
    :param record: Dicionário de dados do MySQL.
    :return: Registro convertido para o formato MongoDB.
    """
    for key, value in record.items():
        # Verifica se o campo é um ID e preserva como inteiro
        if "id" in key.lower() and isinstance(value, int):
            continue  # Mantém o ID como está

        # Convertendo tipos DATE ou DATETIME para strings compatíveis com MongoDB
        elif isinstance(value, (date, datetime)):
            # Converte para formato ISO 8601 (string)
            record[key] = value.isoformat()

        # Convertendo apenas o campo DISPONIBILIDADE
        elif key.lower() == "disponibilidade" and isinstance(value, int) and value in [0, 1]:
            record[key] = bool(value)

        # Convertendo valores DECIMAL para float
        elif isinstance(value, Decimal):  # Certifique-se de importar Decimal
            record[key] = float(value)

    return record
