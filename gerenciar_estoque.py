import flet as ft

def estoque(page: ft.Page, on_home, on_users, on_perfil, on_adicionar_produto, on_editar_produto, on_logout):

    page.controls.clear()
    page.appbar = None
    
    # REMOVIDO: page.bgcolor e page.theme_mode fixos
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Lógica de cores adaptáveis para o tema
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_container_bg = "#111B3D" if is_dark else "#F0F2F8"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = ft.Colors.GREY_500
    cor_borda_busca = "#1e293b" if is_dark else "#D1D5DB"
    cor_fundo_busca = "#0d1626" if is_dark else "#FFFFFF"

    # -----------------
    # APPBAR (Mantida escura para destaque, ou mude para adaptável se preferir)
    # -----------------
    page.appbar = ft.AppBar(
        bgcolor="#0b1445",
        toolbar_height=70,
        leading=ft.Container(width=40),
        title=ft.Text(
            "Vende de Tudo",
            size=18 if page.width < 600 else 22,
            weight=ft.FontWeight.BOLD,
            color="white"
        ),
        center_title=True,
        actions=[
            ft.IconButton(
                icon=ft.Icons.EXIT_TO_APP,
                icon_color="white",
                tooltip="Sair",
                on_click=lambda _: on_logout()
            )
        ]
    )

    # -----------------
    # CARD PRODUTO (Adaptável)
    # -----------------
    def card_produto(cod, nome, preco, marca, validade, quantidade):
        qtd_num = int(quantidade)
        cor_status = "#00b40d" if qtd_num > 10 else "#ff9800"

        return ft.Container(
            padding=15,
            border_radius=15,
            bgcolor=cor_container_bg, # Dinâmico
            margin=ft.margin.only(bottom=5),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column([
                                ft.Text(cod, size=10, color=cor_texto_secundario),
                                ft.Text(nome, size=18, weight="bold", color=cor_texto_principal),
                            ], spacing=2),
                            ft.Column([
                                ft.Text(f"R$ {preco}", weight="bold", size=18, color=cor_texto_principal),
                                ft.Text(marca, size=11, color=cor_texto_secundario),
                            ], horizontal_alignment=ft.CrossAxisAlignment.END),
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(f"Validade: {validade}", size=11, color=ft.Colors.BLUE_GREY_400),
                            ft.Container(
                                content=ft.Text(f"{quantidade} UN", size=11, weight="bold", color="white"),
                                bgcolor=cor_status,
                                padding=ft.padding.symmetric(horizontal=12, vertical=4),
                                border_radius=20,
                            ),
                        ]
                    ),
                    ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, cor_texto_principal)),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.TextButton(
                                "Editar Produto",
                                icon=ft.Icons.EDIT_NOTE,
                                icon_color="#2196f3",
                                on_click=lambda e: on_editar_produto()
                            ),
                        ],
                    ),
                ],
            ),
        )

    # -----------------
    # HEADER
    # -----------------
    header = ft.Row(
        controls=[
            ft.Text("Consultar Estoque", size=22, weight="bold", color=cor_texto_principal),
            ft.FloatingActionButton(
                icon=ft.Icons.ADD,
                bgcolor="#1B4F9C",
                mini=True,
                on_click=lambda e: on_adicionar_produto()
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # -----------------
    # BUSCA (Adaptável)
    # -----------------
    search_field = ft.TextField(
        hint_text="Buscar...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=15,
        height=50,
        bgcolor=cor_fundo_busca,
        border_color=cor_borda_busca,
        hint_style=ft.TextStyle(color=cor_texto_secundario),
        content_padding=10,
        color=cor_texto_principal,
    )

    # -----------------
    # LISTA DE PRODUTOS
    # -----------------
    lista_produtos = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=15,
        controls=[
            card_produto("ML-873", "Moletom", "80,00", "DELLIMODES", "01/04/2029", "5"),
            card_produto("CL-627", "Calça", "60,00", "BELLETICOS", "01/09/2029", "132"),
            card_produto("BM-843", "Bermuda", "35,00", "TECIDOSPKM", "04/04/2032", "123"),
            card_produto("BN-346", "Boné", "40,00", "CAPMODAS", "17/11/2030", "654"),
            card_produto("TN-763", "Tênis", "90,00", "PISAFORO", "23/01/2031", "761"),
        ],
    )

    conteudo = ft.Column(
        expand=True,
        spacing=15,
        controls=[header, search_field, lista_produtos]
    )

    page.add(conteudo)

    # -------------------------
    # NAVIGATION BAR
    # -------------------------
    def trocar_aba(e):
        index = nav.selected_index
        if index == 0: on_home()
        elif index == 1: pass
        elif index == 2: on_users()
        elif index == 3: on_perfil()

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=1,
        on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicial"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, selected_icon=ft.Icons.INVENTORY_2, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, selected_icon=ft.Icons.GROUP, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Perfil"),
        ]
    )

    page.navigation_bar = ft.Container(
        content=nav,
        margin=ft.margin.only(left=25, right=25, bottom=30),
        border_radius=40,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )

    page.update()