import psycopg2
import json

host = "localhost"
database = "tp2"
user = "postgres"
password = "postgres"



def select_db():
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    table = "tabela"

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tabela")
    colunas = [desc[0] for desc in cursor.description]
    dados = {table: {coluna: [] for coluna in colunas}}
    for row in cursor.fetchall():
        for coluna, valor in zip(colunas, row):
            dados[table][coluna].append(valor)
    cursor.close()
    connection.close() 
    
    print(json.dumps(dados, indent=4))

def start_db():
    json_data = {
        "tabela": {
            "id": [1, 2],
            "A": [20, 20],
            "B": [55, 30],
            "C": [15, 90]
        }
    }

    table = "tabela"

    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = connection.cursor()
    colunas = list(json_data["tabela"].keys())
    create_table_query = f"CREATE TABLE {table} ({', '.join([f'{coluna} INT' for coluna in colunas])});"
    cursor.execute(create_table_query)

    for i in range(len(json_data["tabela"]["id"])):
        valores = [json_data["tabela"][coluna][i] for coluna in colunas]
        insert_query = f"INSERT INTO {table} ({', '.join(colunas)}) VALUES ({', '.join(['%s' for _ in colunas])});"
        cursor.execute(insert_query, valores)
    connection.commit()
    cursor.close()
    connection.close()


def commit(id, coluna, valor):
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    
    cursor = connection.cursor()
    
    cursor.execute("select id from tabela where id = (%s)", (id))
    resultados = cursor.fetchall()
    if not resultados:
        cursor.execute("INSERT INTO tabela (id, {}) VALUES (%s, %s)".format(coluna), (id, valor))
    else:
        cursor.execute("UPDATE tabela SET {} = %s WHERE id = %s".format(coluna), (valor, id))
        print("Coluna {} foi atualizada com o valor {}".format(coluna, valor))


    connection.commit()
    if connection:
        cursor.close()
        connection.close()
        
def NOW_GO_AND_JUST_DROP_IT():
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    cursor = connection.cursor()
    cursor.execute("drop table tabela")

    connection.commit()
    if connection:
        cursor.close()
        connection.close()
    



    