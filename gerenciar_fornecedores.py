import flet as ft
from database import buscar_fornecedores, alterar_status_fornecedor_db 

def tela_fornecedores(page: ft.Page, on_home, on_vendas, on_stock, on_usuarios, on_adicionar_fornecedor, on_editar_fornecedor, on_perfil):
    page.controls.clear()
    page.padding = 20

    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_container_bg = "#0b1445" if is_dark else "#F0F2F8"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = ft.Colors.GREY_500
    cor_fundo_busca = "#0d1626" if is_dark else "#FFFFFF"

    # --- VARIÁVEL GLOBAL DA TELA ---
    fornecedores_base = []
    lista_forn_ui = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=15)

    # --- CARD FORNECEDOR ---
    def criar_card_fornecedor(f):
        status_db = f.get("status_fornecedor")
        status = "Ativo" if status_db == 1 or status_db == "1" else "Inativo"
        
        cor_status = "#00b40d" if status == "Ativo" else "#ff4444"
        
        return ft.Container(
            bgcolor=cor_container_bg,
            border_radius=15,
            padding=20,
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.BUSINESS, color=ft.Colors.TEAL_400),
                    ft.Text(f["nome_fornecedor"].upper(), size=16, weight="bold", color=cor_texto_principal, expand=True),
                    ft.Container(
                        content=ft.Text(status, size=10, weight="bold", color="white"),
                        bgcolor=cor_status,
                        padding=ft.padding.symmetric(horizontal=10, vertical=2),
                        border_radius=10
                    ),
                    ft.Text(f"ID: {f['id_fornecedor']}", size=10, color=cor_texto_secundario),
                ], alignment="spaceBetween"),
                
                ft.Divider(height=1, color=ft.Colors.WHITE10),

                ft.Row([
                    ft.Column([
                        ft.Text("CNPJ", size=10, color=cor_texto_secundario, weight="bold"),
                        ft.Text(f["CNPJ"], size=13, color=cor_texto_principal),
                    ], expand=1),
                    ft.Column([
                        ft.Text("TELEFONE", size=10, color=cor_texto_secundario, weight="bold"),
                        ft.Text(f["telefone"], size=13, color=cor_texto_principal),
                    ], expand=1),
                ]),

                ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=14, color=cor_texto_secundario),
                    ft.Text(
                        f"{f['endereco_logradouro']}, {f['endereco_numero']} - {f['bairro']}, {f['cidade']}/{f['estado']}",
                        size=11, color=cor_texto_secundario, expand=True
                    ),
                ]),

                ft.Row([
                    ft.Text(f"✉ {f.get('email_forn', 'Sem e-mail')}", size=12, color=ft.Colors.BLUE_400, expand=True),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            icon_color=ft.Colors.BLUE_400,
                            tooltip="Editar Fornecedor",
                            on_click=lambda _: on_editar_fornecedor(f["id_fornecedor"])
                        ),
                        ft.IconButton(
                            icon=ft.Icons.POWER_SETTINGS_NEW,
                            icon_color=ft.Colors.RED_400 if status == "Ativo" else ft.Colors.GREEN_400,
                            tooltip="Ativar/Desativar",
                            on_click=lambda _: alternar_status_fornecedor(f["id_fornecedor"], status)
                        ),
                    ], spacing=0)
                ], alignment="spaceBetween")
            ], spacing=10)
        )

    # --- LÓGICA ---
    def filtrar(e=None):
        texto = busca_field.value.lower()
        criterio = btn_filtro.data 
        
        filtrados = [
            f for f in fornecedores_base
            if (texto in f["nome_fornecedor"].lower() or texto in f["CNPJ"])
        ]

        if criterio != "todos":
            filtrados = [f for f in filtrados if f.get("status", "Ativo") == criterio]

        lista_forn_ui.controls.clear()
        for f in filtrados:
            lista_forn_ui.controls.append(criar_card_fornecedor(f))
        page.update()

    def mudar_filtro(status_selecionado):
        btn_filtro.data = status_selecionado
        filtrar()

    def alternar_status_fornecedor(id_forn, status_atual):
        novo = "Inativo" if status_atual == "Ativo" else "Ativo"
        resultado = alterar_status_fornecedor_db(id_forn, novo)
        
        if resultado == True:
            carregar_dados() # Sucesso
        elif isinstance(resultado, str):
            # Aqui você exibe um SnackBar ou Banner com a mensagem de erro
            page.snack_bar = ft.SnackBar(ft.Text(resultado), bgcolor="red")
            page.snack_bar.open = True
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
        bgcolor=cor_fundo_busca,
        border_radius=15,
        on_change=filtrar
    )

    btn_filtro = ft.PopupMenuButton(
        icon=ft.Icons.FILTER_ALT_OUTLINED,
        items=[
            ft.PopupMenuItem(content=ft.Text("Todos"), on_click=lambda _: mudar_filtro("todos")),
            ft.PopupMenuItem(content=ft.Text("Ativos"), on_click=lambda _: mudar_filtro("Ativo")),
            ft.PopupMenuItem(content=ft.Text("Inativos"), on_click=lambda _: mudar_filtro("Inativo")),
        ]
    )
    btn_filtro.data = "todos"

    # --- APPBAR COM BOTÃO VOLTAR ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_NEW, 
            icon_color="white", 
            on_click=lambda _: on_stock() 
        ),
        bgcolor="#0b1445",
        title=ft.Text("Gestão de Fornecedores", color="white", weight="bold"),
        center_title=True,
    )

    page.add(
        ft.Column(expand=True, controls=[
            ft.Row([
                ft.Text("Meus Fornecedores", size=24, weight="bold", color=cor_texto_principal),
                ft.FloatingActionButton(
                    icon=ft.Icons.ADD, 
                    bgcolor="#1B4F9C", 
                    mini=True, 
                    on_click=lambda _: on_adicionar_fornecedor()
                )
            ], alignment="spaceBetween"),
            ft.Row([busca_field, btn_filtro]),
            lista_forn_ui
        ])
    )

    def trocar_aba(e):
        idx = e.control.selected_index
        if idx == 0: on_home()
        elif idx == 1: on_vendas()
        elif idx == 2: pass 
        elif idx == 3: on_usuarios()
        elif idx == 4: on_perfil()

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=2,
        on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
            ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
        ]
    )
    
    page.navigation_bar = ft.Container(
        content=nav, margin=ft.margin.only(left=25, right=25, bottom=30), 
        border_radius=40, clip_behavior=ft.ClipBehavior.ANTI_ALIAS
    )

    carregar_dados()