import flet as ft
import flet_charts as fch

def home_page(page: ft.Page, on_logout, on_stock, on_users, on_perfil):

    def sair_app(e):
        on_logout()

    page.controls.clear()
    
    # --- LÓGICA DE CORES ADAPTÁVEIS (O SEGREDO PARA MUDAR O FUNDO) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    
    # 1. Cor de Fundo da PÁGINA (Preto no Dark, Branco Azulado no Light)
    page.bgcolor = "#000000" if is_dark else "#F0F4FF" 
    
    # 2. Cor de Fundo dos CONTAINERS (Azul Escuro no Dark, Azul Claro no Light)
    cor_fundo_container = "#0b1445" if is_dark else "#E1E8FA" 
    
    # 3. Cor do Texto (Branco no Dark, Preto/Azul Escuro no Light)
    cor_texto_principal = ft.Colors.WHITE if is_dark else "#0b1445"
    cor_texto_secundario = ft.Colors.WHITE_70 if is_dark else ft.Colors.GREY_700
    
    # 4. Cor das Bordas (Azul Profundo no Dark, Azul Suave no Light)
    cor_borda = "#1E2B4E" if is_dark else "#BCCAE3"

    # AppBar (Mantendo o azul escuro padrão para contraste)
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
        actions=[
            ft.IconButton(
                icon=ft.Icons.EXIT_TO_APP,
                icon_color="white",
                tooltip="Sair",
                on_click=sair_app
            )
        ]
    )

    # -------------------------
    # CARD RECEITA DO MÊS
    # -------------------------
    card_receita = ft.Container(
        padding=20,
        border_radius=20,
        bgcolor=cor_fundo_container, # Usa a variável dinâmica
        border=ft.border.all(1, cor_borda), # Usa a variável dinâmica
        content=ft.Column(
            [
                ft.Text("RECEITA DO MÊS", size=12, color=cor_texto_secundario, weight="bold"),
                ft.Row(
                    [
                        ft.Text(
                            "R$ 15.420,00",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_ACCENT_400 if is_dark else ft.Colors.GREEN_700,
                        ),
                        ft.Container(
                            content=ft.Text("+8.8%", size=12, color=ft.Colors.GREEN, weight="bold"),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN),
                            padding=5,
                            border_radius=5
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text("Comparado ao mês anterior", size=10, color=cor_texto_secundario),
            ]
        ),
    )

    # -------------------------
    # CARD VOLUME SEMANAL (GRÁFICO)
    # -------------------------
    card_volume = ft.Container(
        bgcolor=cor_fundo_container, # Usa a variável dinâmica
        padding=20,
        border_radius=25,
        border=ft.border.all(1, cor_borda), # Usa a variável dinâmica
        content=ft.Column([
            ft.Text("VOLUME DE VENDAS", size=12, color=cor_texto_secundario, weight="bold"),
            ft.Container(
                height=200,
                content=fch.BarChart(
                    interactive=True,
                    max_y=110,
                    left_axis=fch.ChartAxis(
                        labels=[fch.ChartAxisLabel(value=v, label=ft.Text(str(v), color=cor_texto_principal, size=10)) for v in [0, 50, 100]]
                    ),
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
                        for i, v in enumerate([40, 100, 30, 60, 80])
                    ],
                )
            )
        ])
    )

    # -------------------------
    # RANKING VENDEDORES
    # -------------------------
    def vendedor(nome, vendas, valor, cor):
        return ft.Container(
            padding=12,
            border_radius=15,
            # No Light, o fundo do vendedor fica branco puro para destacar do card azul claro
            bgcolor=cor_fundo_container if is_dark else "#FFFFFF",
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, cor_texto_principal)),
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(nome, weight=ft.FontWeight.BOLD, color=cor_texto_principal),
                            ft.Text(f"{vendas} VENDAS", size=11, color=cor_texto_secundario),
                        ],
                        spacing=2
                    ),
                    ft.Text(valor, weight=ft.FontWeight.BOLD, color=cor),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )

    ranking = ft.Container(
        padding=20,
        border_radius=20,
        bgcolor=cor_fundo_container, # Usa a variável dinâmica
        border=ft.border.all(1, cor_borda), # Usa a variável dinâmica
        content=ft.Column(
            [
                ft.Text("RANKING DO MÊS", size=12, color=cor_texto_secundario, weight="bold"),
                ft.Divider(height=10, color="transparent"),
                vendedor("Gabriel Santos", "199", "R$ 2.230,00", ft.Colors.GREEN),
                vendedor("Alicia Antonella", "176", "R$ 2.000,00", ft.Colors.GREEN),
                vendedor("Luan Gabriel", "156", "R$ 1.898,00", ft.Colors.RED_400),
            ],
            spacing=10
        ),
    )

    conteudo_principal = ft.ListView(
        controls=[
            ft.Text("Consolidação", size=28, weight="bold", color=cor_texto_principal),
            ft.Text("Confira os resultados de hoje", size=14, color=cor_texto_secundario),
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

    # -------------------------
    # NAVIGATION BAR
    # -------------------------
    def trocar_aba(e):
        indices = {0: None, 1: on_stock, 2: on_users, 3: on_perfil}
        if indices[nav.selected_index]:
            indices[nav.selected_index]()
    
    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=0,
        on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
            
        ],
    )

    page.navigation_bar = ft.Container(
        content=nav,
        margin=ft.margin.only(left=20, right=20, bottom=20),
        border_radius=30,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )

    page.update()