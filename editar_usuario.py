import flet as ft

def editar_usuario(page: ft.Page, on_users):
    page.controls.clear()
    page.title = "Editar Usuário"
    
    # REMOVIDO: page.theme_mode e page.bgcolor fixos para respeitar o global
    page.window_width = 400
    page.window_height = 800
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Lógica de cores adaptáveis
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_input_fundo = "#0A122A" if is_dark else "#F0F2F5"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_NEW,
            icon_color="white", # AppBar escura fixa
            on_click=lambda _: on_users()
        ),
        title=ft.Text("Editar Usuário", size=20, weight="bold", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    def estilo_input(label, hint="", value="", read_only=False, col=None):
        input_field = ft.TextField(
            value=value,
            hint_text=hint,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_600),
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color=cor_texto), # Dinâmico
            expand=True,
        )
        
        container = ft.Column(
            [
                ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=input_field,
                    bgcolor=cor_input_fundo, # Dinâmico
                    border=ft.border.all(1, cor_borda), # Dinâmico
                    border_radius=10,
                    padding=ft.padding.only(right=10),
                )
            ],
            spacing=5,
            col=col 
        )
        return container, input_field

    # Criando os campos responsivos
    nome_container, nome_input = estilo_input("NOME COMPLETO", hint="Vitor Irlândes", col=12)
    salario_container, salario_input = estilo_input("SALÁRIO", hint="R$ 1.500,00", col=12)
    data_container, data_input = estilo_input("DATA DE CONTRATAÇÃO", hint="01/02/2026", col=12)

    # Dropdown ajustado para o tema
    cargo_dropdown = ft.Dropdown(
        hint_text="Selecione o cargo",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_600),
        options=[ft.dropdown.Option("ADMINISTRADOR"), ft.dropdown.Option("VENDEDOR")],
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(color=cor_texto), # Dinâmico
        content_padding=ft.padding.only(left=15, right=0),
    )

    cargo_container = ft.Column(
        [
            ft.Text("CARGO", size=11, color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=cargo_dropdown,
                bgcolor=cor_input_fundo, # Dinâmico
                border=ft.border.all(1, cor_borda), # Dinâmico
                border_radius=10,
                height=55,
            )
        ],
        spacing=5,
        col=6 
    )

    def salvar(e):
        print("Usuário salvo com sucesso!")

    layout_campos = ft.ResponsiveRow(
        controls=[
            nome_container,
            salario_container,
            data_container,
            cargo_container, 
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
                    "Salvar", 
                    on_click=salvar, 
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