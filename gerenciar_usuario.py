import flet as ft
from database import buscar_usuarios_db

def usuarios(page: ft.Page, on_home, on_stock, on_vendas, on_perfil, on_logout, on_adicionar_usuario, on_editar_usuario, on_desativar_usuario):

    page.controls.clear()
    page.padding = 20

    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_container_bg = "#0b1445" if is_dark else "#F0F2F8"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = ft.Colors.GREY_500
    cor_fundo_busca = "#0d1626" if is_dark else "#FFFFFF"

    # --- BUSCA DADOS REAIS ---
    usuarios_db = buscar_usuarios_db()
    lista_usuarios_ui = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=10)

    def formatar_moeda(valor):
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # --- CARD USUÁRIO ---
    def user_card(u):
        status_texto = "ATIVO" if u["status_user"] else "INATIVO"
        cor_status = "#00b40d" if u["status_user"] else "#ff0008"
        
        # Ícone e Cor baseada no perfil
        is_admin = u["perfil"].lower() == "admin"
        icone_perfil = ft.Icons.SECURITY if is_admin else ft.Icons.PERSON
        cor_perfil = ft.Colors.BLUE_800 if is_admin else ft.Colors.ORANGE_700

        return ft.Container(
            bgcolor=cor_container_bg, 
            border_radius=15, 
            padding=15,
            content=ft.Column(spacing=10, controls=[
                # Linha ID e CPF
                ft.Row(alignment="spaceBetween", controls=[
                    ft.Text(f"ID: {u['id_user']}", size=12, color=cor_texto_secundario, weight="bold"),
                    ft.Text(f"CPF: {u['cpf']}", size=12, color=cor_texto_secundario),
                ]),
                
                # Linha Principal (Avatar + Nome + Vendas)
                ft.Row(
                    alignment="spaceBetween", 
                    vertical_alignment="center", 
                    controls=[
                        ft.Row([
                            ft.CircleAvatar(
                                content=ft.Icon(icone_perfil, color="white", size=25),
                                bgcolor=cor_perfil,
                                radius=25,
                            ),
                            ft.Column([
                                ft.Text(u["nome_user"], size=18, weight="bold", color=cor_texto_principal),
                                ft.Row([
                                    ft.Text(u["perfil"].upper(), size=11, color=ft.Colors.BLUE_GREY_400),
                                    ft.Text(" • ", color=cor_texto_secundario),
                                    ft.Text(f"{u['total_vendas']} VENDAS", size=11, color="#08D345", weight="bold"),
                                ])
                            ], spacing=2),
                        ], spacing=15),
                        
                        ft.Container(
                            content=ft.Text(status_texto, size=10, weight="bold", color="white"),
                            bgcolor=cor_status, 
                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                            border_radius=20
                        )
                    ]
                ),
                
                # E-mail e Salário
                ft.Row(alignment="spaceBetween", controls=[
                    ft.Text(f"✉ {u['email_user']}", size=12, color=cor_texto_secundario),
                    ft.Text(f"Salário: {formatar_moeda(u['salario'])}", size=13, weight="bold", color=cor_texto_principal),
                ]),

                ft.Divider(height=1, color=ft.Colors.WHITE10),
                
                # Botões de Ação
                ft.Row(alignment="end", spacing=10, controls=[
                    ft.TextButton("Editar", icon=ft.Icons.EDIT_NOTE, on_click=lambda _: on_editar_usuario(u['id_user'])),
                    ft.ElevatedButton(
                        "Desativar" if u["status_user"] else "Reativar",
                        bgcolor="#991f23" if u["status_user"] else "#00b40d",
                        color="white",
                        on_click=lambda _: on_desativar_usuario(u)
                    ),
                ])
            ])
        )

    # --- LÓGICA FILTRO E BUSCA ---
    def filtrar_usuarios(e=None):
        t = search_field.value.lower()
        c = btn_filtro.data
        
        filtrados = [u for u in usuarios_db if t in u["nome_user"].lower() or t in u["email_user"].lower()]

        # Aplicando filtros específicos
        if c == "id":
            filtrados.sort(key=lambda x: x["id_user"])
        elif c == "vendas":
            filtrados.sort(key=lambda x: x["total_vendas"], reverse=True)
        elif c == "alfabetica":
            filtrados.sort(key=lambda x: x["nome_user"])
        elif c == "inativos":
            filtrados = [u for u in filtrados if not u["status_user"]]

        lista_usuarios_ui.controls.clear()
        for u in filtrados:
            lista_usuarios_ui.controls.append(user_card(u))
        page.update()

    def mudar_f(c): 
        btn_filtro.data = c
        filtrar_usuarios()

    search_field = ft.TextField(
        hint_text="Buscar por nome ou e-mail...", prefix_icon=ft.Icons.SEARCH, expand=True,
        on_change=filtrar_usuarios, bgcolor=cor_fundo_busca, border_radius=15
    )

    btn_filtro = ft.PopupMenuButton(icon=ft.Icons.FILTER_LIST, items=[
        ft.PopupMenuItem(content=ft.Text("Ordem Alfabética"), on_click=lambda _: mudar_f("alfabetica")),
        ft.PopupMenuItem(content=ft.Text("Por ID"), on_click=lambda _: mudar_f("id")),
        ft.PopupMenuItem(content=ft.Text("Mais Vendas"), on_click=lambda _: mudar_f("vendas")),
        ft.PopupMenuItem(content=ft.Text("Apenas Inativos"), on_click=lambda _: mudar_f("inativos")),
    ])
    btn_filtro.data = "alfabetica"

    # Layout da Página
    page.appbar = ft.AppBar(
        bgcolor="#0b1445", title=ft.Text("Equipe de Vendas", color="white", weight="bold"),
        center_title=True, actions=[ft.IconButton(ft.Icons.EXIT_TO_APP, icon_color="white", on_click=lambda _: on_logout())]
    )

    page.add(
        ft.Column(expand=True, controls=[
            ft.Row([
                ft.Text("Gerenciar Usuários", size=24, weight="bold", color=cor_texto_principal),
                ft.FloatingActionButton(icon=ft.Icons.ADD, bgcolor="#1B4F9C", mini=True, on_click=lambda _: on_adicionar_usuario())
            ], alignment="spaceBetween"),
            ft.Row([search_field, btn_filtro]),
            lista_usuarios_ui
        ])
    )

    # Barra de Navegação
    def trocar_aba(e):
        idx = e.control.selected_index
        if idx == 0: on_home()
        elif idx == 1: on_vendas()
        elif idx == 2: on_stock()
        elif idx == 4: on_perfil()

    nav = ft.NavigationBar(
        bgcolor="#0b1445", selected_index=3, on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
            ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
        ]
    )
    page.navigation_bar = ft.Container(content=nav, margin=ft.margin.only(left=25, right=25, bottom=30), border_radius=40, clip_behavior="antiAlias")
    
    # Inicializa a lista
    filtrar_usuarios()