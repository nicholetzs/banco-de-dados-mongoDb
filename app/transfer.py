from app.utils.convert_data_types import convert_data_types


def transfer_all(mysql_db, mongo_db, tables):
    """
    Transfere os dados de várias tabelas do MySQL para o MongoDB.
    :param mysql_db: Instância da classe Database para conexão com o MySQL.
    :param mongo_db: Instância da classe MongoDB para acesso à coleção.
    :param tables: Lista de nomes de tabelas no MySQL.
    """
    for table in tables:
        transfer_table(mysql_db, mongo_db, table)


def transfer_table(mysql_db, mongo_db, table_name):
    """
    Transfere os dados de uma tabela do MySQL para uma coleção no MongoDB.
    :param mysql_db: Instância da classe Database para conexão com o MySQL.
    :param mongo_db: Instância da classe MongoDB para acesso à coleção.
    :param table_name: Nome da tabela no MySQL.
    """
    try:
        # Conectando ao MySQL e buscando dados
        mysql_conn = mysql_db.get_connection()
        cursor = mysql_conn.cursor(dictionary=True)
        print(f"Buscando dados da tabela {table_name} no MySQL...")
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        if rows:
            # Convertendo os tipos de dados dos registros antes de inserir no MongoDB
            converted_rows = [convert_data_types(record) for record in rows]

            # Inserindo dados no MongoDB (sem referência direta ao campo `ID`)
            collection = mongo_db.get_collection(
                table_name.lower())  # Coleção com nome da tabela
            print(f"Inserindo {len(converted_rows)} registros na coleção {
                  table_name.lower()} no MongoDB...")

            for record in converted_rows:
                # Salvar o ID original do MySQL em `mysql_id` (opcional)
                if "ID" in record:
                    record["mysql_id"] = record.pop("ID")

                # Inserir o registro com `_id` gerado automaticamente pelo MongoDB
                result = collection.insert_one(record)
                print(f"Registro inserido com _id {
                      result.inserted_id} no MongoDB.")

            print(f"Transferência da tabela {
                  table_name} concluída com sucesso!")
        else:
            print(f"Nenhum dado encontrado na tabela {table_name}.")

    except Exception as e:
        print(f"Erro durante a transferência de {table_name}: {e}")
    finally:
        if mysql_conn:
            mysql_conn.close()
