import mysql.connector
from datetime import datetime

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
    try:
        # Mudamos u.id_user para u.id_user
        query = """
            SELECT 
                u.*, 
                COUNT(v.id_venda) as total_vendas
            FROM usuario u
            LEFT JOIN venda v ON u.id_user = v.id_user
            WHERE u.status_user = 1
            GROUP BY u.id_user
        """
        cursor.execute(query)
        usuarios = []
        for row in cursor.fetchall():
            row['salario'] = float(row['salario']) if row['salario'] else 0.0
            usuarios.append(row)
        return usuarios
    except Exception as e:
        print(f"Erro ao buscar usuários: {e}")
        return []
    finally:
        conn.close()

def atualizar_usuario_db(id_user, nome, cpf, email, perfil, salario, senha=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Onde estava id_user no WHERE, agora é id_user
        if senha and senha.strip() != "":
            sql = "UPDATE usuario SET nome_user=%s, cpf=%s, email_user=%s, perfil=%s, salario=%s, senha_user=%s WHERE id_user=%s"
            valores = (nome, cpf, email, perfil, float(salario), senha, id_user)
        else:
            sql = "UPDATE usuario SET nome_user=%s, cpf=%s, email_user=%s, perfil=%s, salario=%s WHERE id_user=%s"
            valores = (nome, cpf, email, perfil, float(salario), id_user)
        
        cursor.execute(sql, valores)
        conn.commit()
        return True, "Sucesso"
    except Exception as e:
        print(f"Erro no Banco: {e}")
        return False, str(e)
    finally:
        conn.close()

def desativar_usuario_db(id_usuario, motivo=None): # Adicionei o motivo como opcional
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # O SQL continua desativando pelo status
        cursor.execute("UPDATE usuario SET status_user = 0 WHERE id_user = %s", (id_usuario,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao desativar: {e}")
        return False
    finally:
        conn.close()

def cadastrar_usuario_db(id_user, nome, cpf, email, senha, perfil, salario):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO usuario (id_user, nome_user, cpf, email_user, senha_user, perfil, salario, status_user)
            VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
        """
        cursor.execute(query, (id_user, nome, cpf, email, senha, perfil, float(salario)))
        conn.commit()
        return True, "Sucesso"
    except Exception as e:
        print(f"Erro ao cadastrar: {e}")
        return False, str(e)
    finally: conn.close()

def buscar_usuarios_db():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Remova qualquer "WHERE status_user = 1" para que os inativos venham também
        query = """
            SELECT u.*, COUNT(v.id_venda) as total_vendas
            FROM usuario u
            LEFT JOIN venda v ON u.id_user = v.id_user
            GROUP BY u.id_user
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        conn.close()

def buscar_usuario_por_id(id_user):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Busca usando o nome real da coluna 'id_user'
        cursor.execute("SELECT *, id_user as id_user FROM usuario WHERE id_user = %s", (id_user,))
        return cursor.fetchone()
    finally:
        conn.close()

def atualizar_usuario_db(id_user, nome, cpf, email, perfil, salario, senha=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # MUDANÇA AQUI: de id_user para id_user no WHERE
        if senha and senha.strip() != "":
            sql = """
                UPDATE usuario 
                SET nome_user=%s, cpf=%s, email_user=%s, perfil=%s, salario=%s, senha_user=%s 
                WHERE id_user=%s
            """
            valores = (nome, cpf, email, perfil, float(salario), senha, id_user)
        else:
            sql = """
                UPDATE usuario 
                SET nome_user=%s, cpf=%s, email_user=%s, perfil=%s, salario=%s 
                WHERE id_user=%s
            """
            valores = (nome, cpf, email, perfil, float(salario), id_user)
            
        cursor.execute(sql, valores)
        conn.commit()
        return True, "Sucesso"
    except Exception as e:
        print(f"Erro no Banco: {e}") 
        return False, str(e)
    finally:
        conn.close()

def desativar_usuario_db(id_usuario, motivo, admin_nome):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """
            UPDATE usuario 
            SET status_user = 0, 
                motivo_desat = %s, 
                data_desat = %s, 
                admin_desat = %s 
            WHERE id_user = %s
        """
        cursor.execute(sql, (motivo, agora, admin_nome, id_usuario))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao desativar: {e}")
        return False
    finally:
        conn.close()


def buscar_usuario_por_nome(nome_user):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Busca o admin pelo nome exato que foi salvo na desativação
        query = "SELECT * FROM usuario WHERE nome_user = %s"
        cursor.execute(query, (nome_user,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar admin por nome: {e}")
        return None
    finally:
        conn.close()

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
    
    # Se o usuário digitou apenas "1", transformamos no ID correto do banco
    f_id = "F100001" if id_forn == "1" else id_forn
    c_id = "C100001" if id_cat == "1" else id_cat
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO estoque VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (novo_id, f_id, c_id, nome, cod, val, ent, custo, venda, emb, qtd, lote))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro SQL ao cadastrar produto: {e}")
        raise e # Repassa o erro para o Flet exibir no SnackBar
    finally:
        conn.close()

def atualizar_produto_db(id_prod, nome, custo, venda, qtd):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE estoque SET nome_estoque=%s, preco_unitario=%s, preco_venda=%s, quantidade=%s 
        WHERE id_estoque=%s
    """, (nome, custo, venda, qtd, id_prod))
    conn.commit()
    conn.close()


def buscar_vendas_detalhadas():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Busca vendas cruzando com estoque e usuario para mostrar nomes em vez de IDs
        query = """
            SELECT 
                v.id_venda, 
                e.nome_estoque as produto, 
                e.preco_venda, 
                u.nome_user as vendedor, 
                v.data_venda, 
                v.quantidade as qtd_venda, 
                v.metodo_pagamento
            FROM venda v
            JOIN estoque e ON v.id_estoque = e.id_estoque
            JOIN usuario u ON v.id_user = u.id_user
            ORDER BY v.data_venda DESC
        """
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Erro ao buscar vendas detalhadas: {e}")
        return []
    finally:
        conn.close()


def registrar_venda_db(id_user, id_estoque, qtd, metodo, preco_venda=0):
    novo_id = gerar_id_char("venda", "id_venda", "V")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Usamos NOW() para pegar data + hora exata
        # 2. Preenchemos todas as colunas de quantidade possíveis com o valor real (qtd)
        query = """
            INSERT INTO venda (id_venda, id_user, id_estoque, metodo_pagamento, quantidade, qtd_venda, data_venda) 
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        # Aqui passamos a variável 'qtd' (os seus 5 itens) para ambas as colunas
        cursor.execute(query, (novo_id, str(id_user), str(id_estoque), metodo, qtd, qtd))
        
        # Baixa o estoque normalmente
        cursor.execute("UPDATE estoque SET quantidade = quantidade - %s WHERE id_estoque = %s", (qtd, id_estoque))
        
        conn.commit()
        return True, "Sucesso"
    except Exception as e:
        conn.rollback()
        print(f"Erro no Banco: {e}")
        return False, str(e)
    finally:
        conn.close()


# --- AJUSTE NA BUSCA (Garantir que o nome da coluna bata com o card) ---
def buscar_vendas_detalhadas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            v.id_venda, 
            v.data_venda, 
            v.metodo_pagamento, 
            v.quantidade as qtd_venda, 
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
                   SUM(v.quantidade) as qtd_venda, 
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
            row['valor_total'] = float(row['valor_total']) if row['valor_total'] else 0.0
            row['qtd_venda'] = int(row['qtd_venda'])
            ranking.append(row)

        # --- RANKING DE VENDEDORES (ADICIONADO AQUI) ---
        query_vendedores = """
            SELECT u.nome_user as nome, 
                   COUNT(v.id_venda) as total_vendas
            FROM venda v
            JOIN usuario u ON v.id_user = u.id_user
            GROUP BY u.id_user
            ORDER BY total_vendas DESC
            LIMIT 5
        """
        cursor.execute(query_vendedores)
        vendedores = []
        for row in cursor.fetchall():
            row['total_vendas'] = int(row['total_vendas'])
            vendedores.append(row)
        # -----------------------------------------------

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
            "vendedores": vendedores, # Incluído no retorno
            "vendas_semanais": vendas_semanais
        }
    except Exception as e:
        print(f"Erro na Home: {e}")
        return {"receita": 0.0, "ranking": [], "vendedores": [], "vendas_semanais": []}
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

def atualizar_usuario_db(id_user, nome, cpf, email, perfil, salario, senha=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Note que usei 'id_user' no WHERE porque é como está no seu VS Code
        if senha and senha.strip() != "":
            sql = """
                UPDATE usuario 
                SET nome_user=%s, cpf=%s, email_user=%s, perfil=%s, salario=%s, senha_user=%s 
                WHERE id_user=%s
            """
            valores = (nome, cpf, email, perfil, salario, senha, id_user)
        else:
            sql = """
                UPDATE usuario 
                SET nome_user=%s, cpf=%s, email_user=%s, perfil=%s, salario=%s 
                WHERE id_user=%s
            """
            valores = (nome, cpf, email, perfil, salario, id_user)
            
        cursor.execute(sql, valores)
        conn.commit()
        return True, "Sucesso"
    except Exception as e:
        print(f"Erro no Banco: {e}") # Isso vai aparecer no seu terminal
        return False, str(e)
    finally:
        conn.close()

def cadastrar_fornecedor_db(nome, cnpj, tel, email, logradouro, num, bairro, cidade, uf, cep):
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
        valores = (novo_id, nome, cnpj, tel, email, logradouro, num, bairro, cidade, uf, cep)
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

def validar_login(usuario_ou_email, senha):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT * FROM usuario 
            WHERE (nome_user = %s OR email_user = %s) 
            AND senha_user = %s 
            AND status_user = 1
        """
        cursor.execute(query, (usuario_ou_email, usuario_ou_email, senha))
        user = cursor.fetchone()
        
        if user:
            return True, user
        else:
            return False, "Usuário/E-mail ou senha incorretos."
    except Exception as e:
        return False, f"Erro no banco: {str(e)}"
    finally:
        conn.close()
def buscar_tema_db(id_usuario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT tema_dark FROM tema_usuario WHERE id_user = %s", (id_usuario,))
        res = cursor.fetchone()
        # Se não existir registro ainda, retorna 1 (Dark) por padrão
        return res['tema_dark'] if res else 1
    finally:
        conn.close()


def salvar_tema_db(id_usuario, is_dark):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Se is_dark for True, vira 1. Se for False, vira 0.
        valor_tema = 1 if is_dark else 0
        
        sql = "UPDATE usuario SET tema_dark = %s WHERE id_user = %s"
        cursor.execute(sql, (valor_tema, id_usuario))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao salvar tema: {e}")
        return False
    finally:
        conn.close()


def reativar_usuario_db(id_user):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Volta o status para 1 e limpa os campos de desativação
        sql = """
            UPDATE usuario 
            SET status_user = 1, 
                motivo_desat = NULL, 
                data_desat = NULL, 
                admin_desat = NULL 
            WHERE id_user = %s
        """
        cursor.execute(sql, (id_user,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao reativar: {e}")
        return False
    finally:
        conn.close()

def buscar_fornecedores_dropdown():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Pega o ID para o banco e o Nome para o usuário ver
        cursor.execute("SELECT id_fornecedor, nome_fornecedor FROM fornecedor ORDER BY nome_fornecedor ASC")
        return cursor.fetchall()
    finally:
        conn.close()

def buscar_categorias_dropdown():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Pega o ID para o banco e o Nome para o usuário ver
        cursor.execute("SELECT id_categoria, nome_categoria FROM categoria ORDER BY nome_categoria ASC")
        return cursor.fetchall()
    finally:
        conn.close()

def buscar_categorias_detalhado():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_categoria, nome_categoria FROM categoria ORDER BY nome_categoria ASC")
        dados = cursor.fetchall()
        
        for d in dados:
            d['status'] = "Ativo" 
            
        return dados
    finally:
        conn.close()

def salvar_categoria_db(nome):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
        "INSERT INTO categoria (id_categoria, nome_categoria, tipo_categoria, marca, status_categoria) VALUES (%s,%s,%s,%s,%s)",
        (gerar_id_char("categoria","id_categoria","C"), nome, "Diversos", "Generica", 1)
)
        conn.commit()
    finally:
        conn.close()

def editar_categoria_db(id_cat, novo_nome):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE categoria SET nome_categoria = %s WHERE id_categoria = %s", (novo_nome, id_cat))
        conn.commit()
    finally:
        conn.close()

def alterar_status_fornecedor_db(id_forn, novo_status):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE fornecedor SET status = %s WHERE id_fornecedor = %s", 
            (novo_status, id_forn)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"ERRO NO BANCO: {e}") # Isso vai te mostrar se a coluna status falta
        return False
    finally:
        conn.close()

def alterar_status_categoria_db(id_cat, novo_status):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Atualiza o status da categoria
        cursor.execute(
            "UPDATE categoria SET status = %s WHERE id_categoria = %s", 
            (novo_status, id_cat)
        )
        conn.commit()
    except Exception as e:
        print(f"Erro ao alterar status da categoria: {e}")
    finally:
        conn.close()


def buscar_fornecedor_por_id(id_forn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM fornecedor WHERE id_fornecedor = %s", (id_forn,))
        return cursor.fetchone()
    finally:
        conn.close()

def atualizar_fornecedor_db(id_forn, nome, cnpj, tel, email, logradouro, num, bairro, cidade, uf, cep):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Note o email_forn aqui
        sql = """UPDATE fornecedor SET 
                 nome_fornecedor=%s, CNPJ=%s, telefone=%s, email_forn=%s, 
                 endereco_logradouro=%s, endereco_numero=%s, bairro=%s, cidade=%s, estado=%s, cep=%s
                 WHERE id_fornecedor=%s"""
        cursor.execute(sql, (nome, cnpj, tel, email, logradouro, num, bairro, cidade, uf, cep, id_forn))
        conn.commit()
    finally:
        conn.close()

def validar_recuperacao_db(nome, email, cpf):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Verifica se existe um usuário com esses 3 dados exatos
        query = "SELECT id_user FROM usuario WHERE nome_user = %s AND email_user = %s AND cpf = %s AND status_user = 1"
        cursor.execute(query, (nome, email, cpf))
        return cursor.fetchone() # Retorna o ID se achar, ou None se estiver errado
    finally:
        conn.close()

def resetar_senha_db(id_user, nova_senha):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE usuario SET senha_user = %s WHERE id_user = %s", (nova_senha, id_user))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

