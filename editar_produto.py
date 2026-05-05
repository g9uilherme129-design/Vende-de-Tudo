import flet as ft
from database import (
    buscar_produto_por_id, 
    atualizar_produto_db, 
    buscar_categorias_dropdown, 
    buscar_fornecedores
)
from datetime import datetime

def editar_produto(page: ft.Page, on_stock, id_produto):
    page.controls.clear()
    page.padding = 0

    p = buscar_produto_por_id(id_produto)
    categorias_db = buscar_categorias_dropdown() 
    fornecedores_db = buscar_fornecedores()

    def formatar_para_br(data_origem):
        try:
            if hasattr(data_origem, 'strftime'): return data_origem.strftime("%d/%m/%Y")
            dt = datetime.strptime(str(data_origem), "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except: return str(data_origem)

    def formatar_para_banco(data_br):
        try:
            dt = datetime.strptime(data_br, "%d/%m/%Y")
            return dt.strftime("%Y-%m-%d")
        except: return data_br

    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_input_fundo = "#0A122A" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_label = ft.Colors.TEAL_400 if is_dark else ft.Colors.TEAL_900

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_stock()),
        title=ft.Text("Editar Produto", color="white", weight="bold"),
        bgcolor="#0b1445", center_title=True,
    )

    def criar_campo(label, control, col=None):
        return ft.Column([
            ft.Text(f"  {label}", size=11, color=cor_label, weight="bold"),
            ft.Container(
                content=control, bgcolor=cor_input_fundo,
                border=ft.border.all(1, cor_borda), border_radius=12,
                padding=ft.padding.symmetric(horizontal=10)
            )
        ], spacing=5, col=col)

    # --- CAMPOS COM LIMITES (max_length agora sem o parâmetro que deu erro) ---
    in_nome = ft.TextField(
        value=p.get('nome_estoque'), border=ft.InputBorder.NONE, expand=True,
        max_length=100  # O Flet já mostra o contador "0/100" por padrão aqui
    )
    in_preco_compra = ft.TextField(
        value=str(p.get('preco_unitario')), border=ft.InputBorder.NONE, expand=True
    )
    in_preco_venda = ft.TextField(
        value=str(p.get('preco_venda')), border=ft.InputBorder.NONE, expand=True
    )
    in_qtd = ft.TextField(
        value=str(p.get('quantidade')), border=ft.InputBorder.NONE, expand=True
    )
    in_validade = ft.TextField(
        value=formatar_para_br(p.get('data_validade')), border=ft.InputBorder.NONE, expand=True,
        max_length=10
    )
    in_lote = ft.TextField(
        value=p.get('lote'), border=ft.InputBorder.NONE, expand=True,
        max_length=9
    )

    drop_cat = ft.Dropdown(
        value=str(p.get('id_categoria')),
        options=[ft.dropdown.Option(key=str(c['id_categoria']), text=c['nome_categoria']) for c in categorias_db],
        border=ft.InputBorder.NONE, expand=True
    )
    drop_forn = ft.Dropdown(
        value=str(p.get('id_fornecedor')),
        options=[ft.dropdown.Option(key=str(f['id_fornecedor']), text=f['nome_fornecedor']) for f in fornecedores_db],
        border=ft.InputBorder.NONE, expand=True
    )
    drop_emb = ft.Dropdown(
        value=p.get('embalagem'),
        options=[
            ft.dropdown.Option("UN"), ft.dropdown.Option("CX"), 
            ft.dropdown.Option("KG"), ft.dropdown.Option("LT"), ft.dropdown.Option("PCT")
        ],
        border=ft.InputBorder.NONE, expand=True
    )

    def salvar(e):
        try:
            atualizar_produto_db(
                id_produto,
                drop_forn.value,
                drop_cat.value,
                in_nome.value,
                formatar_para_banco(in_validade.value),
                in_preco_compra.value,
                in_preco_venda.value,
                drop_emb.value,
                in_qtd.value,
                in_lote.value
            )
            page.snack_bar = ft.SnackBar(ft.Text("Alterações salvas com sucesso!"), bgcolor="#08D345")
            page.snack_bar.open = True
            on_stock()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao salvar: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    page.add(
        ft.Column(
            expand=True, horizontal_alignment="center", scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    width=600, padding=25,
                    content=ft.Column([
                        ft.Text(f"Editar Produto #{id_produto}", size=22, weight="bold"),
                        ft.ResponsiveRow([
                            criar_campo("NOME DO PRODUTO (Máx 100)", in_nome, 12),
                            criar_campo("CATEGORIA", drop_cat, 6),
                            criar_campo("FORNECEDOR", drop_forn, 6),
                            criar_campo("PREÇO COMPRA", in_preco_compra, 4),
                            criar_campo("PREÇO VENDA", in_preco_venda, 4),
                            criar_campo("EMBALAGEM", drop_emb, 4),
                            criar_campo("QUANTIDADE", in_qtd, 4),
                            criar_campo("VALIDADE (DD/MM/YYYY)", in_validade, 4),
                            criar_campo("LOTE (Máx 9)", in_lote, 4),
                        ], spacing=15),
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "SALVAR ALTERAÇÕES", on_click=salvar,
                            bgcolor="#1B4F9C", color="white", height=55, width=600,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                        )
                    ])
                )
            ]
        )
    )
    page.update()