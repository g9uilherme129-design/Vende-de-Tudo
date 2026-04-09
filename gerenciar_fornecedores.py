import flet as ft
from database import buscar_fornecedores

def tela_fornecedores(page: ft.Page, on_home, on_vendas, on_stock, on_usuarios, on_adicionar_fornecedor):
    page.controls.clear()
    page.padding = 20

    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_container_bg = "#0b1445" if is_dark else "#F0F2F8"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = ft.Colors.GREY_500
    cor_fundo_busca = "#0d1626" if is_dark else "#FFFFFF"

    # --- LISTA DE FORNECEDORES ---
    lista_forn_ui = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=10)

    def criar_card_fornecedor(f):
        return ft.Container(
            bgcolor=cor_container_bg,
            border_radius=15,
            padding=20,
            content=ft.Column([
                # Linha do Cabeçalho (Nome e ID)
                ft.Row([
                    ft.Icon(ft.Icons.BUSINESS, color=ft.Colors.TEAL_400),
                    ft.Text(f["nome_fornecedor"].upper(), size=16, weight="bold", color=cor_texto_principal, expand=True),
                    ft.Text(f["id_fornecedor"], size=10, color=cor_texto_secundario),
                ], alignment="spaceBetween"),
                
                ft.Divider(height=1, color=ft.Colors.WHITE10),

                # Dados de Contato
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

                # Endereço Resumido
                ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=14, color=cor_texto_secundario),
                    ft.Text(
                        f"{f['endereco_logradouro']}, {f['endereco_numero']} - {f['bairro']}, {f['cidade']}/{f['estado']}",
                        size=12, color=cor_texto_secundario, expand=True
                    ),
                ]),

                ft.Row([
                   # O .get('coluna', 'Valor Padrão') evita que o programa feche se o nome estiver errado
ft.Text(f"✉ {f.get('email', f.get('email_forn', 'Sem e-mail'))}", size=12, color=ft.Colors.BLUE_400), 
                ], alignment="end")
            ], spacing=10)
        )

    # --- LÓGICA DE BUSCA ---
    def filtrar(e):
        texto = busca_field.value.lower()
        dados = buscar_fornecedores()
        
        lista_forn_ui.controls.clear()
        for f in dados:
            if texto in f["nome_fornecedor"].lower() or texto in f["CNPJ"]:
                lista_forn_ui.controls.append(criar_card_fornecedor(f))
        page.update()

    # --- COMPONENTES DA INTERFACE ---
    busca_field = ft.TextField(
        hint_text="Buscar por nome ou CNPJ...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        bgcolor=cor_fundo_busca,
        border_radius=15,
        on_change=filtrar
    )

    # Barra Superior
    page.appbar = ft.AppBar(
        bgcolor="#0b1445",
        title=ft.Text("Gestão de Fornecedores", color="white", weight="bold"),
        center_title=True,
    )

    # Montagem da Página
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
            ft.Row([busca_field]),
            lista_forn_ui
        ])
    )

    # Barra de Navegação (Padrão do seu App)
    def trocar_aba(e):
        idx = e.control.selected_index
        if idx == 0: on_home()
        elif idx == 1: on_vendas()
        elif idx == 2: on_stock()
        elif idx == 3: on_usuarios()

    nav = ft.NavigationBar(
        bgcolor="#0b1445", selected_index=2, on_change=trocar_aba, # Coloquei index 2 assumindo que fica perto de estoque
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT, label="Vendas"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP, label="Usuários"),
        ]
    )
    page.navigation_bar = ft.Container(content=nav, margin=ft.margin.only(left=25, right=25, bottom=30), border_radius=40, clip_behavior="antiAlias")

    # Carregamento Inicial
    filtrar(None)