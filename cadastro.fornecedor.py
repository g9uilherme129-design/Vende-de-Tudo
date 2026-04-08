import flet as ft
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="seu_banco"
    )

def buscar_fornecedores():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM fornecedor")
    dados = cursor.fetchall()
    conn.close()
    return dados

def inserir_fornecedor(f):
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    INSERT INTO fornecedor(
    nome_fornecedor, cnpj, telefone, email_forn,
    endereco_logradouro, endereco_numero,
    bairro, cidade, estado, cep
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        f["nome"],
        f["cnpj"],
        f["telefone"],
        f["email"],
        f["logradouro"],
        f["numero"],
        f["bairro"],
        f["cidade"],
        f["estado"],
        f["cep"],
    ))
    conn.commit()
    conn.close()

def tela_cadastro(page, voltar):
    page.controls.clear()

    nome = ft.TextField(label="Nome")
    cnpj = ft.TextField(label="CNPJ")
    telefone = ft.TextField(label="Telefone")
    email = ft.TextField(label="Email")
    logradouro = ft.TextField(label="Rua")
    numero = ft.TextField(label="Número")
    bairro = ft.TextField(label="Bairro")
    cidade = ft.TextField(label="Cidade")
    estado = ft.TextField(label="Estado")
    cep = ft.TextField(label="CEP")

    msg = ft.Text(color="red")

    def salvar(e):
        if not nome.value or not cnpj.value:
            msg.value = "Nome e CNPJ são obrigatórios!"
            page.update()
            return
        inserir_fornecedor({
            "nome":nome.value,
            "cnpj":cnpj.value,
            "telefone":telefone.value,
            "email":email.value,
            "logradouro":logradouro.value,
            "numero":numero.value,
            "bairro":bairro.value,
            "cidade":cidade.value,
            "estado":estado.value,
            "cep":cep.value
        })
        voltar()

    page.add(
    ft.Column([
        ft.Text("Cadastro do Fornecedor", size=22, weight="bold"),
        nome, cnpj, telefone, email,  
        ft.Divider(),
        logradouro, numero, bairro,
        cidade, estado, cep,
        msg,
        ft.Row([
            ft.ElevatedButton("Salvar", on_click=salvar), 
            ft.TextButton("Cancelar", on_click=lambda _: voltar())
        ])
    ])
)
    page.update()

    def tela_fornecedores(page):
        page.controls.clear()
        lista = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

        def abrir_cadastro(e=None):
            tela_cadastro(page, tela_fornecedores)

        def card(f):
            return ft.Container(
                bgcolor="#f5f5f5",
                padding=15,
                border_radius=10,
                content=ft.Column([
                    ft.Text(f["nome_fornecedor"], size=18, weight="bold"),
                    ft.Text(f"CNPJ: {f['cnpj']}"),
                    ft.Text(f"Telefone: {f['telefone']}"),
                    ft.Text(f"Email: {f['email_forn']}"),
                    ft.Text(
                        f"{f['endereco_logradouro']}, {f['endereco_numero']} - "
                        f"{f['bairro']} - {f['cidade']}/{f['estado']}"
                    ),
                    ft.Text(f"CEP: {f['cep']}")
                ])
            )
        def carregar():
            lista.controls.clear()
            dados = buscar_fornecedores()

            for f in dados:
                lista.controls.append(card(f))

            page.update()

        busca = ft.TextField(
            hint_text= "Buscar Fornecedor...",
            on_change=lambda e: filtrar()
        )

        def filtrar():
            texto = busca.value.lower()
            dados = buscar_fornecedores()

            filtrados = [
                f for f in dados
                if texto in f["nome_fornecedor"].lower()
            ]
            lista.controls.clear()
            for f in filtrados:
                lista.controls.append(card(f))
            
            page.update()

            page.add(
                ft.Column([
                    ft.Row([
                        ft.Text("Fornecedores", size=20, weight="bold"),
                        ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=abrir_cadastro)
                    ], alignment="spaceBetween"),
                    busca,
                    lista
                ])
            )
            carregar()

def tela_fornecedores(page):
    page.add(ft.Text("Teste funcionando"))

def main(page: ft.Page):
    page.title = "Fornecedores"
    tela_fornecedores(page)

ft.app(target=main)

ft.app(target=main)