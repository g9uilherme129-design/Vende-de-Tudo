import flet as ft
from database import buscar_produto_por_id, atualizar_produto_db

def editar_produto(page: ft.Page, on_back, id_produto):
    page.controls.clear()
    page.padding = 0

    # Busca dados no banco
    p = buscar_produto_por_id(id_produto)

    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_input_fundo = "#0A122A" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_label = ft.Colors.TEAL_400 if is_dark else ft.Colors.TEAL_900

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_back()),
        title=ft.Text("Vende de Tudo", color="white", weight="bold"),
        bgcolor="#0b1445",
        center_title=True,
    )

    def estilo_input(label, value="", col=None, limite=None):
        input_field = ft.TextField(
            value=str(value) if value else "",
            border=ft.InputBorder.NONE,
            content_padding=15,
            text_style=ft.TextStyle(color=cor_texto),
            expand=True,
            max_length=limite,
        )
        container = ft.Column([
            ft.Text(f"  {label}", size=11, color=cor_label, weight="bold"),
            ft.Container(
                content=input_field, 
                bgcolor=cor_input_fundo,
                border=ft.border.all(1, cor_borda), 
                border_radius=12,
                padding=ft.padding.only(right=10),
            )
        ], spacing=5, col=col)
        return container, input_field

    nome_c, nome_in = estilo_input("NOME DO PRODUTO", value=p['nome_produto'], col=12, limite=100)
    preco_c, preco_in = estilo_input("PREÇO (R$)", value=p['preco'], col=6)
    estoque_c, estoque_in = estilo_input("ESTOQUE ATUAL", value=p['estoque'], col=6)
    desc_c, desc_in = estilo_input("DESCRIÇÃO", value=p['descricao'], col=12, limite=255)

    def salvar(e):
        try:
            atualizar_produto_db(id_produto, nome_in.value, preco_in.value, estoque_in.value, desc_in.value)
            page.snack_bar = ft.SnackBar(ft.Text("Produto atualizado!"), bgcolor="green")
            page.snack_bar.open = True
            on_back()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    form_content = ft.Column(
        expand=True,
        controls=[
            ft.Container(
                padding=ft.padding.only(top=20, bottom=10),
                content=ft.Text(f"Editar Produto #{id_produto}", size=24, weight="bold", color=cor_texto)
            ),
            ft.Container(
                content=ft.Column([
                    ft.ResponsiveRow([nome_c, preco_c, estoque_c, desc_c], spacing=15),
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Salvar Alterações", 
                        on_click=salvar, 
                        width=500, height=50,
                        style=ft.ButtonStyle(bgcolor="#1B4F9C", color="white", shape=ft.RoundedRectangleBorder(radius=12))
                    ),
                ], scroll=ft.ScrollMode.AUTO),
                expand=True
            )
        ]
    )

    page.add(
        ft.Column(
            expand=True,
            horizontal_alignment="center",
            controls=[ft.Container(content=form_content, width=500, padding=20, expand=True)]
        )
    )
    page.update()