import flet as ft

def main(page: ft.Page):
    page.title = "Novo Usuário"
    page.bgcolor = "black"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    def salvar_usuario(e):
        print("Usuário cadastrado!")

    formulario = ft.Container(
        bgcolor="#0F1C3F",
        border_radius=15,
        padding=20,
        content=ft.Column(
            spacing=15,
            controls=[

                ft.Text("Novo Usuário", size=22, weight="bold"),
                ft.Text("NOME COMPLETO", size=12, color="grey"),
                ft.TextField(
                    hint_text="Nome do funcionário",
                    prefix_icon=ft.Icons.PERSON,
                    border_radius=20,
                    bgcolor="#162447",
                    border_color="transparent",
                ),
                ft.Text("CARGO", size=12, color="grey"),
                ft.Dropdown(
                    border_radius=20,
                    bgcolor="#162447",
                    border_color="transparent",
                    options=[
                        ft.dropdown.Option("ADMINISTRADOR"),
                        ft.dropdown.Option("VENDEDOR"),
                    ],
                ),
                ft.Text("SALÁRIO", size=12, color="grey"),
                ft.TextField(
                    hint_text="R$ 0,00",
                    prefix_icon=ft.Icons.ATTACH_MONEY,
                    border_radius=20,
                    bgcolor="#162447",
                    border_color="transparent",
                ),
                ft.Text("DATA DE CONTRATAÇÃO", size=12, color="grey"),
                ft.TextField(
                    hint_text="dd/mm/aaaa",
                    prefix_icon=ft.Icons.CALENDAR_MONTH,
                    border_radius=20,
                    bgcolor="#162447",
                    border_color="transparent",
                ),
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Adicionar Usuário",
                    icon=ft.Icons.SAVE,
                    on_click=salvar_usuario,
                    style=ft.ButtonStyle(
                        bgcolor="#0867F5",
                        shape=ft.RoundedRectangleBorder(radius=20),
                        padding=20,
                    ),
                    width=250,
                ),
            ],
        ),
    )

    page.add(
        ft.Column(
            expand=True,
            horizontal_alignment="center",
            controls=[formulario],
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