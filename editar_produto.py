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

    # --- PADRONIZAÇÃO DE CORES (IDÊNTICO AO RESTANTE DO APP) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D" # Azul ou Rosa suave
    cor_barra = "#0b1445" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_input_bg = "#0A122A" if is_dark else "#F5F7FB"
    cor_destaque = "#36D900" if is_dark else "#FF6C03"
    cor_secundaria =  "#1679f2" if is_dark else "#DA7D7D"

    p = buscar_produto_por_id(id_produto)
    categorias_db = buscar_categorias_dropdown() 
    fornecedores_db = buscar_fornecedores()

    # --- FUNÇÕES DE FORMATAÇÃO ---
    def formatar_data(e):
        valor = "".join(filter(str.isdigit, e.control.value))
        if len(valor) > 8: valor = valor[:8]
        if len(valor) >= 5:
            e.control.value = f"{valor[:2]}/{valor[2:4]}/{valor[4:]}"
        elif len(valor) >= 3:
            e.control.value = f"{valor[:2]}/{valor[2:]}"
        else:
            e.control.value = valor
        page.update()
    
    def formatar_moeda(e):
        valor = "".join(filter(str.isdigit, e.control.value))
        if not valor:
            e.control.value = "0,00"
        else:
            float_valor = float(valor) / 100
            e.control.value = f"{float_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        page.update()

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

    # --- UI COMPONENTS ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_stock()),
        title=ft.Text("Editar Produto", color="white", weight="bold"),
        bgcolor=cor_barra, center_title=True,
    )

    def criar_campo(label, control, col=None):
        return ft.Column([
            ft.Text(f"  {label}", size=11, color=cor_texto_s, weight="bold"),
            ft.Container(
                content=control, bgcolor=cor_input_bg,
                border=ft.border.all(1, cor_borda), border_radius=12,
                padding=ft.padding.symmetric(horizontal=10)
            )
        ], spacing=5, col=col)

    in_nome = ft.TextField(
        value=p.get('nome_estoque'), border=ft.InputBorder.NONE, expand=True,
        max_length=100, text_style=ft.TextStyle(color=cor_texto_p), cursor_color=cor_texto_s
    )
    in_preco_compra = ft.TextField(
        value=str(p.get('preco_unitario')), border=ft.InputBorder.NONE, expand=True, 
        on_change=formatar_moeda, text_style=ft.TextStyle(color=cor_texto_p)
    )
    in_preco_venda = ft.TextField(
        value=str(p.get('preco_venda')), border=ft.InputBorder.NONE, expand=True, 
        on_change=formatar_moeda, text_style=ft.TextStyle(color=cor_texto_p)
    )
    in_qtd = ft.TextField(
        value=str(p.get('quantidade')), border=ft.InputBorder.NONE, expand=True,
        text_style=ft.TextStyle(color=cor_texto_p)
    )
    in_validade = ft.TextField(
        on_change=formatar_data, keyboard_type=ft.KeyboardType.NUMBER,
        value=formatar_para_br(p.get('data_validade')), border=ft.InputBorder.NONE, expand=True,
        max_length=10, text_style=ft.TextStyle(color=cor_texto_p)
    )
    in_lote = ft.TextField(
        value=p.get('lote'), border=ft.InputBorder.NONE, expand=True,
        max_length=9, text_style=ft.TextStyle(color=cor_texto_p)
    )

    drop_cat = ft.Dropdown(
        value=str(p.get('id_categoria')),
        options=[ft.dropdown.Option(key=str(c['id_categoria']), text=c['nome_categoria']) for c in categorias_db],
        border=ft.InputBorder.NONE, expand=True, color=cor_texto_p
    )
    drop_forn = ft.Dropdown(
        value=str(p.get('id_fornecedor')),
        options=[ft.dropdown.Option(key=str(f['id_fornecedor']), text=f['nome_fornecedor']) for f in fornecedores_db],
        border=ft.InputBorder.NONE, expand=True, color=cor_texto_p
    )
    drop_emb = ft.Dropdown(
        value=p.get('embalagem'),
        options=[
            ft.dropdown.Option("UN"), ft.dropdown.Option("CX"), 
            ft.dropdown.Option("KG"), ft.dropdown.Option("LT"), ft.dropdown.Option("PCT")
        ],
        border=ft.InputBorder.NONE, expand=True, color=cor_texto_p
    )

    def salvar(e):
        try:
            atualizar_produto_db(
                id_produto, drop_forn.value, drop_cat.value, in_nome.value,
                formatar_para_banco(in_validade.value), in_preco_compra.value,
                in_preco_venda.value, drop_emb.value, in_qtd.value, in_lote.value
            )
            page.snack_bar = ft.SnackBar(ft.Text("Produto atualizado com sucesso!"), bgcolor=cor_destaque)
            page.snack_bar.open = True
            on_stock()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao salvar: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    # --- LAYOUT FINAL ---
    page.add(
        ft.Container(
            expand=True,
            bgcolor=cor_fundo_tela,
            content=ft.Column(
                horizontal_alignment="center", 
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        width=700, 
                        padding=30,
                        bgcolor=cor_fundo_card,
                        content=ft.Column([
                            ft.Text(f"Produto #{id_produto}", size=28, weight="bold", color=cor_texto_p),
                            ft.Text("Edite as informações técnicas e financeiras do item abaixo.", size=14, color=cor_secundaria),
                            ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                            
                            ft.ResponsiveRow([
                                criar_campo("NOME DO PRODUTO (Máx 100)", in_nome, 12),
                                criar_campo("CATEGORIA", drop_cat, 6),
                                criar_campo("FORNECEDOR", drop_forn, 6),
                                criar_campo("PREÇO CUSTO (R$)", in_preco_compra, 6),
                                criar_campo("PREÇO VENDA (R$)", in_preco_venda, 6),
                                criar_campo("QUANTIDADE EM ESTOQUE", in_qtd, 4),
                                criar_campo("UNIDADE MEDIDA", drop_emb, 4),
                                criar_campo("LOTE / IDENTIFICADOR", in_lote, 4),
                                criar_campo("DATA DE VALIDADE (DD/MM/AAAA)", in_validade, 12),
                            ], spacing=20),
                            
                            ft.Container(height=40),
                            
                            ft.ElevatedButton(
                                "SALVAR ALTERAÇÕES", 
                                on_click=salvar,
                                bgcolor=cor_texto_s, 
                                color="white", 
                                height=60, 
                                width=700,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    elevation=5
                                )
                            ),
                            ft.Container(height=20), # Margem inferior extra
                        ])
                    )
                ]
            )
        )
    )
    page.update()