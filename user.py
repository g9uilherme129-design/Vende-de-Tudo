import flet as ft


def usuarios(page: ft.Page, on_home, on_stock, on_perfil):

    page.controls.clear()
    page.appbar = None
    page.bgcolor = ft.Colors.BLACK

    # ---------------- HEADER ----------------
    header = ft.Row(
        [
            ft.Text(
                "Gerenciar Usuários",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.ADD, color=ft.Colors.WHITE),
                bgcolor="#1e3a8a",
                width=40,
                height=40,
                border_radius=20,
                on_click=lambda e: print("Botão ADICIONAR clicado")
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # ---------------- BUSCA ----------------
    campo_busca = ft.TextField(
        hint_text="Buscar...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=15,
        width=400,
        height=50,
        bgcolor="#0d1626",
        border_color="#1e293b",
        hint_style=ft.TextStyle(color="grey"),
        content_padding=10,
        color=ft.Colors.WHITE
    )

    # ---------------- CARD USUÁRIO ----------------
    def card_usuario(codigo, nome, cargo, admissao, ativo=True, motivo=None, data_desativacao=None):

        status_color = "#22c55e" if ativo else "#ef4444"
        status_text = "ATIVO" if ativo else "INATIVO"

        conteudo = [
            ft.Row(
                [
                    ft.Text(codigo, color=ft.Colors.WHITE70, size=12),
                    ft.Text(f"ADMISSÃO: {admissao}", color=ft.Colors.WHITE54, size=12),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(nome, color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(cargo, color=ft.Colors.WHITE54, size=12),
                        ]
                    ),
                    ft.Container(
                        content=ft.Text(status_text, size=12, weight=ft.FontWeight.BOLD),
                        bgcolor=status_color,
                        padding=ft.padding.symmetric(horizontal=12, vertical=5),
                        border_radius=20
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
        ]

        if not ativo:
            conteudo.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "DETALHES DA DESATIVAÇÃO",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color="#ff6b6b"
                            ),
                            ft.Text(
                                f'"{motivo}"',
                                size=12,
                                italic=True,
                                color=ft.Colors.WHITE70
                            ),
                            ft.Text(
                                f"DATA: {data_desativacao}",
                                size=11,
                                color=ft.Colors.WHITE54
                            )
                        ]
                    ),
                    bgcolor="#5c1d1d",
                    padding=12,
                    border_radius=15,
                    margin=ft.margin.only(top=10)
                )
            )

        else:
            conteudo.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.BLOCK, size=16, color=ft.Colors.WHITE),
                            ft.Text("Desativar Acesso", color=ft.Colors.WHITE)
                        ],
                    ),
                    bgcolor="#162052",
                    padding=10,
                    border_radius=25,
                    margin=ft.margin.only(top=10),
                    on_click=lambda e: print(f"{nome} - botão desativar clicado")
                )
            )

        return ft.Container(
            content=ft.Column(conteudo),
            bgcolor="#0b1445",
            padding=15,
            border_radius=20,
            margin=ft.margin.only(bottom=15)
        )

    # ---------------- LISTA ----------------
    lista_usuarios = ft.Column(
        [
            card_usuario("AD-001", "João Silva", "ADMINISTRADOR", "2023/01/10", True),
            card_usuario(
                "VT-934",
                "Carlos Lima",
                "VENDEDOR",
                "2023/05/15",
                ativo=False,
                motivo="Pedido de demissão para novos projetos.",
                data_desativacao="20/12/2025"
            ),
            card_usuario("VT-473", "Alicia Antonella", "VENDEDOR", "2023/08/20", True),
            card_usuario("VT-638", "Gabriel Santos", "VENDEDOR", "2023/05/16", True),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    layout = ft.Container(
        content=ft.Column(
            [
                header,
                ft.Container(campo_busca, margin=ft.margin.symmetric(vertical=15)),
                lista_usuarios
            ],
            expand=True
        ),
        padding=20,
        expand=True
    )

    page.add(layout)

    # ---------------- NAVEGAÇÃO ----------------
    def trocar_aba(e):
        index = nav.selected_index

        if index == 0:
            on_home()  # Chama home

        elif index == 1:
            on_stock()  # chama estoque

        elif index == 2:
            pass # Ja esta em usuarios

        elif index == 3:
            on_perfil()

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=2,
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