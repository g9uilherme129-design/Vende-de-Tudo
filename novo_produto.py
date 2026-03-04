import flet as ft
import sqlite3

def produto(page: ft.Page, on_stock):
    page.controls.clear()
    page.title = "Cadastro de Novo Produto"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.window_width = 400
    page.window_height = 800
    page.padding = 20

    # --- FUNÇÃO AUXILIAR DE BANCO DE DADOS ---
    def cadastrar_banco(nome, codigo, id_fornecedor, id_categoria):
        try:
            conn = sqlite3.connect('meu_banco.db')
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            cursor.execute('''
                INSERT INTO produto (nome_produto, codigo_barra, id_fornecedor, id_categoria)
                VALUES (?, ?, ?, ?)
            ''', (nome, codigo, id_fornecedor, id_categoria))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return False

    # --- UI HELPER ---
    def estilo_input(label, hint="", value="", width=None, read_only=False):
        input_field = ft.TextField(
            value=value,
            hint_text=hint,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color="white"),
        )

        container = ft.Column(
            [
                ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=input_field,
                    bgcolor="#0A122A",
                    border=ft.border.all(1, "#1E2B4E"),
                    border_radius=10,
                    width=width if width else 360,
                )
            ],
            spacing=5
        )
        return container, input_field

    # Criando campos
    nome_container, nome_input = estilo_input("NOME DO PRODUTO")
    fornecedor_container, fornecedor_input = estilo_input("FORNECEDOR")
    codigo_container, codigo_input = estilo_input("ID / CÓDIGO", value="SW-001", width=170, read_only=True)
    categoria_container, categoria_input = estilo_input("CATEGORIA", value="Moda", width=170)
    quantidade_container, quantidade_input = estilo_input("QUANTIDADE", value="1", width=170)
    venda_container, venda_input = estilo_input("VENDA(R$)", value="R$0,00", width=170)
    custo_container, custo_input = estilo_input("CUSTO(R$)", value="R$0,00", width=170)

    # --- FUNÇÃO DE CLIQUE (Apenas uma!) ---
    def salvar_clique(e):
        nome = nome_input.value
        codigo = codigo_input.value
        # Por enquanto usando IDs fixos, ate nozes criamos os Dropdowns
        fornecedor_id = 1
        categoria_id = 1

        if nome == "":
            nome_input.error_text = "Por favor, digite o nome"
            page.update() 
            return
        
        # Chama a função de banco definida lá em cima
        sucesso = cadastrar_banco(nome, codigo, fornecedor_id, categoria_id)

        if sucesso:
            # Limpa o campo e avisa o usuário
            nome_input.value = ""
            nome_input.error_text = None
            page.snack_bar = ft.SnackBar(ft.Text("Produto salvo com sucesso!"), bgcolor="green")
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao salvar no banco."), bgcolor="red")
            page.snack_bar.open = True
        
        page.update()

    # --- MONTAGEM DA PÁGINA ---
    page.add(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Novo Produto", size=28, weight=ft.FontWeight.BOLD, color="white"),
                ft.Divider(height=10, color="transparent"),

                nome_container,
                fornecedor_container,

                ft.Row(
                    controls=[
                        codigo_container,
                        categoria_container,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),

                quantidade_container,

                ft.Row(
                    controls=[
                        venda_container,
                        custo_container,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),

                ft.Divider(height=20, color="transparent"),

                ft.ElevatedButton(
                    "Adicionar",
                    on_click=salvar_clique, 
                    width=200,
                ),

                ft.TextButton("Voltar", on_click=lambda _: on_stock()),
            ],
            spacing=15
        )
    )
    page.update()