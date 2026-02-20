# Importa a biblioteca Flet
import flet as ft

def login_view(page: ft.Page, on_login_sucesso):

    page.bgcolor = ft.Colors.BLACK_45

    mensagem = ft.Text(value="", color=ft.Colors.RED)

    def login(e):
        if usuario.value == "admin" and senha.value == "1234":
            on_login_sucesso()
        else:
            mensagem.value = "Usuário ou senha inválidos."
            mensagem.color = ft.Colors.RED
            page.update()

    usuario = ft.TextField(
        label="Usuário",
        height=45,
        border_color=ft.Colors.BLUE_900,
        focused_border_color=ft.Colors.BLUE_500,
        bgcolor=ft.Colors.BLUE_900,
        border_radius=10,
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
        color=ft.Colors.WHITE,
        expand=True
    )

    senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        height=45,
        on_submit=login,
        border_color=ft.Colors.BLUE_900,
        focused_border_color=ft.Colors.BLUE_500,
        bgcolor=ft.Colors.BLUE_900,
        border_radius=10,
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
        color=ft.Colors.WHITE,
        expand=True
    )

    def esqueci_senha(e):
        mensagem.value = "Função de recuperação de senha ainda não implementada."
        mensagem.color = ft.Colors.WHITE
        page.update()

    link_senha = ft.TextButton(
        "Esqueci minha senha",
        on_click=esqueci_senha,
        style=ft.ButtonStyle(color=ft.Colors.WHITE),
    )

    botao_login = ft.ElevatedButton(
        "ENTRAR",
        height=45,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=50),
        ),
        on_click=login,
    )

    logo = ft.Image(
        src="imgs/icon.png",
        width=280,
        fit="contain",
    )

    # Card responsivo
    card_login = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "LOGIN",
                    size=22,
                    weight=200,
                    color=ft.Colors.WHITE
                ),

                usuario,
                senha,

                # 🔥 Centralizado
                ft.Row(
                    [link_senha],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                # 🔥 Botão centralizado
                ft.Row(
                    [botao_login],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                mensagem,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor="#12193D",
        padding=30,
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        ),
        width=page.width * 0.9 if page.width < 500 else 400
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