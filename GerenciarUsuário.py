import flet as ft

def main(page: ft.Page):



    page.title = "Gerenciar Usuários"
    page.bgcolor = "black"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    def status_badge(status):
        return ft.Container(
            content=ft.Text(
                status,
                size=12,
                weight="bold",
            ),
            bgcolor="green" if status == "ATIVO" else "red",
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            border_radius=20,
        )
    def user_card(codigo, nome, cargo, admissao, status, detalhes=None):
        return ft.Container(
            bgcolor="#0F1C3F",
            border_radius=15,
            padding=15,
            margin=ft.margin.only(bottom=15),
            content=ft.Column(
                spacing=8,
                        alignment="spaceBetween",
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(codigo, size=12, color="grey"),
                            ft.Text(f"ADMISSÃO: {admissao}", size=12, color="grey"),
                        ],
                    ),
                    ft.Row(
                        alignment="spaceBetween",
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(nome, size=16, weight="bold"),
                                    ft.Text(cargo, size=12, color="grey"),
                                ],
                            ),
                            status_badge(status),
                        ],
                    ),
                    ft.Container(
                        visible=status == "INATIVO",
                        bgcolor="#1c1c1c",
                        border_radius=10,
                        padding=10,
                        content=ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text(
                                    "DETALHES DA DESATIVAÇÃO",
                                    size=12,
                                    color="red",
                                    weight="bold",
                                ),
                                ft.Text(
                                    detalhes if detalhes else "",
                                    size=12,
                                    italic=True,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        visible=status == "ATIVO",
                        content=ft.ElevatedButton(
                            "Desativar Acesso",
                            icon=ft.Icons.BLOCK,
                            style=ft.ButtonStyle(
                                bgcolor="green",
                                shape=ft.RoundedRectangleBorder(radius=20),
                            ),
                        ),
                    ),
                ],
            ),
        )
    lista_usuarios = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
        controls=[
            user_card("AD-001", "João Silva", "ADMINISTRADOR", "2023/01/10", "ATIVO"),
            user_card("VT-934", "Carlos Lima", "VENDEDOR", "2023/05/15", "INATIVO",
                "Pedido de demissão para novos projetos.\nData: 20/12/2025",
            ),
            user_card("VT-473", "Alicia Antonella", "VENDEDOR", "2023/08/20", "ATIVO"),
            user_card("VT-638", "Gabriel Santos", "VENDEDOR", "2023/05/16", "ATIVO"),
        ],
    )
    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Text("Gerenciar Usuários", size=22, weight="bold"),
                        ft.FloatingActionButton(
                            icon=ft.Icons.ADD,
                            bgcolor="#1B4F9C",
                            mini=True,
                        ),
                    ],
                ),
                ft.TextField(
                    hint_text="Buscar...",
                    prefix_icon=ft.Icons.SEARCH,
                    border_radius=20,
                    bgcolor="#162447",
                    border_color="transparent",
                ),
                lista_usuarios, 
            ],
        )
    )
    page.navigation_bar = ft.NavigationBar(
        selected_index=2,
        bgcolor="#0F1C3F",
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Perfil"),
        ],
    )

ft.app(target=main)
