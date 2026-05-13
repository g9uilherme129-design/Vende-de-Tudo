import mysql.connector
from datetime import datetime
import json

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
    try:
        # Adicionamos o JOIN com a tabela fornecedor (f) para pegar o nome real
        query = """
            SELECT 
                e.*, 
                c.nome_categoria, 
                f.nome_fornecedor  -- Traz o nome real do fornecedor mapeado
            FROM estoque e 
            LEFT JOIN categoria c ON e.id_categoria = c.id_categoria
            LEFT JOIN fornecedor f ON e.id_fornecedor = f.id_fornecedor
        """
        cursor.execute(query)
        res = cursor.fetchall()
        return res
    except Exception as e:
        print(f"Erro ao buscar produtos do estoque com fornecedor: {e}")
        return []
    finally:
        conn.close()

def buscar_produto_por_id(id_prod):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM estoque WHERE id_estoque = %s", (id_prod,))
        res = cursor.fetchone()
        return res
    except Exception as e:
        print(f"Erro ao buscar produto por ID: {e}")
        return None
    finally:
        conn.close()

def buscar_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome_categoria FROM categoria ORDER BY nome_categoria ASC")
    res = [r[0] for r in cursor.fetchall()]
    conn.close()
    return res

# Correção no database.py
def cadastrar_produto_db(id_forn, id_cat, nome, cod, val, ent, custo, venda, emb, qtd, lote):
    garantir_dependencias()
    novo_id = gerar_id_char("estoque", "id_estoque", "E")
    
    f_id = "F100001" if id_forn == "1" else id_forn
    c_id = "C100001" if id_cat == "1" else id_cat
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # AQUI: Verifique se as colunas no seu banco são exatamente estas 12:
        # id, fornecedor, categoria, nome, codigo, validade, entrada, custo, venda, embalagem, qtd, lote
        query = "INSERT INTO estoque VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        
        # Certifique-se que o 'val' (validade) não está sendo trocado pelo 'ent' (entrada)
        cursor.execute(query, (novo_id, f_id, c_id, nome, cod, val, ent, custo, venda, emb, qtd, lote))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro SQL ao cadastrar produto: {e}")
        raise e
    finally:
        conn.close()

def atualizar_produto_db(id_produto, id_fornecedor, id_categoria, nome, data_val, preco_uni, preco_ven, embalagem, qtd, lote):
    conn = get_connection() # Sua função de conexão
    cursor = conn.cursor()
    query = """
        UPDATE estoque 
        SET id_fornecedor = %s, 
            id_categoria = %s, 
            nome_estoque = %s, 
            data_validade = %s, 
            preco_unitario = %s, 
            preco_venda = %s, 
            embalagem = %s, 
            quantidade = %s, 
            lote = %s
        WHERE id_estoque = %s
    """
    valores = (id_fornecedor, id_categoria, nome, data_val, preco_uni, preco_ven, embalagem, qtd, lote, id_produto)
    cursor.execute(query, valores)
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

