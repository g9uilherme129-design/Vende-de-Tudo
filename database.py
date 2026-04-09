import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",      
        password="",      
        database="sistema_vendas"
    )

# --- GERADOR DE ID PARA VARCHAR(7) ---
def gerar_id_char(tabela, coluna_id, prefixo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
    qtd = cursor.fetchone()[0]
    conn.close()
    return f"{prefixo}{100000 + qtd + 1}"


def garantir_dependencias():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM categoria")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO categoria VALUES ('C100001', 'Geral', 'Diversos', 'Generica', 1)")
        
        cursor.execute("SELECT COUNT(*) FROM fornecedor")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO fornecedor VALUES ('F100001', 'Fornecedor Padrao', '00000000000000', 
                '999999999', 'padrao@email.com', 'Rua 1', '10', 'Centro', 'Cidade', 'ST', '00000-000')
            """)
        conn.commit()
    except: pass
    finally: conn.close()

# --- 1. FUNÇÕES DE USUÁRIO (O QUE ESTAVA FALTANDO) ---
def buscar_usuarios_db():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario")
    res = cursor.fetchall()
    conn.close()
    return res

def buscar_usuario_por_id(id_user):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE id_user = %s", (id_user,))
    res = cursor.fetchone()
    conn.close()
    return res

def cadastrar_usuario_db(id_user, nome, cpf, email, senha, perfil, salario):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO usuario (id_user, nome_user, cpf, email_user, senha_user, perfil, salario, status_user)
            VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
        """
        # O float(salario) é vital para não dar erro de Decimal
        cursor.execute(query, (id_user, nome, cpf, email, senha, perfil, float(salario)))
        conn.commit()
        return True, "Usuário cadastrado com sucesso!"
    except Exception as e:
        conn.rollback()
        print(f"Erro no Banco: {e}")
        return False, str(e)
    finally:
        conn.close()

def buscar_usuarios_db():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Busca todos os dados do usuário + contagem de vendas na tabela 'venda'
        query = """
            SELECT 
                u.*, 
                COUNT(v.id_venda) as total_vendas
            FROM usuario u
            LEFT JOIN venda v ON u.id_user = v.id_user
            GROUP BY u.id_user
        """
        cursor.execute(query)
        usuarios = []
        for row in cursor.fetchall():
            # Força o salário a ser float para não dar erro de serialização
            row['salario'] = float(row['salario']) if row['salario'] else 0.0
            usuarios.append(row)
        return usuarios
    except Exception as e:
        print(f"Erro ao buscar usuários: {e}")
        return []
    finally:
        conn.close()

def desativar_usuario_db(id_usuario):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE usuario SET status_user = 0 WHERE id_user = %s", (id_usuario,))
        conn.commit()
        return True
    except: return False
    finally: conn.close()

# --- 2. FUNÇÕES DE ESTOQUE ---
def buscar_produtos_estoque():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT e.*, c.nome_categoria, c.marca 
        FROM estoque e 
        LEFT JOIN categoria c ON e.id_categoria = c.id_categoria
    """
    cursor.execute(query)
    res = cursor.fetchall()
    conn.close()
    return res

def buscar_produto_por_id(id_prod):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estoque WHERE id_estoque = %s", (id_prod,))
    res = cursor.fetchone()
    conn.close()
    return res

def buscar_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome_categoria FROM categoria ORDER BY nome_categoria ASC")
    res = [r[0] for r in cursor.fetchall()]
    conn.close()
    return res

def cadastrar_produto_db(id_forn, id_cat, nome, cod, val, ent, custo, venda, emb, qtd, lote):
    garantir_dependencias()
    novo_id = gerar_id_char("estoque", "id_estoque", "E")
    f_id = id_forn if id_forn and len(str(id_forn)) > 2 else "F100001"
    c_id = id_cat if id_cat and len(str(id_cat)) > 2 else "C100001"
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO estoque VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, (novo_id, f_id, c_id, nome, cod, val, ent, custo, venda, emb, qtd, lote))
    conn.commit()
    conn.close()
    return True

def atualizar_produto_db(id_prod, nome, custo, venda, qtd):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE estoque SET nome_estoque=%s, preco_unitario=%s, preco_venda=%s, quantidade=%s 
        WHERE id_estoque=%s
    """, (nome, custo, venda, qtd, id_prod))
    conn.commit()
    conn.close()

# --- 3. FUNÇÕES DE VENDA ---
def registrar_venda_db(id_user, id_estoque, qtd, metodo, preco_venda=0):
    novo_id = gerar_id_char("venda", "id_venda", "V")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Debug: Isso vai aparecer no seu terminal do VS Code
        print(f"Tentando vender com Vendedor ID: '{id_user}' e Produto ID: '{id_estoque}'")
        
        query = """
            INSERT INTO venda (id_venda, id_user, id_estoque, metodo_pagamento, data_venda) 
            VALUES (%s, %s, %s, %s, CURDATE())
        """
        # Garantimos que os IDs sejam strings limpas
        cursor.execute(query, (novo_id, str(id_user).strip(), str(id_estoque).strip(), metodo))
        
        cursor.execute("UPDATE estoque SET quantidade = quantidade - %s WHERE id_estoque = %s", (qtd, id_estoque))
        
        conn.commit()
        return True, "Sucesso"
    except Exception as e:
        conn.rollback()
        print(f"Erro SQL Venda: {e}")
        return False, f"ID de Vendedor '{id_user}' não encontrado no sistema."
    finally:
        conn.close()

