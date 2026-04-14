import flet as ft

def perfil_page(page: ft.Page, on_home, on_stock, on_vendas, on_users, on_logout, on_config):
    page.controls.clear()
    
    # --- RECUPERA DADOS DO USUÁRIO LOGADO ---
    # Agora lendo de page.user_data, que é onde você salvou no main.py
    user_data = page.user_data
    
    if user_data:
        # Tenta pegar 'nome_user' ou 'nome' (depende de como o banco retorna)
        nome_usuario = user_data.get("nome_user") or user_data.get("nome") or "Usuário"
        perfil_usuario = user_data.get("perfil", "Nível")
        # Tenta pegar 'id_user' ou 'id_use'
        id_usuario = user_data.get("id_user") or user_data.get("id_use") or "000"
    else:
        nome_usuario = "Visitante"
        perfil_usuario = "Sem Acesso"
        id_usuario = "???"

    # Lógica de cores adaptáveis
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_item = "#0A122A" if is_dark else "#F0F2F8"
    cor_borda_item = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = "#00bcd4" if is_dark else "#00707D"

    page.appbar = ft.AppBar(
        bgcolor="#0b1445",
        toolbar_height=70,
        title=ft.Text("Vende de Tudo", size=20, weight="bold", color="white"),
        center_title=True,
    )

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

    # --- INFO PRINCIPAL (AGORA DINÂMICA) ---
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

    # --- ITENS DE MENU ---
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

    btn_cloud = criar_item_menu(ft.Icons.CLOUD_OUTLINED, "Sincronização Cloud")
    btn_config = criar_item_menu(ft.Icons.SETTINGS_OUTLINED, "Configurações do App", on_click=lambda _: on_config())

    botao_sair = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.LOGOUT, color="white"), ft.Text("Sair da Conta", color="white", weight="bold", size=16)],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor="#7f0000",
        padding=15,
        border_radius=15,
        on_click=lambda _: on_logout(),
        col=12
    )

    layout_acoes = ft.ResponsiveRow(
        controls=[btn_cloud, btn_config, ft.Container(height=10, col=12), botao_sair],
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
        ft.Container(content=conteudo, padding=25, expand=True)
    )

    # --- BARRA DE NAVEGAÇÃO ---
    def trocar_aba(e):
        idx = e.control.selected_index
        if idx == 0: on_home()
        elif idx == 1: on_vendas()
        elif idx == 2: on_stock()
        elif idx == 3: on_users()
        elif idx == 4: pass

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=4,
        on_change=trocar_aba,  
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
            ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
        ]
    )
    page.navigation_bar = ft.Container(
        content=nav, 
        margin=ft.margin.only(left=25, right=25, bottom=30), 
        border_radius=40, 
        clip_behavior="antiAlias"
    )
    
    page.update()