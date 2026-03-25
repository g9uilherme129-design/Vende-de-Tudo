import flet as ft

def novo_usuario(page: ft.Page, on_users):
    page.controls.clear()
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.window_width = 400
    page.window_height = 800
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color="white",
            on_click=lambda _: on_users()
        ),
        title=ft.Text("Novo Usuário", size=20, weight="bold"),
        bgcolor="#0b1445",
        center_title=True,
    )

    def estilo_input(label, hint="", value="", read_only=False, col=None):
        input_field = ft.TextField(
            value=value,
            hint_text=hint,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color="white"),
            expand=True,
        )
        
        container = ft.Column(
            [
                ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=input_field,
                    bgcolor="#0A122A",
                    border=ft.border.all(1, "#1E2B4E"),
                    border_radius=10,
                    padding=ft.padding.only(right=10),
                )
            ],
            spacing=5,
            col=col # Responsivo (1 a 12)
        )
        return container, input_field

    # Criando os campos responsivos
    nome_container, nome_input = estilo_input("NOME COMPLETO", hint="Nome do funcionário", col=12)
    
    cargo_dropdown = ft.Dropdown(
        hint_text="Selecione o cargo",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
        options=[
            ft.dropdown.Option("ADMINISTRADOR"),
            ft.dropdown.Option("VENDEDOR"),
        ],
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(color="white"),
        content_padding=ft.padding.only(left=15, right=0),
    )

    cargo_container = ft.Column(
        [
            ft.Text("CARGO", size=11, color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=cargo_dropdown,
                bgcolor="#0A122A",
                border=ft.border.all(1, "#1E2B4E"),
                border_radius=10,
                height=55,
            )
        ],
        spacing=5,
        col=6 # Ocupa metade da tela, responsivo
    )

    salario_container, salario_input = estilo_input("SALÁRIO", hint="R$ 0,00", col=12)
    data_container, data_input = estilo_input("DATA DE CONTRATAÇÃO", hint="dd/mm/aaaa", col=12)

    def salvar_usuario(e):
        print("Usuário cadastrado com sucesso!")

    layout_campos = ft.ResponsiveRow(
        controls=[
            nome_container,
            cargo_container, # Responsivo 50%
            salario_container,
            data_container,
        ],
        spacing=15,
        run_spacing=15,
    )

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Divider(height=10, color="transparent"),
                layout_campos,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Adicionar",
                    on_click=salvar_usuario,
                    width=200,
                    style=ft.ButtonStyle(
                        bgcolor="#1B4F9C",
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=10),
                    )
                ),
            ],
            spacing=10
        )
    )
    page.update()