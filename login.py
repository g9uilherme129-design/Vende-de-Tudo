import flet as ft
from database import verificar_login_db # Importando a conexão real

def login_view(page: ft.Page, on_login_sucesso):
    page.bgcolor = "#050505" 
    page.controls.clear()
    
    mensagem = ft.Text(value="", color=ft.Colors.RED_400, size=12, weight="bold")

    def login(e):
        # Validação real no MySQL
        user_data = verificar_login_db(email_field.value, senha_field.value)
        
        if user_data:
            # Salva os dados do usuário na sessão da página para usar no Perfil
            page.session.set("user_id", user_data["id_user"])
            page.session.set("user_name", user_data["nome_user"])
            page.session.set("user_perfil", user_data["perfil"])
            
            on_login_sucesso()
        else:
            mensagem.value = "E-mail ou senha incorretos ou usuário inativo."
            page.update()

    # Reaproveitando seu estilo de campo
    def estilo_campo(label, password=False, suffix=None, on_submit=None):
        return ft.TextField(
            label=label,
            password=password,
            can_reveal_password=True if password else False,
            height=55,
            border_color="#1E2B4E",
            focused_border_color=ft.Colors.BLUE_500,
            bgcolor="#0A122A",
            border_radius=12,
            label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_200),
            color=ft.Colors.WHITE,
            on_submit=on_submit
        )

    email_field = estilo_campo("E-mail")
    senha_field = estilo_campo("Senha", password=True, on_submit=login)

    card_login = ft.Container(
        content=ft.Column(
            [
                ft.Text("LOGIN", size=30, weight="bold", color="white"),
                ft.Divider(height=10, color="transparent"),
                email_field,
                senha_field,
                ft.ElevatedButton(
                    "ENTRAR",
                    height=50, width=250,
                    style=ft.ButtonStyle(bgcolor="#1B4F9C", color="white", shape=ft.RoundedRectangleBorder(radius=12)),
                    on_click=login,
                ),
                mensagem,
            ],
            spacing=15,
            horizontal_alignment="center"
        ),
        bgcolor="#081035", padding=40, border_radius=25, width=400,
    )

    return ft.Column(
        [
            ft.Image(src="imgs/icon.png", width=150, height=150),
            card_login
        ],
        alignment="center", horizontal_alignment="center", expand=True
    )