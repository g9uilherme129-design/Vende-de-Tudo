import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",      # Seu usuário do MySQL
        password="",      # Sua senha do MySQL
        database="sistema_vendas"
    )

def buscar_dados_home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Receita Total do Mês Atual
    cursor.execute("""
        SELECT SUM(e.preco_venda) as total 
        FROM venda v
        JOIN estoque e ON v.id_estoque = e.id_estoque
        WHERE MONTH(v.data_venda) = MONTH(CURRENT_DATE())
    """)
    receita = cursor.fetchone()['total'] or 0.0

    # 2. Ranking de Vendedores (Top 3)
    cursor.execute("""
        SELECT u.nome_user, COUNT(v.id_venda) as qtd_vendas, SUM(e.preco_venda) as valor_total
        FROM usuario u
        LEFT JOIN venda v ON u.id_user = v.id_user
        LEFT JOIN estoque e ON v.id_estoque = e.id_estoque
        GROUP BY u.id_user
        ORDER BY valor_total DESC
        LIMIT 3
    """)
    ranking = cursor.fetchall()

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

