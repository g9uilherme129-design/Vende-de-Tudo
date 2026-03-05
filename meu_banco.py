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
            perfil TEXT NOT NUL
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
            id_fornecedor INTEGER,
            id_categoria INTEGER,
            FOREIGN KEY (id_fornecedor) REFERENCCES fornecedores (id),
            FOREIGN KEY (id_categoria) REFERENCCES categorias (id)                       
        )
    ''')


def venda():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas(
            id_vendas INTEGER PRIMARY KEY AUTOINCREMENT,
            data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL,
            metodo_pagamento TEXT
            
            
        )
    ''')

def itens_venda():
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas(
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venda INTEGER NOT NULL,
            id_produto INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY (id_venda) REFERENCES vendas (id_venda),
            FOREIGN KEY (id_produto) REFERENCES produto (id_venda)
            
            
        )
    ''')

criar_tabelas()

conexao.commit()
conexao.close()