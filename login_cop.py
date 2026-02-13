import flet as ft

def login_view(page: ft.Page, on_login_sucesso):

    page.bgcolor = ft.Colors.BLACK
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    mensagem = ft.Text()

    def login(e):
        if usuario.value == "admin" and senha.value == "1234":
            on_login_sucesso()
        else:
            mensagem.value = "Usuário ou senha inválidos."
            mensagem.color = ft.Colors.RED
            page.update()

    usuario = ft.TextField(
        hint_text="email",
        border_radius=10,
        bgcolor=ft.Colors.BLUE_700,
        border_color=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        width=280,
    )

    senha = ft.TextField(
        hint_text="senha",
        password=True,
        can_reveal_password=True,
        border_radius=10,
        bgcolor=ft.Colors.BLUE_700,
        border_color=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        width=280,
        on_submit=login,
    )

    botao_login = ft.ElevatedButton(
        "ENTRAR",
        width=200,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_500,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=20),
        ),
        on_click=login,
    )

    card_login = ft.Container(
        width=330,
        padding=30,
        bgcolor="#0b1445",
        border_radius=30,
        content=ft.Column(
            [
                ft.Text(
                    "LOGIN",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Container(height=15),
                usuario,
                ft.Container(height=10),
                senha,
                ft.Container(height=10),
                ft.Checkbox(
                    label="Li e estou de acordo com os Termos de Uso",
                    label_style=ft.TextStyle(color=ft.Colors.WHITE70),
                    height=40,
                ),
                ft.Container(height=20),
                botao_login,
                ft.Container(height=10),
                mensagem,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    def esqueci_senha(e):
        mensagem.value = "Função de recuperação de senha ainda não implementada."
        mensagem.color = "blue"
        page.update()

    link_senha = ft.TextButton("Esqueci minha senha", on_click=esqueci_senha)

    # ✅ IMAGEM CORRIGIDA
    logo = ft.Image(
        src="imgs/icon.png",   # confira se a pasta é imgs mesmo
        width=180,
        height=180,
        fit="contain",         # 👈 corrigido aqui
    )

    return ft.Column(
        [
            logo,
            ft.Container(height=25),
            ft.Text(
                "Vende de Tudo",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            ft.Container(height=30),
            card_login,
            link_senha,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
