import flet as ft

def usuarios(page: ft.Page, on_home, on_stock, on_perfil, on_logout, on_adicionar_usuario):

    page.title = "Gerenciar Usuários"
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
            margin=ft.margin.only(bottom=15),
            content=ft.Column(
                spacing=8,
                        alignment="spaceBetween",
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(codigo, size=12, color="grey"),
                            ft.Text(f"ADMISSÃO: {admissao}", size=12, color="grey"),
                        ],
                    ),
                    ft.Row(
                        alignment="spaceBetween",
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(nome, size=16, weight="bold"),
                                    ft.Text(cargo, size=12, color="grey"),
                                ],
                            ),
                            status_badge(status),
                        ],
                    ),
                    ft.Container(
                        visible=status == "INATIVO",
                        bgcolor="#991f23",
                        border_radius=10,
                        padding=10,
                        content=ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text(
                                    "DETALHES DA DESATIVAÇÃO",
                                    size=12,
                                    color="#f60007",
                                    weight="bold",
                                ),
                                ft.Text(
                                    detalhes if detalhes else "",
                                    size=12,
                                    italic=True,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        visible=status == "ATIVO",
                        content=ft.ElevatedButton(
                            "Desativar Acesso",
                            icon=ft.Icons.BLOCK,
                            style=ft.ButtonStyle(
                                bgcolor="#002072",
                                shape=ft.RoundedRectangleBorder(radius=20),
                            ),
                        ),
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
                    border_radius=20,
                    bgcolor="#162447",
                    border_color="transparent",
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