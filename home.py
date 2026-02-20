import flet as ft
import flet_charts as fch

def home_page(page: ft.Page, on_logout):

    def sair_app(e):
        on_logout()

    page.controls.clear()
    page.bgcolor = "#000000"

    page.appbar = ft.AppBar(
        title=ft.Text("Vende de Tudo"),
        bgcolor="#0b1445",
        actions=[
            ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=sair_app)
        ]
    )
    

    # -------------------------
    # CARD RECEITA DO MÊS
    # -------------------------

    card_receita = ft.Container(
        padding=15,
        border_radius=20,
        bgcolor="#0b1445",
        content=ft.Column(
            [
                ft.Text("RECEITA DO MÊS", size=12, color=ft.Colors.WHITE70),
                ft.Row(
                    [
                        ft.Text("R$ 43.500,00",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN),
                        ft.Text("+8.8%",
                                size=16,
                                color=ft.Colors.GREEN)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Text("Comparado ao mês anterior",
                        size=10,
                        color=ft.Colors.WHITE54)
            ]
        )
    )

    # -------------------------
    # CARD VOLUME SEMANAL
    # -------------------------

    # card_volume = ft.Container(
    #     padding=15,
    #     border_radius=20,
    #     bgcolor="#0b1445",
    #     content=ft.Column(
    #         [
    #             ft.Text("VOLUME SEMANAL", size=12, color=ft.Colors.WHITE70),
    #             ft.Container(
    #                 height=120,
    #                 content=ft.Row(
    #                     [
    #                         ft.Container(width=20, height=60, bgcolor=ft.Colors.GREEN),
    #                         ft.Container(width=20, height=90, bgcolor=ft.Colors.GREEN),
    #                         ft.Container(width=20, height=75, bgcolor=ft.Colors.GREEN),
    #                         ft.Container(width=20, height=110, bgcolor=ft.Colors.GREEN),
    #                         ft.Container(width=20, height=130, bgcolor=ft.Colors.GREEN),
    #                     ],
    #                     alignment=ft.MainAxisAlignment.SPACE_AROUND,
    #                     vertical_alignment=ft.CrossAxisAlignment.END
    #                 )
    #             )
    #         ]
    #     )
    # )


    card_volume = fch.BarChart(
        expand=True,
        interactive=True,
        max_y=110,
        border=ft.Border.all(1, ft.Colors.BLUE_400),
        horizontal_grid_lines=fch.ChartGridLines(
            color=ft.Colors.BLUE_300, width=1, dash_pattern=[3, 3]
        ),
        tooltip=fch.BarChartTooltip(
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.WHITE),
            border_radius=ft.BorderRadius.all(20),
        ),
        left_axis=fch.ChartAxis(
            label_size=40, title_size=40
        ),
        right_axis=fch.ChartAxis(show_labels=False),
        bottom_axis=fch.ChartAxis(
            label_size=40,
            labels=[
                fch.ChartAxisLabel(
                    value=0, label=ft.Container(ft.Text("S", color=ft.Colors.WHITE), padding=10)
                ),
                fch.ChartAxisLabel(
                    value=1, label=ft.Container(ft.Text("T", color=ft.Colors.WHITE), padding=10)
                ),
                fch.ChartAxisLabel(
                    value=2, label=ft.Container(ft.Text("Q", color=ft.Colors.WHITE), padding=10)
                ),
                fch.ChartAxisLabel(
                    value=3, label=ft.Container(ft.Text("Q", color=ft.Colors.WHITE), padding=10)
                ),
                fch.ChartAxisLabel(
                    value=4, label=ft.Container(ft.Text("S", color=ft.Colors.WHITE), padding=10)
                ),
            ],
        ),
        groups=[
            fch.BarChartGroup(
                x=0,
                rods=[
                    fch.BarChartRod(
                        from_y=0,
                        to_y=40,
                        width=40,
                        color=ft.Colors.GREEN_ACCENT_400,
                        border_radius=0,
                    ),
                ],
            ),
            fch.BarChartGroup(
                x=1,
                rods=[
                    fch.BarChartRod(
                        from_y=0,
                        to_y=100,
                        width=40,
                        color=ft.Colors.GREEN_ACCENT_400,
                        border_radius=0,
                    ),
                ],
            ),
            fch.BarChartGroup(
                x=2,
                rods=[
                    fch.BarChartRod(
                        from_y=0,
                        to_y=30,
                        width=40,
                        color=ft.Colors.GREEN_ACCENT_400,
                        border_radius=0,
                    ),
                ],
            ),
            fch.BarChartGroup(
                x=3,
                rods=[
                    fch.BarChartRod(
                        from_y=0,
                        to_y=60,
                        width=40,
                        color=ft.Colors.GREEN_ACCENT_400,
                        border_radius=0,
                    ),
                ],
            ),
            fch.BarChartGroup(
                x=4,
                rods=[
                    fch.BarChartRod(
                        from_y=0,
                        to_y=60,
                        width=40,
                        color=ft.Colors.GREEN_ACCENT_400,
                        border_radius=0,
                    ),
                ],
            ),
        ],
    )

    # -------------------------
    # RANKING VENDEDORES
    # -------------------------

    def vendedor(nome, vendas, valor, cor):
        return ft.Container(
            padding=10,
            border_radius=15,
            bgcolor="#111c5c",
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(nome,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE),
                            ft.Text(f"{vendas} VENDAS",
                                    size=11,
                                    color=ft.Colors.WHITE70)
                        ]
                    ),
                    ft.Text(valor,
                            weight=ft.FontWeight.BOLD,
                            color=cor)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

    ranking = ft.Container(
        padding=15,
        border_radius=20,
        bgcolor="#0b1445",
        content=ft.Column(
            [
                ft.Text("RANKING DE VENDEDORES DO MÊS",
                        size=12,
                        color=ft.Colors.WHITE70),
                ft.Container(height=10),
                vendedor("Gabriel Santos", "199", "R$ 2.230,00", ft.Colors.GREEN),
                ft.Container(height=8),
                vendedor("Alicia Antonella", "176", "R$ 2.000,00", ft.Colors.GREEN),
                ft.Container(height=8),
                vendedor("Luan Gabriel", "156", "R$ 1.898,00", ft.Colors.RED),
            ]
        )
    )

       # -------------------------
    # CONTEÚDO PRINCIPAL
    # -------------------------

    conteudo_principal = ft.Column(
        [
            ft.Text("Consolidação",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE),

            ft.Container(height=15),
            card_receita,
            ft.Container(height=15),
            card_volume,
            ft.Container(height=15),
            ranking,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True 
    )

    page.add(conteudo_principal)

        # -------------------------
    # RODAPÉ PREMIUM ARREDONDADO
    # -------------------------

    def trocar_aba(e):
        index = nav.selected_index

        if index == 0:
            print("Home")
        elif index == 1:
            print("Produtos")
        elif index == 2:
            print("Equipe")
        elif index == 3:
            print("Perfil")

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=0,
        on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label=""
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.INVENTORY_2_OUTLINED,
                selected_icon=ft.Icons.INVENTORY_2,
                label=""
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.GROUP_OUTLINED,
                selected_icon=ft.Icons.GROUP,
                label=""
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON_OUTLINE,
                selected_icon=ft.Icons.PERSON,
                label=""
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
