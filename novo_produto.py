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

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color="white",
            on_click=lambda _: on_stock()
        ),
        title=ft.Text("Novo Produto", size=20, weight="bold"),
        bgcolor="#0b1445",
        center_title=True,
    )

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

    def estilo_input(label, hint="", value="", read_only=False, col=None):
        input_field = ft.TextField(
            value=value,
            hint_text=hint,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color="white"),
            expand=True,
        )
        
        container = ft.Column(
            [
                ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=input_field,
                    bgcolor="#0A122A",
                    border=ft.border.all(1, "#1E2B4E"),
                    border_radius=10,
                    padding=ft.padding.only(right=10), # Ajuste para o texto não colar na borda
                )
            ],
            spacing=5,
            col=col # Define a largura responsiva (de 1 a 12)
        )
        return container, input_field

    # Criando os campos com definições de colunas (6 = metade da tela, 12 = tela cheia)
    nome_container, nome_input = estilo_input("NOME DO PRODUTO", col=12)
    fornecedor_container, fornecedor_input = estilo_input("FORNECEDOR", col=12)
    codigo_container, codigo_input = estilo_input("ID / CÓDIGO", value="SW-001", read_only=True, col=6)
    categoria_container, categoria_input = estilo_input("CATEGORIA", value="Moda", col=6)
    quantidade_container, quantidade_input = estilo_input("QUANTIDADE", value="1", col=12)
    venda_container, venda_input = estilo_input("VENDA(R$)", value="R$0,00", col=6)
    custo_container, custo_input = estilo_input("CUSTO(R$)", value="R$0,00", col=6)

    def salvar_clique(e):
        nome = nome_input.value
        codigo = codigo_input.value
        if nome == "":
            nome_input.error_text = "Por favor, digite o nome"
            page.update() 
            return
        
        sucesso = cadastrar_banco(nome, codigo, 1, 1)
        if sucesso:
            nome_input.value = ""
            page.snack_bar = ft.SnackBar(ft.Text("Produto salvo com sucesso!"), bgcolor="green")
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao salvar no banco."), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    # Organizando tudo em um ResponsiveRow para as caixas ficarem do mesmo tamanho
    layout_campos = ft.ResponsiveRow(
        controls=[
            nome_container,
            fornecedor_container,
            codigo_container,
            categoria_container,
            quantidade_container,
            venda_container,
            custo_container,
        ],
        spacing=15,
        run_spacing=15, # Espaço entre as "linhas" do grid
    )

    page.add(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Divider(height=10, color="transparent"),
                layout_campos,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Adicionar", 
                    on_click=salvar_clique, 
                    width=200,
                    height=45,
                    style=ft.ButtonStyle(
                        bgcolor="#1B4F9C",
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=10),
                    )
                ),
            ],
            spacing=10
        )
    )
    page.update()