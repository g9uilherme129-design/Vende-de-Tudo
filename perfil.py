import flet as ft

def perfil_page(page: ft.Page, on_home, on_stock, on_users, on_logout, on_config):
    page.controls.clear()
    
    # Lógica de cores adaptáveis
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_item = "#0A122A" if is_dark else "#F0F2F8"
    cor_borda_item = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = "#00bcd4" if is_dark else "#00707D"

    # Reset da AppBar para garantir o padrão
    page.appbar = ft.AppBar(
        bgcolor="#0b1445",
        toolbar_height=70,
        title=ft.Text(
            "Vende de Tudo",
            size=20,
            weight=ft.FontWeight.BOLD,
            color="white"
        ),
        center_title=True,
    )

    # -------------------------
    # AVATAR E INFO PRINCIPAL
    # -------------------------
    avatar = ft.Container(
        content=ft.Icon(
            ft.Icons.PERSON,
            size=80,
            color=cor_texto_secundario,
        ),
        width=140,
        height=140,
        border_radius=70,
        border=ft.border.all(3, cor_texto_secundario),
    )

    user_info = ft.Column(
        [
            ft.Text("João Silva", size=24, weight="bold", color=cor_texto_principal),
            ft.Text("Administrador", size=14, color="#00b0ff"),
            ft.Container(
                content=ft.Text("ID: VT-001", size=12, color="white"),
                bgcolor="#1e3a8a",
                padding=ft.padding.symmetric(horizontal=12, vertical=4),
                border_radius=20,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    # -------------------------
    # BOTÕES DE AÇÃO
    # -------------------------
    def criar_item_menu(icon, label, color="#2196f3", on_click=None):
        return ft.Container(
            padding=15,
            border_radius=15,
            bgcolor=cor_fundo_item,
            border=ft.border.all(1, cor_borda_item),
            content=ft.Row(
                [
                    ft.Icon(icon, color=color),
                    ft.Text(label, color=cor_texto_principal, weight="w500", expand=True),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.with_opacity(0.3, cor_texto_principal)),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_click=on_click,
            col=12 
        )

    btn_cloud = criar_item_menu(
        ft.Icons.CLOUD_OUTLINED, 
        "Sincronização Cloud", 
        on_click=lambda _: print("Sync clicado")
    )

    btn_config = criar_item_menu(
        ft.Icons.SETTINGS_OUTLINED, 
        "Configurações do App", 
        on_click=lambda _: on_config() # <-- Agora ele abre a tela de config!
    )
    

    # Botão Sair
    botao_sair = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LOGOUT, color="white"),
                ft.Text("Sair da Conta", color="white", weight="bold", size=16),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor="#7f0000",
        padding=15,
        border_radius=15,
        on_click=lambda _: on_logout(),
        col=12
    )

    layout_acoes = ft.ResponsiveRow(
        controls=[
            btn_cloud,
            btn_config,
            ft.Container(height=10, col=12),
            botao_sair,
        ],
        spacing=15,
    )

    conteudo = ft.Column(
        [
            ft.Container(height=20),
            avatar,
            ft.Container(height=10),
            user_info,
            ft.Container(height=40),
            layout_acoes,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )

    page.add(
        ft.Container(
            content=conteudo,
            padding=25,
            expand=True,
        )
    )

    # -------------------------
    # NAVIGATION BAR
    # -------------------------
    def trocar_aba(e):
        indices = {0: on_home, 1: on_stock, 2: on_users, 3: None}
        if indices[nav.selected_index]:
            indices[nav.selected_index]()

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=3,
        on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, selected_icon=ft.Icons.INVENTORY_2, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, selected_icon=ft.Icons.GROUP, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Perfil"),
        ],
    )

    page.navigation_bar = ft.Container(
        content=nav,
        margin=ft.margin.only(left=20, right=20, bottom=20),
        border_radius=30,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )
    
    page.update()