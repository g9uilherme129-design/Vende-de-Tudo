import flet as ft
from database import buscar_fornecedores, alterar_status_fornecedor_db 

def tela_fornecedores(page: ft.Page, on_home, on_vendas, on_stock, on_usuarios, on_adicionar_fornecedor, on_editar_fornecedor, on_perfil):
    page.controls.clear()
    page.padding = 0

    # --- PADRONIZAÇÃO DE CORES (IDÊNTICO AO SEU PERFIL) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#11259c" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_input = "#0A122A" if is_dark else "#F5F7FB"
    cor_secundaria =  "#1679f2" if is_dark else "#DA7D7D"
    cor_bar =  "#1679f2" if is_dark else "#BA7272"

    fornecedores_base = []
    lista_forn_ui = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=15)

    # --- CARD FORNECEDOR ---
    def criar_card_fornecedor(f):
        status_db = f.get("status_fornecedor")
        esta_ativo = status_db == 1 or status_db == "1"
        status_txt = "Ativo" if esta_ativo else "Inativo"
        cor_status = "#00b40d" if esta_ativo else "#ff4444"
        
        return ft.Container(
            bgcolor=cor_fundo_card,
            border_radius=15,
            padding=20,
            border=ft.border.all(1, cor_borda),
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.BUSINESS, color=cor_texto_s),
                    ft.Text(f["nome_fornecedor"].upper(), size=16, weight="bold", color=cor_texto_p, expand=True),
                    ft.Container(
                        content=ft.Text(status_txt.upper(), size=10, weight="bold", color="white"),
                        bgcolor=cor_status,
                        padding=ft.padding.symmetric(horizontal=10, vertical=2),
                        border_radius=10
                    ),
                    ft.Text(f"ID: {f['id_fornecedor']}", size=10, color=cor_secundaria),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Divider(height=1, color=ft.Colors.WHITE10),

                ft.Row([
                    ft.Column([
                        ft.Text("CNPJ", size=10, color=cor_secundaria, weight="bold"),
                        ft.Text(f["CNPJ"], size=13, color=cor_texto_p),
                    ], expand=1),
                    ft.Column([
                        ft.Text("TELEFONE", size=10, color=cor_secundaria, weight="bold"),
                        ft.Text(f["telefone"], size=13, color=cor_texto_p),
                    ], expand=1),
                ]),

                ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=14, color=cor_secundaria),
                    ft.Text(
                        f"{f['endereco_logradouro']}, {f['endereco_numero']} - {f['bairro']}, {f['cidade']}/{f['estado']}",
                        size=11, color=cor_secundaria, expand=True
                    ),
                ]),

                ft.Row([
                    ft.Text(f"✉ {f.get('email_forn', 'Sem e-mail')}", size=12, color=cor_texto_s, expand=True),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            icon_color=cor_texto_s,
                            on_click=lambda _: on_editar_fornecedor(f["id_fornecedor"])
                        ),
                        ft.IconButton(
                            icon=ft.Icons.POWER_SETTINGS_NEW,
                            icon_color=ft.Colors.RED_400 if esta_ativo else ft.Colors.GREEN_400,
                            on_click=lambda _: alternar_status_fornecedor(f["id_fornecedor"], status_txt)
                        ),
                    ], spacing=0)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], spacing=10)
        )

    # --- LÓGICA ---
    def filtrar(e=None):
        texto = busca_field.value.lower() if busca_field.value else ""
        criterio = btn_filtro.data 
        
        filtrados = [
            f for f in fornecedores_base
            if (texto in f["nome_fornecedor"].lower() or texto in f["CNPJ"])
        ]

        if criterio != "todos":
            filtrados = [f for f in filtrados if ("Ativo" if f.get("status_fornecedor") == 1 else "Inativo") == criterio]

        lista_forn_ui.controls.clear()
        for f in filtrados:
            lista_forn_ui.controls.append(criar_card_fornecedor(f))
        page.update()

    def mudar_filtro(status_selecionado):
        btn_filtro.data = status_selecionado
        filtrar()

    def alternar_status_fornecedor(id_forn, status_atual):
        novo = "Inativo" if status_atual == "Ativo" else "Ativo"
        if alterar_status_fornecedor_db(id_forn, novo):
            carregar_dados()
        page.update()

    def carregar_dados():
        nonlocal fornecedores_base
        fornecedores_base = buscar_fornecedores()
        filtrar()

    # --- COMPONENTES ---
    busca_field = ft.TextField(
        hint_text="Buscar por nome ou CNPJ...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        bgcolor=cor_input,
        border_radius=15,
        border_color=cor_borda,
        text_style=ft.TextStyle(color=cor_texto_p),
        on_change=filtrar
    )

    btn_filtro = ft.PopupMenuButton(
        icon=ft.Icons.FILTER_ALT_OUTLINED,
        icon_color=cor_texto_p,
        items=[
            ft.PopupMenuItem(content=ft.Text("Todos"), on_click=lambda _: mudar_filtro("todos")),
            ft.PopupMenuItem(content=ft.Text("Ativos"), on_click=lambda _: mudar_filtro("Ativo")),
            ft.PopupMenuItem(content=ft.Text("Inativos"), on_click=lambda _: mudar_filtro("Inativo")),
        ]
    )
    btn_filtro.data = "todos"

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_stock()),
        bgcolor=cor_barra,
        title=ft.Text("Gestão de Fornecedores", color="white", weight="bold"),
        center_title=True,
    )

    def trocar_aba(e):
        idx = e.control.selected_index
        if idx == 0: on_home()
        elif idx == 1: on_vendas()
        elif idx == 2: pass 
        elif idx == 3: on_usuarios()
        elif idx == 4: on_perfil()

    page.navigation_bar = ft.Container(
        content=ft.NavigationBar(
            bgcolor=cor_barra, selected_index=2, on_change=trocar_aba,
            indicator_color=cor_bar,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
                ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"),
                ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2, label="Estoque"),
                ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Usuários"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
            ]
        ),
        margin=ft.margin.only(left=25, right=25, bottom=20),
        border_radius=40, clip_behavior=ft.ClipBehavior.ANTI_ALIAS
    )

    page.add(
        ft.Container(
            expand=True, bgcolor=cor_fundo_tela, padding=20,
            content=ft.Column(expand=True, controls=[
                ft.Row([
                    ft.Text("Meus Fornecedores", size=24, weight="bold", color=cor_texto_p),
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, bgcolor=cor_texto_s, tooltip="Novo Fornecedor", mini=True, 
                        on_click=lambda _: on_adicionar_fornecedor()
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([busca_field, btn_filtro]),
                lista_forn_ui
            ])
        )
    )

    carregar_dados()