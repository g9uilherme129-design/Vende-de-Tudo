import flet as ft
from database import buscar_produtos_estoque # Importando a nova função

def estoque(page: ft.Page, on_home, on_users, on_perfil, on_adicionar_produto, on_editar_produto, on_logout):

    page.controls.clear()
    page.padding = 20
    
    # Lógica de cores adaptáveis
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_container_bg = "#0b1445" if is_dark else "#F0F2F8"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = ft.Colors.GREY_500
    cor_borda_busca = "#1e293b" if is_dark else "#D1D5DB"
    cor_fundo_busca = "#0d1626" if is_dark else "#FFFFFF"

    # --- BUSCA DADOS REAIS ---
    try:
        produtos_db = buscar_produtos_estoque()
    except Exception as ex:
        print(f"Erro ao carregar estoque: {ex}")
        produtos_db = []

    lista_produtos_ui = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)

    # --- CARD PRODUTO ---
    def card_produto(id_prod, nome, preco, marca, validade, quantidade):
        cor_status = "#00b40d" if quantidade > 10 else "#ff9800"
        return ft.Container(
            padding=15, border_radius=15, bgcolor=cor_container_bg,
            content=ft.Column(spacing=10, controls=[
                ft.Row(alignment="spaceBetween", controls=[
                    ft.Column([
                        ft.Text(f"ID: {id_prod}", size=10, color=cor_texto_secundario),
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

    # --- FILTRAGEM ---
    def filtrar_estoque(e=None):
        texto = search_field.value.lower()
        criterio = btn_filtro.data
        
        filtrados = [p for p in produtos_db if texto in p["nome_estoque"].lower() or texto in p["marca"].lower()]

        if criterio == "caro": filtrados.sort(key=lambda x: x["preco_venda"], reverse=True)
        elif criterio == "barato": filtrados.sort(key=lambda x: x["preco_venda"])
        elif criterio == "estoque_baixo": filtrados.sort(key=lambda x: x["quantidade"])

        lista_produtos_ui.controls.clear()
        for p in filtrados:
            lista_produtos_ui.controls.append(
                card_produto(p["id_estoque"], p["nome_estoque"], p["preco_venda"], p["marca"], p["data_validade"], p["quantidade"])
            )
        page.update()

    search_field = ft.TextField(
        hint_text="Buscar no estoque...", expand=True, on_change=filtrar_estoque,
        bgcolor=cor_fundo_busca, border_radius=15, prefix_icon=ft.Icons.SEARCH
    )

    btn_filtro = ft.PopupMenuButton(icon=ft.Icons.SORT, items=[
        ft.PopupMenuItem(content=ft.Text("Mais Caro"), on_click=lambda _: mudar_f("caro")),
        ft.PopupMenuItem(content=ft.Text("Mais Barato"), on_click=lambda _: mudar_f("barato")),
        ft.PopupMenuItem(content=ft.Text("Estoque Baixo"), on_click=lambda _: mudar_f("estoque_baixo")),
    ])
    btn_filtro.data = "estoque_baixo"
    def mudar_f(c): btn_filtro.data = c; filtrar_estoque()

    # AppBar
    page.appbar = ft.AppBar(
        bgcolor="#0b1445", title=ft.Text("Estoque Real", color="white", weight="bold"),
        center_title=True, actions=[ft.IconButton(ft.Icons.EXIT_TO_APP, icon_color="white", on_click=lambda _: on_logout())]
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

    # Navbar
    nav = ft.NavigationBar(
        bgcolor="#0b1445", selected_index=1,
        on_change=lambda e: [on_home(), None, on_users(), on_perfil()][e.control.selected_index],
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
        ]
    )
    page.navigation_bar = ft.Container(content=nav, margin=ft.margin.only(left=25, right=25, bottom=30), border_radius=40, clip_behavior="antiAlias")
    
    filtrar_estoque() # Carrega a lista inicial