import mysql.connector

def conectar():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="vende_de_tudo"
    )
    return conn