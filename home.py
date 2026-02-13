import flet as ft

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

    card_volume = ft.Container(
        padding=15,
        border_radius=20,
        bgcolor="#0b1445",
        content=ft.Column(
            [
                ft.Text("VOLUME SEMANAL", size=12, color=ft.Colors.WHITE70),
                ft.Container(
                    height=120,
                    content=ft.Row(
                        [
                            ft.Container(width=20, height=60, bgcolor=ft.Colors.GREEN),
                            ft.Container(width=20, height=90, bgcolor=ft.Colors.GREEN),
                            ft.Container(width=20, height=75, bgcolor=ft.Colors.GREEN),
                            ft.Container(width=20, height=110, bgcolor=ft.Colors.GREEN),
                            ft.Container(width=20, height=130, bgcolor=ft.Colors.GREEN),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        vertical_alignment=ft.CrossAxisAlignment.END
                    )
                )
            ]
        )
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

    page.add(
        ft.Column(
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
            scroll=ft.ScrollMode.AUTO
        )
    )

    page.update()
