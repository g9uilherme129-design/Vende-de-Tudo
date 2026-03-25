import flet as ft

def usuarios(page: ft.Page, on_home, on_stock, on_perfil, on_logout, on_adicionar_usuario, on_editar_usuario):

    page.bgcolor = "black"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.controls.clear()

    def sair_app(e):
        on_logout()


    page.appbar = ft.AppBar(
        bgcolor="#0b1445",
        toolbar_height=70,

        leading=ft.Container(width=40),

        title=ft.Row(
            [
                ft.Text(
                    "Vende de Tudo",
                    size=18 if page.width < 600 else 22,
                    weight=ft.FontWeight.BOLD,
                    color="white"
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True
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
            ),
            bgcolor="#00b40d" if status == "ATIVO" else "#ff0008",
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            border_radius=20,
        )
    def user_card(codigo, nome, cargo, admissao, status, detalhes=None):

        return ft.Container(
            bgcolor="#0b1445",
            border_radius=15,
            padding=15,
            margin=ft.margin.only(bottom=10),

            content=ft.Column(
                spacing=10,
                controls=[

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(codigo, size=12, color="grey"),
                            ft.Text(f"ADMISSÃO: {admissao}", size=12, color="grey"),
                        ],
                    ),
                    # Linha de Informações Principais
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(nome, size=18, weight="bold", color="white"),
                                    ft.Text(cargo, size=13, color="bluegrey200"),
                                ],
                            ),
                            status_badge(status),
                        ],
                    ),
                    # Detalhes de Desativação (se houver)
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
                                ft.Text(detalhes if detalhes else "Não especificado", size=12, color="white", italic=True),
                            ],
                        ),
                    ),
                    # Ações
                    ft.Divider(height=1, color="white10"),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10,
                        controls=[
                            ft.TextButton(
                                "Editar Usuário",
                                icon=ft.Icons.EDIT_NOTE,
                                style=ft.ButtonStyle(color="white"),
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
                                on_click=lambda e: print(f"Desativando {codigo}") # Adicione sua lógica aqui
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
                    alignment="spaceBetween",
                    controls=[
                        ft.Text("Gerenciar Usuários", size=22, weight="bold"),
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
                    bgcolor="#0d1626",
                    border_color="#1e293b",
                    hint_style=ft.TextStyle(color="grey"),
                    content_padding=10,
                    color=ft.Colors.WHITE
                ),
                lista_usuarios, 
            ],
        )
    )

    #---------------- NAVEGAÇÃO ----------------
    def trocar_aba(e):
        index = nav.selected_index

        if index == 0:
            on_home()  # Chama home

        elif index == 1:
            on_stock()  # chama estoque

        elif index == 2:
            pass # Ja esta em usuarios

        elif index == 3:
            on_perfil()

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=2,
        on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Inicial"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.INVENTORY_2_OUTLINED,
                selected_icon=ft.Icons.INVENTORY_2,
                label="Estoque"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.GROUP_OUTLINED,
                selected_icon=ft.Icons.GROUP,
                label="Usuários"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON_OUTLINE,
                selected_icon=ft.Icons.PERSON,
                label="Perfil"
            ),
        ]
    )

    page.navigation_bar = ft.Container(
        content=nav,
        margin=ft.margin.only(left=25, right=25, bottom=30),
        border_radius=40, 
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK)
        )
    )

    page.update()