import flet as ft

def login_view(page: ft.Page, on_login_sucesso):
    # Ajuste: Usando cores que funcionam bem em ambos os modos ou forçando o fundo escuro apenas aqui
    page.bgcolor = "#050505" 
    page.controls.clear()
    
    mensagem = ft.Text(value="", color=ft.Colors.RED_400, size=12, weight="bold")

    def login(e):
        if usuario.value == "admin" and senha.value == "1234":
            on_login_sucesso()
        else:
            mensagem.value = "Usuário ou senha inválidos."
            page.update()

    # Estilo dos campos de entrada
    def estilo_campo(label, password=False, suffix=None, on_submit=None):
        return ft.TextField(
            label=label,
            password=password,
            height=50,
            border_color="#1E2B4E",
            focused_border_color=ft.Colors.BLUE_500,
            bgcolor="#0A122A",
            border_radius=12,
            label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_200),
            color=ft.Colors.WHITE,
            expand=True,
            suffix=suffix,
            on_submit=on_submit
        )

    usuario = estilo_campo("Usuário")
    
    def toggle_password(e):
        senha.password = not senha.password
        senha.suffix.icon = ft.Icons.VISIBILITY_OFF if senha.password else ft.Icons.VISIBILITY
        senha.update()

    senha = estilo_campo(
        label="Senha", 
        password=True, 
        on_submit=login,
        suffix=ft.IconButton(
            icon=ft.Icons.VISIBILITY,
            icon_color=ft.Colors.BLUE_GREY_200,
            on_click=toggle_password
        )
    )

    def esqueci_senha(e):
        mensagem.value = "Recuperação de senha enviada ao e-mail cadastrado."
        mensagem.color = ft.Colors.BLUE_200
        page.update()

    link_senha = ft.TextButton(
        "Esqueci minha senha",
        on_click=esqueci_senha,
        style=ft.ButtonStyle(color=ft.Colors.BLUE_GREY_200),
    )

    botao_login = ft.ElevatedButton(
        "ENTRAR",
        height=50,
        width=250,
        style=ft.ButtonStyle(
            bgcolor="#1B4F9C",
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=12),
            elevation=5
        ),
        on_click=login,
    )

    # Logo (Certifique-se que o caminho da imagem está correto no seu projeto)
    logo = ft.Image(
        src="imgs/icon.png",
        width=200,
        height=200,
        fit="contain",
    )

    # Card de Login
    card_login = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "LOGIN",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                ),
                ft.Divider(height=10, color="transparent"),
                usuario,
                senha,
                ft.Row([link_senha], alignment=ft.MainAxisAlignment.END),
                ft.Divider(height=10, color="transparent"),
                botao_login,
                mensagem,
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor="#081035",
        padding=40,
        border_radius=25,
        border=ft.border.all(1, "#1E2B4E"),
        width=400,
    )

    return ft.Column(
        [
            logo,
            card_login
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )