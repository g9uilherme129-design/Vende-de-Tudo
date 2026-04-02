import flet as ft
from database import buscar_produto_por_id, atualizar_produto_db

def editar_produto(page: ft.Page, on_stock, id_produto):
    page.controls.clear()
    
    # Busca os dados atuais no banco para preencher os campos
    dados_atuais = buscar_produto_por_id(id_produto)
    
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_input_fundo = "#0A122A" if is_dark else "#F0F2F5"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_stock()),
        title=ft.Text(f"Editar Produto #{id_produto}", size=20, weight="bold", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    def estilo_input(label, value="", read_only=False, col=None):
        input_field = ft.TextField(
            value=str(value),
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color=cor_texto),
            expand=True,
        )
        container = ft.Column([
            ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight="bold"),
            ft.Container(
                content=input_field, bgcolor=cor_input_fundo,
                border=ft.border.all(1, cor_borda), border_radius=10,
                padding=ft.padding.only(right=10),
            )
        ], spacing=5, col=col)
        return container, input_field

    # Preenchendo com dados vindos do MySQL
    nome_c, nome_in = estilo_input("NOME DO PRODUTO", value=dados_atuais['nome_estoque'], col=12)
    cod_c, cod_in = estilo_input("CÓDIGO DE BARRAS", value=dados_atuais['codigo_barras'], read_only=True, col=12)
    qtd_c, qtd_in = estilo_input("ESTOQUE ATUAL", value=dados_atuais['quantidade'], col=6)
    venda_c, venda_in = estilo_input("PREÇO VENDA (R$)", value=dados_atuais['preco_venda'], col=6)
    custo_c, custo_in = estilo_input("PREÇO CUSTO (R$)", value=dados_atuais['preco_unitario'], col=12)

    def salvar_alteracoes(e):
        try:
            atualizar_produto_db(
                id_prod=id_produto,
                nome=nome_in.value,
                custo=float(custo_in.value),
                venda=float(venda_in.value),
                qtd=int(qtd_in.value)
            )
            page.snack_bar = ft.SnackBar(ft.Text("Produto atualizado com sucesso!"), bgcolor="green")
            page.snack_bar.open = True
            on_stock() # Volta para a lista
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao atualizar: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    layout_campos = ft.ResponsiveRow(
        controls=[nome_c, cod_c, qtd_c, venda_c, custo_c],
        spacing=15, run_spacing=15,
    )

    page.add(
        ft.Column(
            horizontal_alignment="center",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Divider(height=10, color="transparent"),
                layout_campos,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Salvar Alterações", 
                    on_click=salvar_alteracoes, 
                    width=250, height=50,
                    style=ft.ButtonStyle(bgcolor="#1B4F9C", color="white", shape=ft.RoundedRectangleBorder(radius=10))
                ),
            ],
            spacing=10
        )
    )
    page.update()