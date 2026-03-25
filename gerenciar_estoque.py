# Importa a biblioteca Flet
import flet as ft


def estoque(page: ft.Page, on_home, on_users, on_perfil, on_adicionar_produto, on_editar_produto, on_logout):

    page.controls.clear()
    page.appbar = None
    page.bgcolor = "#050505"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START

    # -----------------
    # LOGOUT
    # -----------------

    def sair_app(e):
        on_logout()

    # -----------------
    # APPBAR
    # -----------------

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

    # -----------------
    # CARD PRODUTO
    # -----------------

    def card_produto(cod, nome, preco, marca, validade, quantidade):

        return ft.Container(
            padding=15,
            border_radius=15,
            bgcolor="#0b1445",
           
            content=ft.Column(
                spacing=10,
                controls=[

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[

                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(cod, size=10, color="grey"),
                                    ft.Text(
                                        nome,
                                        size=16,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                ],
                            ),

                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                controls=[
                                    ft.Text(
                                        f"R$ {preco}",
                                        weight=ft.FontWeight.BOLD,
                                        size=16
                                    ),
                                    ft.Text(
                                        marca,
                                        size=10,
                                        color="grey"
                                    ),
                                ],
                            ),
                        ],
                    ),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[

                            ft.Text(
                                f"Val - {validade}",
                                size=10,
                                color="grey"
                            ),

                            ft.Container(
                                padding=ft.padding.symmetric(
                                    horizontal=10,
                                    vertical=4
                                ),
                                bgcolor="#00b40d",
                                border_radius=20,

                                content=ft.Text(
                                    f"{quantidade} UN",
                                    size=11,
                                    weight=ft.FontWeight.BOLD
                                ),
                            ),
                        ],
                    ),

                    ft.Container(
                        width=60,  
                        height=30,
                        bgcolor="#002072",
                        border_radius=20,
                        padding=5,
                        content=ft.Text(
                            "Editar",
                            weight=ft.FontWeight.BOLD,
                        ),
                        on_click=lambda e: on_editar_produto()
                    ),
                ],
            ),
        )

    # -----------------
    # HEADER
    # -----------------

    header = ft.Row(
        controls=[

            ft.Text(
                "Consultar Estoque",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),

            ft.Container(
                content=ft.Image(
                    src="imgs/addicon.png",
                    width=35,
                    height=35,
                ),
                on_click=lambda e: on_adicionar_produto(),
            ),

        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # -----------------
    # BUSCA
    # -----------------

    search_field = ft.TextField(
        hint_text="Buscar...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=15,
        height=50,
        bgcolor="#0d1626",
        border_color="#1e293b",
        hint_style=ft.TextStyle(color="grey"),
        content_padding=10,
        color=ft.Colors.WHITE
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

    # -----------------
    # CONTEÚDO
    # -----------------

    conteudo = ft.Column(
        expand=True,
        spacing=15,
        controls=[

            header,

            search_field,

            lista_produtos
        ]
    )

    page.add(conteudo)

    # -------------------------
    # NAVIGATION BAR
    # -------------------------

    def trocar_aba(e):

        index = nav.selected_index

        if index == 0:
            on_home()

        elif index == 1:
            pass

        elif index == 2:
            on_users()

        elif index == 3:
            on_perfil()

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=1,
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