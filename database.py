import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",      
        password="",      
        database="sistema_vendas"
    )


def buscar_dados_home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Receita Total (Soma de Qtd x Preço) - Convertido para float
    cursor.execute("""
        SELECT SUM(v.quantidade_vendida * v.preco_venda) as total 
        FROM venda v
        WHERE MONTH(v.data_venda) = MONTH(CURRENT_DATE())
          AND YEAR(v.data_venda) = YEAR(CURRENT_DATE())
    """)
    res_receita = cursor.fetchone()
    # O float() aqui resolve o erro de serialização do Decimal
    receita = float(res_receita['total']) if res_receita['total'] else 0.0

    # 2. Ranking de Vendedores (Convertendo valor_total para float)
    cursor.execute("""
        SELECT 
            u.nome_user, 
            SUM(v.quantidade_vendida) as qtd_vendas, 
            SUM(v.quantidade_vendida * v.preco_venda) as valor_total
        FROM usuario u
        INNER JOIN venda v ON u.id_user = v.id_user
        WHERE MONTH(v.data_venda) = MONTH(CURRENT_DATE())
        GROUP BY u.id_user
        ORDER BY valor_total DESC
        LIMIT 3
    """)
    ranking_raw = cursor.fetchall()
    # Criamos uma lista nova convertendo os Decimals para float
    ranking = []
    for r in ranking_raw:
        ranking.append({
            "nome_user": r["nome_user"],
            "qtd_vendas": int(r["qtd_vendas"]), # Garante que é número inteiro
            "valor_total": float(r["valor_total"]) if r["valor_total"] else 0.0
        })

    # 3. Volume Semanal (SOMA DE PRODUTOS: Os 2394 que você quer)
    cursor.execute("""
        SELECT 
            DAYOFWEEK(data_venda) as dia, 
            SUM(quantidade_vendida) as qtd
        FROM venda
        WHERE data_venda >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
        GROUP BY dia 
        ORDER BY dia
    """)
    vendas_raw = cursor.fetchall()
    # Converte as quantidades para float/int para o Flet não reclamar
    vendas_semanais = []
    for v in vendas_raw:
        vendas_semanais.append({
            "dia": v["dia"],
            "qtd": float(v["qtd"]) if v["qtd"] else 0.0
        })

    conn.close()
    return {"receita": receita, "ranking": ranking, "vendas_semanais": vendas_semanais}

# --- 2. FUNÇÕES DO ESTOQUE ---
def buscar_produtos_estoque():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT e.id_estoque, e.nome_estoque, e.codigo_barras, 
               e.preco_venda, e.quantidade, e.data_validade,
               c.marca, c.nome_categoria
        FROM estoque e
        JOIN categoria c ON e.id_categoria = c.id_categoria
    """
    cursor.execute(query)
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def buscar_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT nome_categoria FROM categoria ORDER BY nome_categoria ASC")
    categorias = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return categorias

def cadastrar_produto_db(id_fornecedor, id_categoria, nome, codigo, validade, entrada, custo, venda, embalagem, qtd, lote):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO estoque (id_fornecedor, id_categoria, nome_estoque, codigo_barras, data_validade, 
        data_entrada, preco_unitario, preco_venda, embalagem, quantidade, lote)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (id_fornecedor, id_categoria, nome, codigo, validade, entrada, custo, venda, embalagem, qtd, lote))
    conn.commit()
    conn.close()

def buscar_produto_por_id(id_prod):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estoque WHERE id_estoque = %s", (id_prod,))
    produto = cursor.fetchone()
    conn.close()
    return produto

def atualizar_produto_db(id_prod, nome, custo, venda, qtd):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE estoque SET nome_estoque = %s, preco_unitario = %s, preco_venda = %s, quantidade = %s WHERE id_estoque = %s"
    cursor.execute(query, (nome, custo, venda, qtd, id_prod))
    conn.commit()
    conn.close()

# --- 3. FUNÇÕES DE USUÁRIO ---
def buscar_usuarios_db():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_user, nome_user, cpf, email_user, status_user, perfil FROM usuario")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def cadastrar_usuario_db(nome, cpf, email, senha, perfil):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO usuario (nome_user, cpf, email_user, senha_user, perfil, status_user) VALUES (%s, %s, %s, %s, %s, TRUE)"
    cursor.execute(query, (nome, cpf, email, senha, perfil))
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
    query = "UPDATE usuario SET nome_user = %s, cpf = %s, email_user = %s, perfil = %s WHERE id_user = %s"
    cursor.execute(query, (nome, cpf, email, perfil, id_user))
    conn.commit()
    conn.close()

# FUNÇÃO QUE RESOLVE O SEU ERRO DE IMPORTAÇÃO
def desativar_usuario_db(id_usuario, motivo=None, senha_protocolo=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = "UPDATE usuario SET status_user = 0 WHERE id_user = %s"
        cursor.execute(sql, (id_usuario,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao desativar: {e}")
        return False
    finally:
        conn.close()

# --- 4. FUNÇÕES DE VENDA ---
def registrar_venda_db(id_user, id_estoque, qtd, metodo, preco_venda):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT quantidade FROM estoque WHERE id_estoque = %s", (id_estoque,))
        prod = cursor.fetchone()
        if not prod or prod[0] < qtd: return False, "Estoque insuficiente!"
        
        query = "INSERT INTO venda (id_user, id_estoque, quantidade_vendida, metodo_pagamento, preco_venda, data_venda) VALUES (%s, %s, %s, %s, %s, NOW())"
        cursor.execute(query, (id_user, id_estoque, qtd, metodo, preco_venda))
        cursor.execute("UPDATE estoque SET quantidade = quantidade - %s WHERE id_estoque = %s", (qtd, id_estoque))
        conn.commit()
        return True, "Venda realizada!"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def buscar_vendas_detalhadas():
    conn = get_connection() 
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT v.id_venda, v.data_venda, v.quantidade_vendida, v.preco_venda, v.metodo_pagamento,
               e.nome_estoque as produto, u.nome_user as vendedor
        FROM venda v
        JOIN estoque e ON v.id_estoque = e.id_estoque
        JOIN usuario u ON v.id_user = u.id_user
        ORDER BY v.id_venda DESC
    """
    cursor.execute(query)
    vendas = cursor.fetchall()
    conn.close()
    return vendas