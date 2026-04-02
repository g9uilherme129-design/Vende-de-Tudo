import flet as ft
import flet_charts as fch
from database import buscar_dados_home  # Certifique-se que o arquivo database.py existe

def home_page(page: ft.Page, on_logout, on_stock, on_users, on_perfil):

    # --- BUSCA DE DADOS REAIS DO MYSQL ---
    try:
        dados = buscar_dados_home()
    except Exception as ex:
        print(f"Erro ao conectar no banco: {ex}")
        # Dados de backup caso o banco esteja offline
        dados = {
            "receita": 0.0, 
            "ranking": [{"nome_user": "Erro Banco", "qtd_vendas": 0, "valor_total": 0}], 
            "vendas_semanais": []
        }

    def sair_app(e):
        on_logout()

    page.controls.clear()
    
    # --- LÓGICA DE CORES ADAPTÁVEIS ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    page.bgcolor = "#000000" if is_dark else "#F0F4FF" 
    cor_fundo_container = "#0b1445" if is_dark else "#E1E8FA" 
    cor_texto_principal = ft.Colors.WHITE if is_dark else "#0b1445"
    cor_texto_secundario = ft.Colors.WHITE_70 if is_dark else ft.Colors.GREY_700
    cor_borda = "#1E2B4E" if is_dark else "#BCCAE3"

    # AppBar
    page.appbar = ft.AppBar(
        bgcolor="#0b1445",
        toolbar_height=70,
        title=ft.Text("Vende de Tudo", size=20, weight="bold", color="white"),
        center_title=True,
        actions=[ft.IconButton(icon=ft.Icons.EXIT_TO_APP, icon_color="white", on_click=sair_app)]
    )

    # --- CARD RECEITA DO MÊS (DINÂMICO) ---
    card_receita = ft.Container(
        padding=20,
        border_radius=20,
        bgcolor=cor_fundo_container,
        border=ft.border.all(1, cor_borda),
        content=ft.Column([
            ft.Text("RECEITA DO MÊS", size=12, color=cor_texto_secundario, weight="bold"),
            ft.Row([
                ft.Text(
                    f"R$ {dados['receita']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREEN_ACCENT_400 if is_dark else ft.Colors.GREEN_700,
                ),
                ft.Container(
                    content=ft.Text("LIVE", size=12, color=ft.Colors.GREEN, weight="bold"),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN),
                    padding=5,
                    border_radius=5
                ),
            ], alignment="spaceBetween"),
            ft.Text("Dados reais do banco de dados", size=10, color=cor_texto_secundario),
        ]),
    )

    # --- CARD VOLUME SEMANAL (GRÁFICO DINÂMICO) ---
    # Mapeia os dias (MySQL 1=Dom, 2=Seg...) para o gráfico (0 a 4)
    valores_grafico = [0, 0, 0, 0, 0]
    for v in dados['vendas_semanais']:
        index = v['dia'] - 2 # Ajusta Segunda(2) para index 0
        if 0 <= index <= 4:
            valores_grafico[index] = v['qtd']

    card_volume = ft.Container(
        bgcolor=cor_fundo_container,
        padding=20,
        border_radius=25,
        border=ft.border.all(1, cor_borda),
        content=ft.Column([
            ft.Text("VOLUME DE VENDAS (SEG-SEX)", size=12, color=cor_texto_secundario, weight="bold"),
            ft.Container(
                height=200,
                content=fch.BarChart(
                    interactive=True,
                    max_y=max(valores_grafico) + 5 if valores_grafico else 10,
                    bottom_axis=fch.ChartAxis(
                        labels=[
                            fch.ChartAxisLabel(value=0, label=ft.Text("S", color=cor_texto_principal)),
                            fch.ChartAxisLabel(value=1, label=ft.Text("T", color=cor_texto_principal)),
                            fch.ChartAxisLabel(value=2, label=ft.Text("Q", color=cor_texto_principal)),
                            fch.ChartAxisLabel(value=3, label=ft.Text("Q", color=cor_texto_principal)),
                            fch.ChartAxisLabel(value=4, label=ft.Text("S", color=cor_texto_principal)),
                        ]
                    ),
                    groups=[
                        fch.BarChartGroup(x=i, rods=[fch.BarChartRod(from_y=0, to_y=v, width=30, color="#4FC3F7", border_radius=5)]) 
                        for i, v in enumerate(valores_grafico)
                    ],
                )
            )
        ])
    )

    # --- RANKING VENDEDORES (LOOP DINÂMICO) ---
    def item_vendedor(nome, vendas, valor):
        return ft.Container(
            padding=12,
            border_radius=15,
            bgcolor=cor_fundo_container if is_dark else "#FFFFFF",
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, cor_texto_principal)),
            content=ft.Row([
                ft.Column([
                    ft.Text(nome, weight="bold", color=cor_texto_principal),
                    ft.Text(f"{vendas} VENDAS", size=11, color=cor_texto_secundario),
                ], spacing=2),
                ft.Text(f"R$ {valor:,.2f}", weight="bold", color=ft.Colors.GREEN),
            ], alignment="spaceBetween"),
        )

    coluna_ranking = ft.Column(spacing=10)
    for v in dados['ranking']:
        coluna_ranking.controls.append(
            item_vendedor(v['nome_user'], v['qtd_vendas'], v['valor_total'] or 0.0)
        )

    ranking = ft.Container(
        padding=20,
        border_radius=20,
        bgcolor=cor_fundo_container,
        border=ft.border.all(1, cor_borda),
        content=ft.Column([
            ft.Text("RANKING DO MÊS", size=12, color=cor_texto_secundario, weight="bold"),
            ft.Divider(height=10, color="transparent"),
            coluna_ranking
        ]),
    )

    # Montagem da lista principal
    conteudo_principal = ft.ListView(
        controls=[
            ft.Text("Consolidação", size=28, weight="bold", color=cor_texto_principal),
            ft.Text("Confira os resultados reais do sistema", size=14, color=cor_texto_secundario),
            ft.Container(height=15),
            card_receita,
            ft.Container(height=15),
            card_volume,
            ft.Container(height=15),
            ranking,
            ft.Container(height=100),
        ],
        padding=20,
        expand=True,
    )

    page.add(conteudo_principal)

    # --- NAVEGAÇÃO ---
    def trocar_aba(e):
        index = nav.selected_index
        if index == 0: pass
        elif index == 1: on_stock()
        elif index == 2: on_users()
        elif index == 3: on_perfil()

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=0,
        on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicial"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, selected_icon=ft.Icons.INVENTORY_2, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, selected_icon=ft.Icons.GROUP, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Perfil"),
        ]
    )

    page.navigation_bar = ft.Container(
        content=nav,
        margin=ft.margin.only(left=25, right=25, bottom=30),
        border_radius=40, 
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )

    page.update()