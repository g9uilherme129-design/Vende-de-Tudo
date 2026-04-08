import flet as ft
from database import buscar_usuarios_db # Importando a nova função

def vendas(page: ft.Page, on_home, on_users, on_perfil, on_stock, on_nova_venda, on_detalhes_venda, on_logout):

    page.controls.clear()
    page.padding = 20
    
    # Lógica de cores adaptáveis (Mantida do original)
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_container_bg = "#0b1445" if is_dark else "#F0F2F8"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = ft.Colors.GREY_500
    cor_borda_busca = "#1e293b" if is_dark else "#D1D5DB"
    cor_fundo_busca = "#0d1626" if is_dark else "#FFFFFF"

    # --- BUSCA DADOS REAIS DE VENDAS ---
    try:
        # Substitua pela sua função real de busca de vendas
        vendas_db = buscar_historico_vendas() 
    except Exception as ex:
        print(f"Erro ao carregar histórico de vendas: {ex}")
        vendas_db = []

    lista_vendas_ui = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)

    # --- CARD DE VENDA ---
    def card_venda(id_venda, cliente, valor_total, forma_pagamento, data, status):
        # Lógica de cor baseada no status da venda
        if status.lower() == "concluída":
            cor_status = "#00b40d" # Verde
        elif status.lower() == "cancelada":
            cor_status = "#d32f2f" # Vermelho
        else:
            cor_status = "#ff9800" # Laranja (Pendente, etc)

        return ft.Container(
            padding=15, border_radius=15, bgcolor=cor_container_bg,
            content=ft.Column(spacing=10, controls=[
                ft.Row(alignment="spaceBetween", controls=[
                    ft.Column([
                        ft.Text(f"Pedido: #{id_venda}", size=10, color=cor_texto_secundario),
                        ft.Text(cliente, size=18, weight="bold", color=cor_texto_principal),
                    ], spacing=2),
                    ft.Column([
                        ft.Text(f"R$ {valor_total:.2f}", weight="bold", size=18, color=cor_texto_principal),
                        ft.Text(forma_pagamento, size=11, color=cor_texto_secundario),
                    ], horizontal_alignment="end"),
                ]),
                ft.Row(alignment="spaceBetween", controls=[
                    ft.Text(f"Data: {data}", size=11, color=ft.Colors.BLUE_GREY_400),
                    ft.Container(
                        content=ft.Text(status.upper(), size=11, weight="bold", color="white"),
                        bgcolor=cor_status, padding=ft.padding.symmetric(horizontal=12, vertical=4), border_radius=20,
                    ),
                ]),
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, cor_texto_principal)),
                ft.Row(alignment="end", controls=[
                    # Botão adaptado para ver detalhes da venda ou emitir recibo
                    ft.TextButton(
                        "Ver Detalhes", 
                        icon=ft.Icons.RECEIPT_LONG, 
                        on_click=lambda _: on_detalhes_venda(id_venda)
                    ),
                ]),
            ])
        )


#---- dps termino
    # # --- LÓGICA FILTRO E BUSCA ---
    # def filtrar_usuarios(e=None):
    #     t = search_field.value.lower()
    #     c = btn_filtro.data
        
    #     # Busca por nome ou e-mail
    #     filtrados = [u for u in usuarios_db if t in u["nome_user"].lower() or t in u["email_user"].lower()]

    #     if c == "alfabetica": filtrados.sort(key=lambda x: x["nome_user"])
    #     elif c == "admin": filtrados = [u for u in filtrados if u["perfil"].lower() == "admin"]
    #     elif c == "inativos": filtrados = [u for u in filtrados if not u["status_user"]]

    #     lista_vendas_ui.controls.clear()
    #     for u in filtrados:
    #         lista_vendas_ui.controls.append(vendas_card(u))
    #     page.update()

    # search_field = ft.TextField(
    #     hint_text="Buscar usuário...", prefix_icon=ft.Icons.SEARCH, expand=True,
    #     on_change=filtrar_usuarios, bgcolor=cor_fundo_busca, border_radius=15
    # )

    # btn_filtro = ft.PopupMenuButton(icon=ft.Icons.FILTER_LIST, items=[
    #     ft.PopupMenuItem(content=ft.Text("Ordem Alfabética"), on_click=lambda _: mudar_f("alfabetica")),
    #     ft.PopupMenuItem(content=ft.Text("Recentes"), on_click=lambda _: mudar_f("")),
    #     ft.PopupMenuItem(content=ft.Text("Preço"), on_click=lambda _: mudar_f("")),
    # ])
    # btn_filtro.data = "alfabetica"
    # def mudar_f(c): btn_filtro.data = c; filtrar_usuarios()

    # AppBar
    page.appbar = ft.AppBar(
        bgcolor="#0b1445", title=ft.Text("Vendas", color="white", weight="bold"),
        center_title=True, actions=[ft.IconButton(ft.Icons.EXIT_TO_APP, icon_color="white", on_click=lambda _: on_logout())]
    )

    # page.add(ft.Column(expand=True, controls=[
    #     ft.Row([
    #         ft.Text("Gerenciar Usuários", size=22, weight="bold"),
    #         ft.FloatingActionButton(icon=ft.Icons.ADD, bgcolor="#1B4F9C", mini=True, on_click=lambda _: on_adicionar_usuario())
    #     ], alignment="spaceBetween"),
    #     ft.Row([search_field, btn_filtro]),
    #     lista_vendas_ui
    # ]))

    # Navigation Bar
    # --- FUNÇÃO DE NAVEGAÇÃO ---
    def trocar_aba(e):
        idx = e.control.selected_index
        if idx == 0:
            on_home()
        elif idx == 1:
            pass # Já estamos em Vendas
        elif idx == 2:
            on_stock()
        elif idx == 3:
            on_users()
        elif idx == 4:
            on_perfil()

    # --- WIDGET DA NAVBAR ---
    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=1, # Define o ícone de Vendas (segunda posição) como ativo
        on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
            ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
        ]
    )
    page.navigation_bar = ft.Container(content=nav, margin=ft.margin.only(left=25, right=25, bottom=30), border_radius=40, clip_behavior="antiAlias")
    
    # filtrar_usuarios()