def buscar_venda_por_id(id_venda):
    conn = get_connection() # Use sua função de conexão aqui
    cursor = conn.cursor(dictionary=True)
    
    # O segredo está neste SQL com JOIN
    query = """
        SELECT 
            v.id_venda,
            v.quantidade,
            v.metodo_pagamento,
            u.nome_user AS vendedor,
            e.nome_estoque AS produto,
            e.preco_venda   -- O preço vem da tabela estoque
        FROM venda v
        JOIN usuario u ON v.id_user = u.id_user
        JOIN estoque e ON v.id_estoque = e.id_estoque
        WHERE v.id_venda = %s
    """
    
    cursor.execute(query, (id_venda,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

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

def buscar_vendas_detalhadas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                v.id_venda, 
                v.data_venda, 
                v.metodo_pagamento, 
                v.quantidade as qtd_venda, 
                e.nome_estoque as produto, 
                e.preco_venda, 
                u.nome_user as vendedor,
                c.nome_categoria as categoria
            FROM venda v
            JOIN estoque e ON v.id_estoque = e.id_estoque
            JOIN usuario u ON v.id_user = u.id_user
            JOIN categoria c ON e.id_categoria = c.id_categoria
            ORDER BY v.data_venda DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        conn.close()

def buscar_venda_por_id(id_venda):
    conn = get_connection() # Use sua função de conexão aqui
    cursor = conn.cursor(dictionary=True)
    
    # O segredo está neste SQL com JOIN
    query = """
        SELECT 
            v.id_venda,
            v.quantidade,
            v.metodo_pagamento,
            u.nome_user AS vendedor,
            e.nome_estoque AS produto,
            e.preco_venda   -- O preço vem da tabela estoque
        FROM venda v
        JOIN usuario u ON v.id_user = u.id_user
        JOIN estoque e ON v.id_estoque = e.id_estoque
        WHERE v.id_venda = %s
    """
    
    cursor.execute(query, (id_venda,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def atualizar_venda_db(id_venda, nova_qtd, novo_metodo):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Primeiro precisamos saber a quantidade antiga para ajustar o estoque
        cursor.execute("SELECT id_estoque, quantidade FROM venda WHERE id_venda = %s", (id_venda,))
        venda_antiga = cursor.fetchone()
        
        if venda_antiga:
            id_prod = venda_antiga[0]
            qtd_antiga = venda_antiga[1]
            
            # 2. Devolve a quantidade antiga ao estoque e subtrai a nova
            # (Estoque Atual + Qtd Antiga) - Nova Qtd
            cursor.execute(
                "UPDATE estoque SET quantidade = (quantidade + %s) - %s WHERE id_estoque = %s",
                (qtd_antiga, int(nova_qtd), id_prod)
            )

            # 3. Atualiza a venda (atualizamos as duas colunas de quantidade por segurança)
            query = """
                UPDATE venda 
                SET quantidade = %s, qtd_venda = %s, metodo_pagamento = %s 
                WHERE id_venda = %s
            """
            cursor.execute(query, (int(nova_qtd), int(nova_qtd), novo_metodo, id_venda))
            
            conn.commit()
            return True, "Venda atualizada com sucesso!"
        return False, "Venda não encontrada."
    except Exception as e:
        conn.rollback()
        print(f"Erro ao atualizar venda: {e}")
        return False, str(e)
    finally:
        conn.close()

def excluir_item_venda_db(id_venda):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Busca a quantidade e o produto para devolver ao estoque antes de deletar
        cursor.execute("SELECT id_estoque, quantidade FROM venda WHERE id_venda = %s", (id_venda,))
        venda = cursor.fetchone()
        
        if venda:
            id_prod = venda[0]
            qtd_venda = venda[1]
            
            # 2. Devolve os produtos ao estoque
            cursor.execute(
                "UPDATE estoque SET quantidade = quantidade + %s WHERE id_estoque = %s",
                (qtd_venda, id_prod)
            )
            
            # 3. Exclui a venda
            cursor.execute("DELETE FROM venda WHERE id_venda = %s", (id_venda,))
            
            conn.commit()
            return True, "Venda excluída e estoque atualizado!"
        
        return False, "Venda não encontrada."
        
    except Exception as e:
        conn.rollback()
        print(f"Erro ao excluir venda: {e}")
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

def buscar_dados_home_vendedor(id_user):
    # --- RASTREADOR DE BUG (Olhe o terminal do VS Code quando abrir a tela!) ---
    print("\n" + "="*50)
    print(f"[RASTREIO] O ID QUE CHEGOU NA HOME FOI: {id_user} (Tipo: {type(id_user)})")
    print("="*50 + "\n")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Se o ID veio nulo ou vazio, não adianta nem ir ao banco
        if not id_user:
            print("[AVISO] ID veio vazio, pulando busca e retornando zero.")
            return {"receita_vendedor": 0.0, "ranking": [], "produtos_scrum": [], "vendedores": [], "vendas_semanais": []}

        # Converte para string limpa, exatamente como está no banco
        id_user_str = str(id_user).strip()
        
        # 1. MINHAS VENDAS REALIZADAS
        query_receita = """
            SELECT SUM(e.preco_venda * v.quantidade) as total 
            FROM venda v 
            JOIN estoque e ON v.id_estoque = e.id_estoque
            WHERE v.id_user = %s
        """
        cursor.execute(query_receita, (id_user_str,))
        res_receita = cursor.fetchone()
        receita_vendedor = float(res_receita['total']) if res_receita and res_receita['total'] else 0.0

        # 2. RANKING DE PRODUTOS
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

        # 3. PRODUTOS SCRUM
        query_scrum = """
            SELECT nome_estoque as nome, preco_venda as preco, quantidade
            FROM estoque
            WHERE quantidade >= 0
            ORDER BY nome_estoque ASC
        """
        cursor.execute(query_scrum)
        produtos_scrum = []
        for row in cursor.fetchall():
            row['preco'] = float(row['preco']) if row['preco'] else 0.0
            row['quantidade'] = int(row['quantidade'])
            produtos_scrum.append(row)

        return {
            "receita_vendedor": receita_vendedor, 
            "ranking": ranking, 
            "produtos_scrum": produtos_scrum,
            "vendedores": [],
            "vendas_semanais": []
        }
    except Exception as e:
        print(f"[ERRO NO BANCO DA HOME]: {e}")
        return {"receita_vendedor": 0.0, "ranking": [], "produtos_scrum": [], "vendedores": [], "vendas_semanais": []}
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

def buscar_tema_usuario(id_usuario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT tema_dark FROM usuario WHERE id_user = %s", (id_usuario,))
        res = cursor.fetchone()
        # Se não achar ou der erro, o padrão será Dark (1)
        return res['tema_dark'] if res and res['tema_dark'] is not None else 1
    finally:
        conn.close()

def buscar_tema_db(id_usuario):
    conn = get_connection() # Ou o nome da sua função de conexão
    cursor = conn.cursor()
    try:
        # Busca o valor da coluna tema_dark para o usuário específico
        cursor.execute("SELECT tema_dark FROM usuario WHERE id_user = %s", (id_usuario,))
        resultado = cursor.fetchone()
        
        # Se retornar algo, pegamos o valor (0 ou 1). Se não, retornamos 1 (Dark) como padrão.
        if resultado:
            return resultado[0] # Se fetchall for usado, ajuste o índice
        return 1 
    except Exception as e:
        print(f"Erro ao buscar tema: {e}")
        return 1
    finally:
        conn.close()


def salvar_tema_db(id_usuario, is_dark):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # No SQL, True vira 1 e False vira 0
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

def alterar_status_categoria_db(id_cat, novo_status):
    """ 
    Altera o status da categoria. 
    Impedindo a desativação se houver produtos vinculados.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # REGRA DE NEGÓCIO: Se for desativar, verifica se há produtos
        if novo_status == "Inativo" or novo_status == 0:
            cursor.execute("SELECT COUNT(*) as total FROM estoque WHERE id_categoria = %s", (id_cat,))
            resultado = cursor.fetchone()
            
            if resultado['total'] > 0:
                return "Erro: Existem produtos cadastrados nesta categoria."

        # Se seu banco usa INT (1/0) ou VARCHAR ('Ativo'/'Inativo'), ajuste aqui:
        # Exemplo para VARCHAR:
        status_final = novo_status 
        
        query = "UPDATE categoria SET status_categoria = %s WHERE id_categoria = %s"
        cursor.execute(query, (status_final, id_cat))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao alterar status da categoria: {e}")
        return False
    finally:
        conn.close()


def buscar_categorias_ativas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Pega apenas as que não estão desativadas
        cursor.execute("SELECT * FROM categoria WHERE status_categoria = 'Ativo'")
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
    cursor = conn.cursor(dictionary=True)
    try:
        # REGRA: Se for desativar, verifica se há produtos no estoque
        if novo_status == "Inativo":
            cursor.execute("SELECT COUNT(*) as total FROM estoque WHERE id_fornecedor = %s", (id_forn,))
            vinc_estoque = cursor.fetchone()
            
            if vinc_estoque['total'] > 0:
                # Retorna uma mensagem de erro ou False para a UI avisar o usuário
                return "Erro: Fornecedor possui produtos vinculados no estoque."

        # Se passou na regra ou se for para Ativar, procede:
        # Se seu banco for INT use 1 e 0, se for VARCHAR use 'Ativo'/'Inativo'
        status_val = 0 if novo_status == "Inativo" else 1 
        
        cursor.execute(
            "UPDATE fornecedor SET status_fornecedor = %s WHERE id_fornecedor = %s", 
            (status_val, id_forn)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao alterar status: {e}")
        return False
    finally:
        conn.close()

def buscar_fornecedores_ativos():
    """Retorna apenas fornecedores que podem ser vinculados a novos produtos"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Filtra por status 1 (ou 'Ativo')
        cursor.execute("SELECT id_fornecedor, nome_fornecedor FROM fornecedor WHERE status_fornecedor = 1")
        return cursor.fetchall()
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

# --- perfil ---

def obter_resumo_vendas_vendedor(id_user):
    """ Retorna a quantidade de vendas e o valor total vendido pelo usuário logado """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Soma a quantidade e o valor total (preço_venda * quantidade)
        query = """
            SELECT 
                COUNT(v.id_venda) as total_vendas,
                SUM(e.preco_venda * v.quantidade) as valor_total
            FROM venda v
            JOIN estoque e ON v.id_estoque = e.id_estoque
            WHERE v.id_user = %s
        """
        cursor.execute(query, (id_user,))
        res = cursor.fetchone()
        
        return {
            "total_vendas": res['total_vendas'] if res['total_vendas'] else 0,
            "valor_total": float(res['valor_total']) if res['valor_total'] else 0.0
        }
    except Exception as e:
        print(f"Erro ao buscar resumo de vendas do perfil: {e}")
        return {"total_vendas": 0, "valor_total": 0.0}
    finally:
        conn.close()

def obter_ultimo_produto_vendedor(id_user):
    """ Busca o nome do último produto vendido pelo usuário """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT e.nome_estoque 
            FROM venda v
            JOIN estoque e ON v.id_estoque = e.id_estoque
            WHERE v.id_user = %s
            ORDER BY v.data_venda DESC
            LIMIT 1
        """
        cursor.execute(query, (id_user,))
        res = cursor.fetchone()
        return res['nome_estoque'] if res else "Nenhuma venda"
    except Exception as e:
        print(f"Erro ao buscar último produto: {e}")
        return "Erro ao carregar"
    finally:
        conn.close()

def buscar_dados_completos_perfil(id_user):
    """ Busca todos os campos do usuário para garantir que CPF, Salário e Email apareçam """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM usuario WHERE id_user = %s"
        cursor.execute(query, (id_user,))
        return cursor.fetchone()
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

def Validar_senha_atual_db(id_user, senha_ditada):
    """Verificar se a senha atual informa confere com a do banco."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT senha_user FROM usuario WHERE id_user = %s", (id_user,))
        res = cursor.fetchone()
        if res and res[0] == senha_ditada:
            return True
        return False
    except Exception as e:
        print(f"Erro ao validar senha: {e}")
        return False
    finally:
        conn.close()

