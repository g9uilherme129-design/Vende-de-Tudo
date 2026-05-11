import flet as ft
from database import buscar_produtos_estoque, buscar_categorias 
from datetime import datetime

def estoque(page: ft.Page, on_home, on_users, on_perfil, on_vendas, on_adicionar_produto, on_editar_produto, on_logout, on_fornecedores, on_categorias):

    page.controls.clear()
    page.padding = 0 # Padding zero para o container de fundo preencher tudo
    
    # --- PADRONIZAÇÃO DE CORES (IDÊNTICO ÀS OUTRAS TELAS) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#0b1445" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_input = "#0A122A" if is_dark else "#F5F7FB"
    cor_secundaria =  "#1679f2" if is_dark else "#DA7D7D"
    cor_bar =  "#1679f2" if is_dark else "#BA7272"
    cort_3 = "#36D900" if is_dark else "#FF6C03"

    # --- FUNÇÃO AUXILIAR DATA ---
    def formatar_data_br(data_origem):
        try:
            if hasattr(data_origem, 'strftime'):
                return data_origem.strftime("%d/%m/%Y")
            dt = datetime.strptime(str(data_origem), "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except:
            return str(data_origem)

    # --- BUSCA DADOS REAIS ---
    try:
        produtos_db = buscar_produtos_estoque()
        categorias_reais = buscar_categorias() 
    except:
        produtos_db = []
        categorias_reais = []

    lista_produtos_ui = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)

    # --- CARD PRODUTO ---
    def card_produto(id_prod, nome, preco, marca, validade, quantidade, categoria_nome="Geral"):
        # Status de estoque: Verde se > 10, Laranja se > 0, Vermelho se 0
        if quantidade > 15: cor_status = "#00b40d"
        elif quantidade > 0: cor_status = "#ff4545"
        else: cor_status = "#ff4444"

        return ft.Container(
            padding=15, 
            border_radius=15, 
            bgcolor=cor_fundo_card,
            border=ft.border.all(1, cor_borda),
            content=ft.Column(spacing=10, controls=[
                ft.Row(alignment="spaceBetween", controls=[
                    ft.Column([
                        ft.Text(f"ID: {id_prod} | {categoria_nome.upper()}", size=10, color=cor_secundaria, weight="bold"),
                        ft.Text(nome, size=18, weight="bold", color=cor_texto_p),
                    ], spacing=2, expand=True),
                    ft.Column([
                        ft.Text(f"R$ {preco:.2f}", weight="bold", size=18, color=cort_3),
                        ft.Text(marca, size=11, color=cor_secundaria),
                    ], horizontal_alignment="end"),
                ]),
                ft.Row(alignment="spaceBetween", controls=[
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_MONTH_OUTLINED, size=14, color=cor_secundaria),
                        ft.Text(f"Validade: {validade}", size=11, color=cor_secundaria),
                    ], spacing=5),
                    ft.Container(
                        content=ft.Text(f"{quantidade} UN", size=11, weight="bold", color="white"),
                        bgcolor=cor_status, 
                        padding=ft.padding.symmetric(horizontal=12, vertical=4), 
                        border_radius=20,
                    ),
                ]),
                ft.Divider(height=1, color=ft.Colors.WHITE10),
                ft.Row(alignment="end", controls=[
                    ft.TextButton(
                        "Editar Produto", 
                        icon=ft.Icons.EDIT_OUTLINED, 
                        icon_color=cor_texto_s,
                        on_click=lambda _: on_editar_produto(id_prod)
                    ),
                ]),
            ])
        )

    # --- LÓGICA FILTRAGEM ---
    def filtrar_estoque(e=None):
        texto = search_field.value.lower() if search_field.value else ""
        criterio = btn_filtro.data
        
        filtrados = [
            p for p in produtos_db 
            if texto in p["nome_estoque"].lower() 
            or texto in p["marca"].lower()
            or texto in p.get("nome_categoria", "").lower()
        ]

        # Ordenação
        if criterio == "caro": filtrados.sort(key=lambda x: x["preco_venda"], reverse=True)
        elif criterio == "barato": filtrados.sort(key=lambda x: x["preco_venda"])
        elif criterio == "estoque_baixo": filtrados.sort(key=lambda x: x["quantidade"])
        elif criterio != "todos":
            filtrados = [p for p in filtrados if p.get("nome_categoria") == criterio]

        lista_produtos_ui.controls.clear()
        for p in filtrados:
            lista_produtos_ui.controls.append(
                card_produto(
                    p["id_estoque"], p["nome_estoque"], p["preco_venda"], 
                    p["marca"], formatar_data_br(p["data_validade"]), p["quantidade"],
                    p.get("nome_categoria", "Geral")
                )
            )
        page.update()

    def mudar_f(c): 
        btn_filtro.data = c
        filtrar_estoque()

    # --- COMPONENTES ---
    menu_items = [
        ft.PopupMenuItem(content=ft.Text("Todos os Produtos"), on_click=lambda _: mudar_f("todos")),
        ft.PopupMenuItem(content=ft.Text("Mais Caro"), on_click=lambda _: mudar_f("caro")),
        ft.PopupMenuItem(content=ft.Text("Mais Barato"), on_click=lambda _: mudar_f("barato")),
        ft.PopupMenuItem(content=ft.Text("Estoque Baixo"), on_click=lambda _: mudar_f("estoque_baixo")),
    ]

    if categorias_reais:
        menu_items.append(ft.PopupMenuItem(content=ft.Divider(height=1)))
        for cat in categorias_reais:
            menu_items.append(ft.PopupMenuItem(content=ft.Text(cat), on_click=lambda e, c=cat: mudar_f(c)))

    btn_filtro = ft.PopupMenuButton(icon=ft.Icons.SORT, icon_color=cor_texto_p, items=menu_items)
    btn_filtro.data = "todos"

    search_field = ft.TextField(
        hint_text="Buscar no estoque...", expand=True, on_change=filtrar_estoque,
        bgcolor=cor_input, border_radius=15, prefix_icon=ft.Icons.SEARCH,
        border_color=cor_borda, text_style=ft.TextStyle(color=cor_texto_p)
    )

    page.appbar = ft.AppBar(
        bgcolor=cor_barra, 
        title=ft.Text("Gestão de Estoque", color="white", weight="bold"),
        center_title=True, 
        actions=[ft.IconButton(ft.Icons.EXIT_TO_APP, icon_color="white", on_click=lambda _: on_logout())]
    )

    def trocar_aba(e):
        idx = e.control.selected_index
        if idx == 0: on_home()
        elif idx == 1: on_vendas()
        elif idx == 2: pass 
        elif idx == 3: on_users()
        elif idx == 4: on_perfil()

    page.navigation_bar = ft.Container(
        content=ft.NavigationBar(
            bgcolor=cor_barra, selected_index=2, on_change=trocar_aba,
            indicator_color=cor_bar,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
                ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"),
                ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2, label="Estoque"),
                ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Usuários"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
            ]
        ),
        margin=ft.margin.only(left=25, right=25, bottom=20),
        border_radius=40, clip_behavior=ft.ClipBehavior.ANTI_ALIAS
    )

    page.add(
        ft.Container(
            expand=True, bgcolor=cor_fundo_tela, padding=20,
            content=ft.Column(expand=True, spacing=15, controls=[
                ft.Row([
                    ft.Text("Meus Produtos", size=24, weight="bold", color=cor_texto_p),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.CATEGORY_ROUNDED,
                            icon_color=cor_texto_s,
                            tooltip="Categorias",
                            on_click=lambda _: on_categorias()
                        ),
                        ft.IconButton(
                            icon=ft.Icons.BUSINESS,
                            icon_color=cor_texto_s,
                            tooltip="Fornecedores",
                            on_click=lambda _: on_fornecedores()
                        ),
                        ft.FloatingActionButton(
                            icon=ft.Icons.ADD, 
                            bgcolor=cor_texto_s, 
                            tooltip="Novo Produto",
                            mini=True, 
                            on_click=lambda _: on_adicionar_produto()
                        ),
                    ], spacing=5)
                ], alignment="spaceBetween"),
                ft.Row([search_field, btn_filtro]),
                lista_produtos_ui
            ])
        )
    )
    
    filtrar_estoque()