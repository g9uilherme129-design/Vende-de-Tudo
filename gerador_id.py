import random
import string
from database import get_connection

def gerar_id_unico(tabela, coluna):
    #define os prefixos para cada tipo de tabela
    prefixos ={
        "usuario":"U",
        "categoria":"C",
        "fornecedor":"F",
        "estoque":"E",
        "venda":"V",
        "tema":"T"
    }

    prefixo = prefixos.get(tabela, "X")

    conn = get_connection()
    cursor = conn.cursor()

    while True:
        aleatorio = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        novo_id =f"{prefixo}{aleatorio}"

        query = f"SELECT COUT(*) FROM {tabela} WHERE {coluna} =%s"
        cursor.execute(query, (novo_id))
        existe = cursor.fetchone()[0]

        if existe == 0:
            conn.close()
            return novo_id