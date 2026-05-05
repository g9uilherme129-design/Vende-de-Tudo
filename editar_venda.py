import flet as ft
from database import (
    buscar_venda_por_id,  # Certifique-se que essa função existe no database
    atualizar_venda_db,   # Certifique-se que essa função existe no database
    buscar_produtos_estoque
)
from datetime import datetime

def editar_venda(page: ft.Page, on_vendas, id_venda):
    page.controls.clear()
    page.padding = 0

    # Busca dados da venda
    v = buscar_venda_por_id(id_venda)
    produtos_db = buscar_produtos_estoque()

    # --- FUNÇÕES DE DATA ---
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
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_vendas()),
        title=ft.Text("Editar Venda", color="white", weight="bold"),
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

    # --- CAMPOS ---
    # Dropdown de Produtos
    drop_produto = ft.Dropdown(
        value=str(v.get('id_estoque')),
        options=[ft.dropdown.Option(key=str(p['id_estoque']), text=p['nome_estoque']) for p in produtos_db],
        border=ft.InputBorder.NONE, expand=True
    )

    in_quantidade = ft.TextField(value=str(v.get('quantidade_vendida')), border=ft.InputBorder.NONE, expand=True)
    in_preco_total = ft.TextField(value=str(v.get('preco_total')), border=ft.InputBorder.NONE, expand=True)
    in_data = ft.TextField(value=formatar_para_br(v.get('data_venda')), border=ft.InputBorder.NONE, expand=True)
    
    drop_metodo = ft.Dropdown(
        value=v.get('metodo_pagamento'),
        options=[
            ft.dropdown.Option("Dinheiro"), 
            ft.dropdown.Option("Cartão Crédito"), 
            ft.dropdown.Option("Cartão Débito"),
            ft.dropdown.Option("Pix")
        ],
        border=ft.InputBorder.NONE, expand=True
    )

    def salvar(e):
        try:
            atualizar_venda_db(
                id_venda,
                drop_produto.value,
                in_quantidade.value,
                in_preco_total.value,
                formatar_para_banco(in_data.value),
                drop_metodo.value
            )
            page.snack_bar = ft.SnackBar(ft.Text("Venda atualizada!"), bgcolor="#08D345")
            page.snack_bar.open = True
            on_vendas()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    page.add(
        ft.Column(
            expand=True, horizontal_alignment="center", scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    width=600, padding=25,
                    content=ft.Column([
                        ft.Text(f"Venda #{id_venda}", size=22, weight="bold"),
                        ft.ResponsiveRow([
                            criar_campo("PRODUTO", drop_produto, 12),
                            criar_campo("QUANTIDADE", in_quantidade, 6),
                            criar_campo("VALOR TOTAL", in_preco_total, 6),
                            criar_campo("DATA DA VENDA", in_data, 6),
                            criar_campo("PAGAMENTO", drop_metodo, 6),
                        ], spacing=15),
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "ATUALIZAR VENDA", on_click=salvar,
                            bgcolor="#1B4F9C", color="white", height=55, width=600,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                        )
                    ])
                )
            ]
        )
    )
    page.update()