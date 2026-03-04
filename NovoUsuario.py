import flet as ft

def novo_usuario(page: ft.Page, on_users):
    page.controls.clear()
    page.title = "Cadastro de Novo Usuário"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.window_width = 400
    page.window_height = 800
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    def estilo_input(label, hint="", value="", width=None, read_only=False):
        input_field = ft.TextField(
            value=value,
            hint_text=hint,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color="white"),
        )

        return ft.Column(
            [
                ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=input_field,
                    bgcolor="#0A122A",
                    border=ft.border.all(1, "#1E2B4E"),
                    border_radius=10,
                    width=width if width else 360,
                )
            ],
            spacing=5
        ), input_field

    # Criando campos
    nome_container, nome_input = estilo_input("NOME COMPLETO", hint="Nome do funcionário")
    salario_container, salario_input = estilo_input("SALÁRIO", hint="R$ 0,00")
    data_container, data_input = estilo_input("DATA DE CONTRATAÇÃO", hint="dd/mm/aaaa")

    cargo_dropdown = ft.Dropdown(
        hint_text="Selecione o cargo",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
        options=[
            ft.dropdown.Option("ADMINISTRADOR"),
            ft.dropdown.Option("VENDEDOR"),
        ],
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(color="white"),
        content_padding=ft.padding.only(left=15, right=0),  # seta colada
    )

    cargo_container = ft.Column(
        [
            ft.Text(
                "CARGO",
                size=11,
                color=ft.Colors.TEAL_700,
                weight=ft.FontWeight.BOLD
            ),
            ft.Container(
                content=cargo_dropdown,
                bgcolor="#0A122A",
                border=ft.border.all(1, "#1E2B4E"),
                border_radius=10,
                width=250,  # 🔹 menor largura
                height=55,  # 🔹 altura mais compacta
            )
        ],
        spacing=5
    )

    def salvar_usuario(e):
        print("Usuário cadastrado!")

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Novo Usuário", size=28, weight=ft.FontWeight.BOLD, color="white"),
                ft.Divider(height=10, color="transparent"),

                nome_container,
                cargo_container,
                salario_container,
                data_container,

                ft.Divider(height=20, color="transparent"),

                ft.ElevatedButton(
                    "Adicionar",
                    on_click=salvar_usuario,
                    width=200,
                ),

                ft.TextButton("Voltar", on_click=lambda _: on_users()),
            ],
            spacing=15
        )
    )

    page.update()