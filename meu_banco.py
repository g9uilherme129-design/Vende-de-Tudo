import sqlite3

conexao = sqlite3.connect('meu_banco.db')
cursor = conexao.cursor()

def criar_tabelas():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_user TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_user TEXT,
            status TEXT NOT NULL,
            perfil TEXT NOT NUL,
            venda TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categoria(
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL
            
            
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produto(
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_fornecedor INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL,
            nome_produto TEXT NOT NULL,
            codigo_barra TEXT NOT NULL,
            FOREIGN KEY (id_fornecedor) REFERENCCES fornecedores (id_fornecedor),
            FOREIGN KEY (id_categoria) REFERENCCES categorias (id_categoria)                  
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fornecedor(
            id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_fornecedor TEXT NOT NULL,
            cnpj INTEGER NOT NULL,
            contato INTEGER NOT NULL,
            email TEXT NOT NULL, 
            rua TEXT NOT NULL,
            cep INTEGER NOT NULL
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas(
            id_itens INTEGER NOT NULL,
            id_user INTEGER NOT NULL,
            FOREIGN KEY (id_item ) REFERENCCES itens_venda (id_item),
            FOREIGN KEY (id_user) REFERENCCES categorias (id_user) 
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_vendidos(
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            id_produto INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            metodo_pagamento TEXT,
            data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_user) REFERENCES vendas (id_user),
            FOREIGN KEY (id_produto) REFERENCES produto (id_produto)
            
            
        )
    ''')

criar_tabelas()

conexao.commit()
conexao.close()