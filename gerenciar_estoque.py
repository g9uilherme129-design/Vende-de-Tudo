# Importa a biblioteca Flet
import flet as ft

def estoque(page: ft.Page, on_home, on_users, on_perfil, on_adicionar_produto, on_editar_produto, on_logout):

    page.controls.clear()
    page.appbar = None
    page.bgcolor = ft.Colors.BLACK_45
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START

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

            ft.Container(
                content=ft.Image(
                    src="imgs/editar_icon.png",
                    width=35,
                    height=35,
                ),
                on_click=lambda e: on_editar_produto(),
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # -----------------
    # CAMPO DE BUSCA 
    # -----------------

    search_field = ft.TextField(
        hint_text="Buscar...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=15,
        width=400,
        height=50,
        bgcolor="#0d1626",
        border_color="#1e293b",
        hint_style=ft.TextStyle(color="grey"),
        content_padding=10,
        color=ft.Colors.WHITE
    )

    conteudo = ft.Column(
        controls=[
            header,
            ft.Container(height=20),
            ft.Text(
                "PESQUISAR PRODUTO",
                size=12,
                color="grey",
                weight=ft.FontWeight.BOLD
            ),
            search_field
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START
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