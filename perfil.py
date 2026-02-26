import flet as ft


def perfil_page(page: ft.Page, on_home, on_stock, on_users, on_logout):

    page.controls.clear()
    page.bgcolor = "#000000"
    page.appbar = None

    # -------------------------
    # FUNÇÃO SAIR
    # -------------------------
    def sair_app(e):
        print("Logout clicado")
        on_logout()

    # -------------------------
    # HEADER
    # -------------------------
    titulo = ft.Text(
        "Perfil",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    # -------------------------
    # AVATAR
    # -------------------------
    avatar = ft.Container(
        content=ft.Icon(
            ft.Icons.PERSON,
            size=80,
            color="#00bcd4",
        ),
        width=150,
        height=150,
        border_radius=75,
        border=ft.border.all(3, "#00bcd4"),
    )

    # -------------------------
    # INFORMAÇÕES USUÁRIO
    # -------------------------
    nome = ft.Text(
        "João Silva",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    cargo = ft.Text(
        "Administrador",
        size=14,
        color="#00b0ff",
    )

    codigo = ft.Text(
        "VT-001",
        size=12,
        color="#2979ff",
        weight=ft.FontWeight.BOLD,
    )

    # -------------------------
    # BOTÃO CLOUD
    # -------------------------
    botao_cloud = ft.Container(
        padding=15,
        border_radius=20,
        bgcolor="#0b1445",
        border=ft.border.all(1, "#1e3a8a"),
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CLOUD_OUTLINED, color="#2196f3"),
                ft.Text("Sincronização Cloud", color=ft.Colors.WHITE),
                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.WHITE54),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        on_click=lambda e: print("Sincronização Cloud clicado"),
    )

    # -------------------------
    # BOTÃO SAIR
    # -------------------------
    botao_sair = ft.Container(
        padding=15,
        border_radius=20,
        bgcolor="#7f0000",
        content=ft.Row(
            [
                ft.Text(
                    "Sair",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                )
            ],
        ),
        on_click=sair_app,
    )

    # -------------------------
    # CONTEÚDO PRINCIPAL
    # -------------------------
    conteudo = ft.Column(
        [
            titulo,
            ft.Container(height=30),
            avatar,
            ft.Container(height=15),
            nome,
            cargo,
            codigo,
            ft.Container(height=40),
            botao_cloud,
            ft.Container(height=20),
            botao_sair,
        ],
        alignment=ft.MainAxisAlignment.CENTER,          # Centraliza verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    page.add(
        ft.Container(
            content=conteudo,
            padding=20,
            expand=True,
        )
    )

    # -------------------------
    # NAVIGATION BAR
    # -------------------------
    def trocar_aba(e):
        index = nav.selected_index

        if index == 0:
            on_home()
        elif index == 1:
            on_stock()
        elif index == 2:
            on_users()
        elif index == 3:
            pass  # já está no perfil

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=3,
        on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.INVENTORY_2_OUTLINED,
                selected_icon=ft.Icons.INVENTORY_2,
                label="",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.GROUP_OUTLINED,
                selected_icon=ft.Icons.GROUP,
                label="",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON_OUTLINE,
                selected_icon=ft.Icons.PERSON,
                label="",
            ),
        ],
    )

    page.navigation_bar = ft.Container(
        content=nav,
        margin=ft.margin.only(left=25, right=25, bottom=30),
        border_radius=40,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
        ),
    )

    page.update()