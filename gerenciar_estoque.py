import flet as ft
from database import buscar_produtos_estoque, buscar_categorias 

def estoque(page: ft.Page, on_home, on_users, on_perfil, on_vendas, on_adicionar_produto, on_editar_produto, on_logout):

    page.controls.clear()
    page.appbar = None
    
    # --- CORES E TEMA ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_container_bg = "#111B3D" if is_dark else "#F0F2F8"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = ft.Colors.GREY_500
    cor_fundo_busca = "#0d1626" if is_dark else "#FFFFFF"

    # --- BUSCA DADOS REAIS ---
    try:
        produtos_db = buscar_produtos_estoque()
        categorias_reais = buscar_categorias() 
    except Exception as ex:
        print(f"Erro ao carregar dados: {ex}")
        produtos_db = []
        categorias_reais = []

    lista_produtos_ui = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)

    # --- CARD PRODUTO ---
    def card_produto(id_prod, nome, preco, marca, validade, quantidade, categoria_nome="Geral"):
        cor_status = "#00b40d" if quantidade > 10 else "#ff9800"
        return ft.Container(
            padding=15, border_radius=15, bgcolor=cor_container_bg,
            content=ft.Column(spacing=10, controls=[
                ft.Row(alignment="spaceBetween", controls=[
                    ft.Column([
                        ft.Text(f"ID: {id_prod} | {categoria_nome}", size=10, color=cor_texto_secundario),
                        ft.Text(nome, size=18, weight="bold", color=cor_texto_principal),
                    ], spacing=2),
                    ft.Column([
                        ft.Text(f"R$ {preco:.2f}", weight="bold", size=18, color=cor_texto_principal),
                        ft.Text(marca, size=11, color=cor_texto_secundario),
                    ], horizontal_alignment="end"),
                ]),
                ft.Row(alignment="spaceBetween", controls=[
                    ft.Text(f"Validade: {validade}", size=11, color=ft.Colors.BLUE_GREY_400),
                    ft.Container(
                        content=ft.Text(f"{quantidade} UN", size=11, weight="bold", color="white"),
                        bgcolor=cor_status, padding=ft.padding.symmetric(horizontal=12, vertical=4), border_radius=20,
                    ),
                ]),
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, cor_texto_principal)),
                ft.Row(alignment="end", controls=[
                    ft.TextButton("Editar", icon=ft.Icons.EDIT_NOTE, on_click=lambda _: on_editar_produto(id_prod)),
                ]),
            ])
        )

    # --- LÓGICA DE FILTRAGEM ---
    def filtrar_estoque(e=None):
        texto = search_field.value.lower()
        criterio = btn_filtro.data
        
        filtrados = [
            p for p in produtos_db 
            if texto in p["nome_estoque"].lower() 
            or texto in p["marca"].lower()
            or texto in p.get("nome_categoria", "").lower()
        ]

        if criterio == "caro": 
            filtrados.sort(key=lambda x: x["preco_venda"], reverse=True)
        elif criterio == "barato": 
            filtrados.sort(key=lambda x: x["preco_venda"])
        elif criterio == "estoque_baixo": 
            filtrados.sort(key=lambda x: x["quantidade"])
        elif criterio != "todos":
            filtrados = [p for p in filtrados if p.get("nome_categoria") == criterio]

        lista_produtos_ui.controls.clear()
        for p in filtrados:
            lista_produtos_ui.controls.append(
                card_produto(
                    p["id_estoque"], p["nome_estoque"], p["preco_venda"], 
                    p["marca"], p["data_validade"], p["quantidade"],
                    p.get("nome_categoria", "Geral")
                )
            )
        page.update()

    def mudar_f(c): 
        btn_filtro.data = c
        filtrar_estoque()

    # --- MONTAGEM DO MENU (CORRIGIDA) ---
    menu_items = [
        ft.PopupMenuItem(content=ft.Text("Todos os Produtos"), on_click=lambda _: mudar_f("todos")),
        ft.PopupMenuItem(content=ft.Text("Mais Caro"), on_click=lambda _: mudar_f("caro")),
        ft.PopupMenuItem(content=ft.Text("Mais Barato"), on_click=lambda _: mudar_f("barato")),
        ft.PopupMenuItem(content=ft.Text("Estoque Baixo"), on_click=lambda _: mudar_f("estoque_baixo")),
    ]

    # Adiciona categorias dinâmicas
    if categorias_reais:
        # Usamos um texto simples como divisor para evitar erro de versão
        menu_items.append(ft.PopupMenuItem(content=ft.Text("----------", text_align="center"), disabled=True))
        for cat in categorias_reais:
            menu_items.append(
                ft.PopupMenuItem(
                    content=ft.Text(cat), 
                    on_click=lambda e, c=cat: mudar_f(c)
                )
            )

    btn_filtro = ft.PopupMenuButton(icon=ft.Icons.SORT, items=menu_items)
    btn_filtro.data = "todos"

    search_field = ft.TextField(
        hint_text="Buscar no estoque...", expand=True, on_change=filtrar_estoque,
        bgcolor=cor_fundo_busca, border_radius=15, prefix_icon=ft.Icons.SEARCH
    )

    page.appbar = ft.AppBar(
        bgcolor="#0b1445", 
        title=ft.Text("Estoque Real", color="white", weight="bold"),
        center_title=True, 
        actions=[ft.IconButton(ft.Icons.EXIT_TO_APP, icon_color="white", on_click=lambda _: on_logout())]
    )

    page.add(
        ft.Column(expand=True, spacing=15, controls=[
            ft.Row([
                ft.Text("Consultar Produtos", size=22, weight="bold"),
                ft.FloatingActionButton(icon=ft.Icons.ADD, bgcolor="#1B4F9C", mini=True, on_click=lambda _: on_adicionar_produto()),
            ], alignment="spaceBetween"),
            ft.Row([search_field, btn_filtro]),
            lista_produtos_ui
        ])
    )

    def trocar_aba(e):
        idx = e.control.selected_index
        if idx == 0: on_home()
        elif idx == 1: on_vendas()
        elif idx == 2: pass 
        elif idx == 3: on_users()
        elif idx == 4: on_perfil()

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=2,
        on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
            ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
        ]
    )
    
    page.navigation_bar = ft.Container(
        content=nav, margin=ft.margin.only(left=25, right=25, bottom=30), 
        border_radius=40, clip_behavior=ft.ClipBehavior.ANTI_ALIAS
    )
    
    filtrar_estoque()
