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

    # 3. Volume Semanal (Vendas por dia da semana atual)
    # Retorna uma lista de 5 dias (Seg a Sex por exemplo)
    cursor.execute("""
        SELECT DAYOFWEEK(data_venda) as dia, COUNT(*) as qtd
        FROM venda
        WHERE data_venda >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
        GROUP BY dia ORDER BY dia
    """)
    vendas_semanais = cursor.fetchall()

    conn.close()
    return {
        "receita": receita,
        "ranking": ranking,
        "vendas_semanais": vendas_semanais
    }

def buscar_produtos_estoque():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Fazemos JOIN para pegar o nome da marca/categoria das outras tabelas
    query = """
        SELECT 
            e.id_estoque, e.nome_estoque, e.codigo_barras, 
            e.preco_venda, e.quantidade, e.data_validade,
            c.marca, c.nome_categoria
        FROM estoque e
        JOIN categoria c ON e.id_categoria = c.id_categoria
    """
    cursor.execute(query)
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def buscar_usuarios_db():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Buscando os campos conforme o seu CREATE TABLE
    query = "SELECT id_user, nome_user, cpf, email_user, status_user, perfil FROM usuario"
    cursor.execute(query)
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def cadastrar_produto_db(id_fornecedor, id_categoria, nome, codigo, validade, entrada, custo, venda, embalagem, qtd, lote):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO estoque 
        (id_fornecedor, id_categoria, nome_estoque, codigo_barras, data_validade, data_entrada, 
         preco_unitario, preco_venda, embalagem, quantidade, lote)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (id_fornecedor, id_categoria, nome, codigo, validade, entrada, custo, venda, embalagem, qtd, lote)
    cursor.execute(query, valores)
    conn.commit()
    conn.close()

def cadastrar_usuario_db(nome, cpf, email, senha, perfil):
    conn = get_connection()
    cursor = conn.cursor()
    # status_user entra como TRUE por padrão no seu SQL
    query = """
        INSERT INTO usuario (nome_user, cpf, email_user, senha_user, perfil, status_user)
        VALUES (%s, %s, %s, %s, %s, TRUE)
    """
    valores = (nome, cpf, email, senha, perfil)
    cursor.execute(query, valores)
    conn.commit()
    conn.close()

def buscar_produto_por_id(id_prod):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estoque WHERE id_estoque = %s", (id_prod,))
    produto = cursor.fetchone()
    conn.close()
    return produto


def buscar_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Busca apenas os nomes únicos das categorias
    query = "SELECT DISTINCT nome_categoria FROM categoria ORDER BY nome_categoria ASC"
    
    cursor.execute(query)
    # Transforma a lista de tuplas em uma lista simples de strings
    categorias = [linha[0] for linha in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    return categorias

def atualizar_produto_db(id_prod, nome, custo, venda, qtd):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        UPDATE estoque 
        SET nome_estoque = %s, preco_unitario = %s, preco_venda = %s, quantidade = %s
        WHERE id_estoque = %s
    """
    cursor.execute(query, (nome, custo, venda, qtd, id_prod))
    conn.commit()
    conn.close()

def buscar_usuario_por_id(id_user):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_user, nome_user, cpf, email_user, perfil FROM usuario WHERE id_user = %s", (id_user,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def atualizar_usuario_db(id_user, nome, cpf, email, perfil):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        UPDATE usuario 
        SET nome_user = %s, cpf = %s, email_user = %s, perfil = %s
        WHERE id_user = %s
    """
    cursor.execute(query, (nome, cpf, email, perfil, id_user))
    conn.commit()
    conn.close()

def desativar_usuario_db(id_usuario, motivo, senha_protocolo):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Exemplo: Atualiza o status e salva o motivo/senha de reativação
        sql = "UPDATE usuarios SET ativo = 0, motivo_saida = %s, senha_reativacao = %s WHERE id_user = %s"
        cursor.execute(sql, (motivo, senha_protocolo, id_usuario))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao desativar: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def registrar_venda_db(id_user, id_estoque, metodo_pagamento, data_venda):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Insere a venda
        query = "INSERT INTO venda (id_user, id_estoque, metodo_pagamento, data_venda) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (id_user, id_estoque, metodo_pagamento, data_venda))
        
        # Baixa automática no estoque
        cursor.execute("UPDATE estoque SET quantidade = quantidade - 1 WHERE id_estoque = %s", (id_estoque,))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False
    finally:
        conn.close()
