import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        self.config ={
            'host':"localhost",
            'user':"root",
            'password':"",
            'database':"sistema_vendas"
        }

    def conectar(self):
        return mysql.connector.connect(**self.config)

    def inserir_estoque(self, nome, codigo, id_fornecedor, id_categoria, validade, data_entrada, preco_custo, preco_venda, embalagem, qtd, lote):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = """
                INSERT INTO estoque 
                (id_fornecedor, id_categoria, nome_estoque, codigo_barras, data_validade, 
                data_entrada, preco_unitario, preco_venda, embalagem, quantidade, lote) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data_entrada = datetime.now().strftime('%Y-%M-%D')

            valores = (
                id_fornecedor, id_categoria, nome, codigo, validade,
                data_entrada, preco_custo, preco_venda, embalagem, qtd, lote
            )

            cursor.execute(sql, (nome, codigo, id_fornecedor, id_categoria))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro no MySQL: {e}")
            return False