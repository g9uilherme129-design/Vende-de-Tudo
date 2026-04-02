import flet as ft
from database import cadastrar_produto_db  # Importa a função do MySQL
from datetime import datetime

def produto(page: ft.Page, on_stock):
    page.controls.clear()
    page.padding = 20

    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_input = "#0A122A" if is_dark else "#FFFFFF"
    cor_borda_input = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_input = "white" if is_dark else "black"
    cor_label = ft.Colors.TEAL_700 if is_dark else ft.Colors.TEAL_900

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_stock()),
        title=ft.Text("Novo Produto", size=20, weight="bold", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    def estilo_input(label, hint="", value="", read_only=False, col=None, keyboard_type=ft.KeyboardType.TEXT):
        input_field = ft.TextField(
            value=value, hint_text=hint, border=ft.InputBorder.NONE,
            content_padding=15, read_only=read_only, text_style=ft.TextStyle(color=cor_texto_input),
            expand=True, keyboard_type=keyboard_type
        )
        container = ft.Column([
            ft.Text(label, size=11, color=cor_label, weight="bold"),
            ft.Container(
                content=input_field, bgcolor=cor_fundo_input,
                border=ft.border.all(1, cor_borda_input), border_radius=10,
                padding=ft.padding.only(right=10),
            )
        ], spacing=5, col=col)
        return container, input_field

    # --- CAMPOS DO FORMULÁRIO ---
    nome_c, nome_in = estilo_input("NOME DO PRODUTO", col=12)
    cod_c, cod_in = estilo_input("CÓDIGO DE BARRAS", hint="Digite o EAN", col=12)
    # IDs fixos em 1 por enquanto (como no seu exemplo) ou vincular a busca de categorias
    forn_c, forn_in = estilo_input("ID FORNECEDOR", value="1", col=6, keyboard_type=ft.KeyboardType.NUMBER)
    cat_c, cat_in = estilo_input("ID CATEGORIA", value="1", col=6, keyboard_type=ft.KeyboardType.NUMBER)
    
    qtd_c, qtd_in = estilo_input("QUANTIDADE", value="0", col=4, keyboard_type=ft.KeyboardType.NUMBER)
    lote_c, lote_in = estilo_input("LOTE", hint="Ex: L468", col=4)
    emb_c, emb_in = estilo_input("EMBALAGEM", value="Unidade", col=4)

    custo_c, custo_in = estilo_input("PREÇO CUSTO (R$)", value="0.00", col=6, keyboard_type=ft.KeyboardType.NUMBER)
    venda_c, venda_in = estilo_input("PREÇO VENDA (R$)", value="0.00", col=6, keyboard_type=ft.KeyboardType.NUMBER)
    
    val_c, val_in = estilo_input("VALIDADE (AAAA-MM-DD)", value="2026-12-31", col=12)

    def salvar_clique(e):
        if not nome_in.value or not cod_in.value:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha Nome e Código!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
        
        try:
            cadastrar_produto_db(
                id_fornecedor=int(forn_in.value),
                id_categoria=int(cat_in.value),
                nome=nome_in.value,
                codigo=cod_in.value,
                validade=val_in.value,
                entrada=datetime.now().strftime("%Y-%m-%d"),
                custo=float(custo_in.value),
                venda=float(venda_in.value),
                embalagem=emb_in.value,
                qtd=int(qtd_in.value),
                lote=lote_in.value
            )
            page.snack_bar = ft.SnackBar(ft.Text("Produto cadastrado no MySQL!"), bgcolor="green")
            page.snack_bar.open = True
            on_stock() # Volta para o estoque para ver o novo item
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    layout_campos = ft.ResponsiveRow(
        controls=[nome_c, cod_c, forn_c, cat_c, qtd_c, lote_c, emb_c, custo_c, venda_c, val_c],
        spacing=15, run_spacing=15,
    )

    page.add(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment="center",
            controls=[
                ft.Divider(height=10, color="transparent"),
                layout_campos,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Cadastrar no Sistema", on_click=salvar_clique, 
                    width=250, height=50,
                    style=ft.ButtonStyle(bgcolor="#1B4F9C", color="white", shape=ft.RoundedRectangleBorder(radius=12))
                ),
                ft.Container(height=40) # Respiro no fundo
            ]
        )
    )
    page.update()