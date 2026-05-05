import flet as ft

def perfil_page(page: ft.Page, on_home, on_stock, on_vendas, on_users, on_logout, on_config, on_theme_change):
    page.controls.clear()
    
    # --- RECUPERAÇÃO DE DADOS ---
    user_data = page.user_data
    if user_data:
        nome_usuario = user_data.get("nome_user") or user_data.get("nome") or "Usuário"
        perfil_usuario = user_data.get("perfil", "Nível")
        id_usuario = user_data.get("id_user") or user_data.get("id_use") or "000"
    else:
        nome_usuario = "Visitante"; perfil_usuario = "Sem Acesso"; id_usuario = "???"

    # --- LÓGICA DE CORES USANDO IF ---
    if page.theme_mode == ft.ThemeMode.DARK:
        cor_fundo_item = "#0A122A"
        cor_borda_item = "#1E2B4E"
        cor_texto_principal = ft.Colors.WHITE
        cor_texto_secundario = "#00bcd4"
        cor_barra = "#0b1445"
        cor_fundo_tela = "#050A18"
        icone_tema = ft.Icons.LIGHT_MODE
    else:
        cor_fundo_item = "#FFFFFF"
        cor_borda_item = "#D1D5DB"
        cor_texto_principal = ft.Colors.BLACK
        cor_texto_secundario = "#00707D"
        cor_barra = "#1A237E"
        cor_fundo_tela = "#F0F4FF"
        icone_tema = ft.Icons.DARK_MODE

    # --- COMPONENTES ---

    # Botão de Tema no AppBar (Ao clicar, ele executa o refresh do main.py)
    btn_tema = ft.IconButton(
        icon=icone_tema,
        icon_color="white",
        on_click=lambda _: on_theme_change() 
    )

    page.appbar = ft.AppBar(
        bgcolor=cor_barra,
        toolbar_height=70,
        title=ft.Text("Vende de Tudo", size=20, weight="bold", color="white"),
        center_title=True,
        actions=[btn_tema]
    )

    avatar = ft.Container(
        content=ft.Icon(ft.Icons.PERSON, size=80, color=cor_texto_secundario),
        width=140, height=140, border_radius=70,
        border=ft.border.all(3, cor_texto_secundario),
    )

    user_info = ft.Column(
        [
            ft.Text(nome_usuario, size=24, weight="bold", color=cor_texto_principal),
            ft.Text(perfil_usuario, size=14, color="#00b0ff"),
            ft.Container(
                content=ft.Text(f"ID: {id_usuario}", size=12, color="white"),
                bgcolor="#1e3a8a",
                padding=ft.padding.symmetric(horizontal=12, vertical=4),
                border_radius=20,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    def criar_item_menu(icon, label, color="#2196f3", on_click=None):
        return ft.Container(
            padding=15, border_radius=15,
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

    # ITENS DE MENU
    btn_cloud = criar_item_menu(ft.Icons.CLOUD_OUTLINED, "Sincronização Cloud")
    btn_config = criar_item_menu(ft.Icons.SETTINGS_OUTLINED, "Configurações do App", on_click=lambda _: on_config())

    botao_sair = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.LOGOUT, color="white"), ft.Text("Sair da Conta", color="white", weight="bold")],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor="#7f0000", padding=15, border_radius=15,
        on_click=lambda _: on_logout(), col=12
    )

    # Conteúdo envolto em um Container com cor de fundo dinâmica
    layout_principal = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=20),
                avatar,
                ft.Container(height=10),
                user_info,
                ft.Container(height=40),
                ft.ResponsiveRow([btn_cloud, btn_config, ft.Container(height=10, col=12), botao_sair], spacing=15),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=25,
        expand=True,
        bgcolor=cor_fundo_tela
    )

    page.add(layout_principal)

    # --- BARRA DE NAVEGAÇÃO ---
    nav = ft.NavigationBar(
        bgcolor=cor_barra,
        selected_index=4,
        on_change=lambda e: [on_home() if e.control.selected_index==0 else 
                             on_vendas() if e.control.selected_index==1 else
                             on_stock() if e.control.selected_index==2 else
                             on_users() if e.control.selected_index==3 else None],
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
            ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
        ]
    )
    
    page.navigation_bar = ft.Container(
        content=nav, margin=ft.margin.only(left=25, right=25, bottom=30), 
        border_radius=40, clip_behavior="antiAlias"
    )
    
    page.update()