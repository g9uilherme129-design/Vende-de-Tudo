from db import conectar
import hashlib


def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def verificar_login(email, senha_digitada):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()

    conn.close()

    if usuario:
        senha_hash = hash_senha(senha_digitada)

        if usuario["senha"] == senha_hash and usuario["ativo"]:
            return usuario  # retorna dados do usuário

    return None