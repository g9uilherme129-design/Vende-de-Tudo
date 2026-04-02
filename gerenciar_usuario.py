import flet as ft

def usuarios(page: ft.Page, on_home, on_stock, on_perfil, on_logout, on_adicionar_usuario, on_editar_usuario):

    page.controls.clear()
    # REMOVIDO: page.bgcolor e page.theme_mode fixos
    page.padding = 20

    # Lógica de cores adaptáveis
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_container_bg = "#111B3D" if is_dark else "#F0F2F8"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = ft.Colors.GREY_500
    cor_fundo_busca = "#0d1626" if is_dark else "#FFFFFF"
    cor_borda_busca = "#1e293b" if is_dark else "#D1D5DB"

    def sair_app(e):
        on_logout()

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
                on_click=sair_app
            )
        ]
    )

    def status_badge(status):
        return ft.Container(
            content=ft.Text(
                status,
                size=12,
                weight="bold",
                color="white" # Texto sempre branco no selo colorido
            ),
            bgcolor="#00b40d" if status == "ATIVO" else "#ff0008",
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            border_radius=20,
        )

    def user_card(codigo, nome, cargo, admissao, status, detalhes=None):
        return ft.Container(
            bgcolor=cor_container_bg, # Dinâmico
            border_radius=15,
            padding=15,
            margin=ft.margin.only(bottom=10),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(codigo, size=12, color=cor_texto_secundario),
                            ft.Text(f"ADMISSÃO: {admissao}", size=12, color=cor_texto_secundario),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(nome, size=18, weight="bold", color=cor_texto_principal),
                                    ft.Text(cargo, size=13, color=ft.Colors.BLUE_GREY_400),
                                ],
                            ),
                            status_badge(status),
                        ],
                    ),
                    # Detalhes de Desativação
                    ft.Container(
                        visible=status == "INATIVO",
                        bgcolor=ft.Colors.with_opacity(0.1, "red"),
                        border=ft.border.all(1, "#991f23"),
                        border_radius=10,
                        padding=10,
                        content=ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text("MOTIVO DA INATIVIDADE", size=11, color="#ff4444", weight="bold"),
                                ft.Text(detalhes if detalhes else "Não especificado", size=12, color=cor_texto_principal, italic=True),
                            ],
                        ),
                    ),
                    ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, cor_texto_principal)),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10,
                        controls=[
                            ft.TextButton(
                                "Editar Usuário",
                                icon=ft.Icons.EDIT_NOTE,
                                icon_color="#2196f3",
                                on_click=lambda e: on_editar_usuario()
                            ),
                            ft.ElevatedButton(
                                "Desativar",
                                icon=ft.Icons.BLOCK,
                                visible=status == "ATIVO",
                                style=ft.ButtonStyle(
                                    bgcolor="#002072",
                                    color="white",
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=lambda e: print(f"Desativando {codigo}")
                            ),
                        ]
                    ),
                ],
            ),
        )

    lista_usuarios = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
        controls=[
            user_card("AD-001", "João Silva", "ADMINISTRADOR", "2023/01/10", "ATIVO"),
            user_card("VT-934", "Carlos Lima", "VENDEDOR", "2023/05/15", "INATIVO",
                "Pedido de demissão para novos projetos.\nData: 20/12/2025",
            ),
            user_card("VT-473", "Alicia Antonella", "VENDEDOR", "2023/08/20", "ATIVO"),
            user_card("VT-638", "Gabriel Santos", "VENDEDOR", "2023/05/16", "ATIVO"),
        ],
    )

    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Gerenciar Usuários", size=22, weight="bold", color=cor_texto_principal),
                        ft.FloatingActionButton(
                            icon=ft.Icons.ADD,
                            bgcolor="#1B4F9C",
                            mini=True,
                            on_click=lambda e: on_adicionar_usuario()
                        ),
                    ],
                ),
                ft.TextField(
                    hint_text="Buscar...",
                    prefix_icon=ft.Icons.SEARCH,
                    border_radius=15,
                    height=50,
                    bgcolor=cor_fundo_busca,
                    border_color=cor_borda_busca,
                    hint_style=ft.TextStyle(color=cor_texto_secundario),
                    content_padding=10,
                    color=cor_texto_principal
                ),
                lista_usuarios, 
            ],
        )
    )

    #---------------- NAVEGAÇÃO ----------------
    def trocar_aba(e):
        index = nav.selected_index
        if index == 0: on_home()
        elif index == 1: on_stock()
        elif index == 2: pass
        elif index == 3: on_perfil()

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=2,
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