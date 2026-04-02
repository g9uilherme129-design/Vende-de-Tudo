import flet as ft
from database import Database

db = Database()

def produto(page: ft.Page, on_stock):
    page.controls.clear()
    page.title = "Cadastro de Novo Produto"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.window_width = 400
    page.window_height = 800
    page.padding = 20


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
        fornecedor_id = 1
        categoria_id =1
        codigo = codigo_input.value
        validade = "2026-12-31"
        custo = custo_input.value.replace("R$", "").replace(",", ".")
        venda = venda_input.value.replace("R$", "").replace(",", ".")
        embalagem = "unidade"
        try:  
            qtd = int(quantidade_input.value)
        except:
            qdt = 0
            
        lote = "L-001"

        if not nome:
            nome_input.error_text = "Digite o nome do produto"
            page.update()
            return

        sucesso = db.inserir_estoque(
            fornecedor_id,
            categoria_id,
            codigo,
            validade,
            custo,
            venda,
            embalagem,
            qtd,
            lote,
        )

        if sucesso:
            nome_input.value = ""
            page.snack_bar = ft.SnackBar(ft.Text("produto salvo com susseso"), bgcolor="green")
            page.snack_bar.open = True

        else:
            page.snack_bar = ft.SnackBar(ft.Text("erro ao conectar ao Banco"), bgcolor="red")
            page.snack_bar.open = True
       
        page.update()

    page.add(
        ft.Colunm(
            scroll=ft.ScrollMode.AUTO,
            horizontal_aligment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("novo produto", size=28, weight=ft.FontWeight.BOLD, color="white"),
                nome_container,
                fornecedor_container,
                ft.Row([codigo_container, categoria_container], alignment=ft.MainAxisAlignment.CENTER),
                ft.ElevatedButton("Adicionar", on_click=salvar_clique, width=200),
                ft.TextButton("voltar", on_click=lambda _: on_stock()),
            ],
            spacing=15
        )
    )
    page.update()






















# import flet as ft

# def produto(page: ft.Page, on_stock):
#     page.controls.clear()
#     page.title = "Cadastro de Novo Produto"
#     page.theme_mode = ft.ThemeMode.DARK
#     page.bgcolor = "#050505"
#     page.window_width = 400
#     page.window_height = 800
#     page.padding = 20

#     def estilo_input(label, hint="", value="", width=None, read_only=False):
#         input_field = ft.TextField(
#             value=value,
#             hint_text=hint,
#             hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
#             border=ft.InputBorder.NONE,
#             content_padding=15,
#             read_only=read_only,
#             text_style=ft.TextStyle(color="white"),
#         )

#         return ft.Column(
#             [
#                 ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD),
#                 ft.Container(
#                     content=input_field,
#                     bgcolor="#0A122A",
#                     border=ft.border.all(1, "#1E2B4E"),
#                     border_radius=10,
#                     width=width if width else 360,
#                 )
#             ],
#             spacing=5
#         ), input_field

#     # Criando campos
#     nome_container, nome_input = estilo_input("NOME DO PRODUTO")
#     fornecedor_container, fornecedor_input = estilo_input("FORNECEDOR")
#     codigo_container, codigo_input = estilo_input("ID / CÓDIGO", value="SW-001", width=170, read_only=True)
#     categoria_container, categoria_input = estilo_input("CATEGORIA", value="Moda", width=170)

#     def salvar(e):
#         print("Salvando:")
#         print("Nome:", nome_input.value)
#         print("Fornecedor:", fornecedor_input.value)
#         print("Categoria:", categoria_input.value)

#     page.add(
#         ft.Column(
#             scroll=ft.ScrollMode.AUTO,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             controls=[
#                 ft.Text("Novo Produto", size=28, weight=ft.FontWeight.BOLD, color="white"),
#                 ft.Divider(height=10, color="transparent"),

#                 nome_container,
#                 fornecedor_container,

#                 ft.Row(
#                     controls=[
#                         codigo_container,
#                         categoria_container,
#                     ],
#                     alignment=ft.MainAxisAlignment.CENTER,
#                     spacing=20
#                 ),

#                 ft.Divider(height=20, color="transparent"),

#                 ft.ElevatedButton(
#                     "Adicionar",
#                     on_click=salvar,
#                     width=200,
#                 ),

#                 ft.TextButton("Voltar", on_click=lambda _: on_stock()),
#             ],
#             spacing=15
#         )
#     )

#     page.update()