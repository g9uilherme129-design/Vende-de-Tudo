import flet as ft
import sqlite3

def produto(page: ft.Page, on_stock):
    page.controls.clear()
    
    # REMOVIDO: page.bgcolor e page.theme_mode fixos para seguir o sistema global
    page.padding = 20

    # Lógica de cores adaptáveis
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_input = "#0A122A" if is_dark else "#FFFFFF"
    cor_borda_input = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_input = "white" if is_dark else "black"
    cor_label = ft.Colors.TEAL_700 if is_dark else ft.Colors.TEAL_900

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color="white",
            on_click=lambda _: on_stock()
        ),
        title=ft.Text("Novo Produto", size=20, weight="bold", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    def cadastrar_banco(nome, codigo, id_fornecedor, id_categoria):
        try:
            # Nota: Certifique-se que o arquivo 'meu_banco.db' existe na raiz
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
            hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color=cor_texto_input),
            expand=True,
        )
        
        container = ft.Column(
            [
                ft.Text(label, size=11, color=cor_label, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=input_field,
                    bgcolor=cor_fundo_input,
                    border=ft.border.all(1, cor_borda_input),
                    border_radius=10,
                    padding=ft.padding.only(right=10),
                )
            ],
            spacing=5,
            col=col 
        )
        return container, input_field

    # Campos Responsivos
    nome_container, nome_input = estilo_input("NOME DO PRODUTO", col={"sm": 12, "md": 12})
    fornecedor_container, fornecedor_input = estilo_input("FORNECEDOR", col=12)
    codigo_container, codigo_input = estilo_input("ID / CÓDIGO", value="SW-001", read_only=True, col=6)
    categoria_container, categoria_input = estilo_input("CATEGORIA", value="Moda", col=6)
    quantidade_container, quantidade_input = estilo_input("QUANTIDADE", value="1", col=12)
    venda_container, venda_input = estilo_input("VENDA(R$)", value="0,00", col=6)
    custo_container, custo_input = estilo_input("CUSTO(R$)", value="0,00", col=6)

    def salvar_clique(e):
        if not nome_input.value:
            nome_input.error_text = "Campo obrigatório"
            page.update() 
            return
        
        sucesso = cadastrar_banco(nome_input.value, codigo_input.value, 1, 1)
        if sucesso:
            nome_input.value = ""
            page.snack_bar = ft.SnackBar(ft.Text("Produto salvo com sucesso!"), bgcolor="green")
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao salvar no banco."), bgcolor="red")
            page.snack_bar.open = True
        page.update()

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
        run_spacing=15,
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
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor="#1B4F9C",
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=12),
                    )
                ),
            ],
            spacing=10
        )
    )
    page.update()