# 1. ATUALIZE A BUSCA (Para pegar a coluna 'quantidade' real)
def buscar_vendas_detalhadas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            v.id_venda, 
            v.data_venda, 
            v.metodo_pagamento, 
            v.quantidade as quantidade_vendida, -- Agora pega do banco
            e.nome_estoque as produto, 
            e.preco_venda, 
            u.nome_user as vendedor
        FROM venda v
        JOIN estoque e ON v.id_estoque = e.id_estoque
        JOIN usuario u ON v.id_user = u.id_user
        ORDER BY v.data_venda DESC
    """
    cursor.execute(query)
    res = cursor.fetchall()
    conn.close()
    return res

# 2. ATUALIZE O REGISTRO (Para salvar a quantidade enviada pela tela)
def registrar_venda_db(id_user, id_estoque, qtd, metodo, preco_venda=0):
    novo_id = gerar_id_char("venda", "id_venda", "V")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Adicionado 'quantidade' no INSERT
        query = """
            INSERT INTO venda (id_venda, id_user, id_estoque, metodo_pagamento, quantidade, data_venda) 
            VALUES (%s, %s, %s, %s, %s, CURDATE())
        """
        cursor.execute(query, (novo_id, str(id_user), str(id_estoque), metodo, qtd))
        
        # Diminui do estoque
        cursor.execute("UPDATE estoque SET quantidade = quantidade - %s WHERE id_estoque = %s", (qtd, id_estoque))
        
        conn.commit()
        return True, "Sucesso"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

# --- 4. HOME ---
def buscar_dados_home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 1. RECEITA TOTAL (Convertendo explicitamente para float)
        query_receita = """
            SELECT SUM(e.preco_venda * v.quantidade) as total 
            FROM venda v 
            JOIN estoque e ON v.id_estoque = e.id_estoque
        """
        cursor.execute(query_receita)
        res_receita = cursor.fetchone()
        receita = float(res_receita['total']) if res_receita and res_receita['total'] else 0.0

        # 2. RANKING (Convertendo valor_total para float)
        query_ranking = """
            SELECT e.nome_estoque as nome_user, 
                   SUM(v.quantidade) as qtd_vendas, 
                   CAST(SUM(e.preco_venda * v.quantidade) AS DOUBLE) as valor_total
            FROM venda v
            JOIN estoque e ON v.id_estoque = e.id_estoque
            GROUP BY e.nome_estoque
            ORDER BY valor_total DESC
            LIMIT 5
        """
        cursor.execute(query_ranking)
        ranking = []
        for row in cursor.fetchall():
            # Garantia dupla: Cast no SQL e float() no Python
            row['valor_total'] = float(row['valor_total']) if row['valor_total'] else 0.0
            row['qtd_vendas'] = int(row['qtd_vendas'])
            ranking.append(row)

        # 3. GRÁFICO
        query_grafico = """
            SELECT WEEKDAY(data_venda) as dia_num, SUM(quantidade) as qtd
            FROM venda
            WHERE data_venda >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY dia_num
            ORDER BY dia_num ASC
        """
        cursor.execute(query_grafico)
        vendas_semanais = []
        for row in cursor.fetchall():
            row['qtd'] = int(row['qtd'])
            vendas_semanais.append(row)

        return {
            "receita": receita, 
            "ranking": ranking, 
            "vendas_semanais": vendas_semanais
        }
    except Exception as e:
        print(f"Erro na Home: {e}")
        return {"receita": 0.0, "ranking": [], "vendas_semanais": []}
    finally:
        conn.close()


def buscar_usuario_por_id(id_user):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM usuario WHERE id_user = %s"
        cursor.execute(query, (id_user,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar usuário por ID: {e}")
        return None
    finally:
        conn.close()

def atualizar_usuario_db(id_user, nome, cpf, email, perfil, salario):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE usuario 
            SET nome_user = %s, cpf = %s, email_user = %s, perfil = %s, salario = %s 
            WHERE id_user = %s
        """
        # Forçamos o salario para float para evitar erro de Decimal/Serialização
        cursor.execute(query, (nome, cpf, email, perfil, float(salario), id_user))
        conn.commit()
        return True, "Usuário atualizado com sucesso!"
    except Exception as e:
        conn.rollback()
        print(f"Erro ao atualizar usuário: {e}")
        return False, str(e)
    finally:
        conn.close()

def cadastrar_fornecedor_db(nome, cnpj, tel, email, rua, num, bairro, cidade, uf, cep):
    # Gera o ID no padrão F100001
    novo_id = gerar_id_char("fornecedor", "id_fornecedor", "F")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO fornecedor 
            (id_fornecedor, nome_fornecedor, CNPJ, telefone, email_forn, 
             endereco_logradouro, endereco_numero, bairro, cidade, estado, cep)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (novo_id, nome, cnpj, tel, email, rua, num, bairro, cidade, uf, cep)
        cursor.execute(query, valores)
        conn.commit()
        return True, "Fornecedor cadastrado com sucesso!"
    except Exception as e:
        conn.rollback()
        print(f"Erro ao cadastrar fornecedor: {e}")
        return False, str(e)
    finally:
        conn.close()

def buscar_fornecedores():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM fornecedor ORDER BY nome_fornecedor ASC")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar fornecedores: {e}")
        return []
    finally:
        conn.close()
