import flet as ft
from database import validar_login 
import time

def login_view(page: ft.Page, on_login_sucesso):
    page.bgcolor = "#050505" 
    page.controls.clear()
    
    mensagem = ft.Text(value="", color=ft.Colors.RED_400, size=12, weight="bold")

    # --- FUNÇÃO DE LOGIN CONECTADA AO BANCO ---
    def realizar_login(e):
        if not usuario.value or not senha.value:
            mensagem.value = "Por favor, preencha todos os campos."
            page.update()
            return

        # Chama a função do banco de dados
        sucesso, resultado = validar_login(usuario.value, senha.value)

        if sucesso:
            # SINALIZANDO SUCESSO NA UI
            mensagem.value = f"Bem-vindo, {resultado.get('nome_user', 'Usuário')}!"
            mensagem.color = ft.Colors.GREEN_400
            page.update()
            
            # Pequeno delay para feedback visual
            time.sleep(1) 
            
            # MANDANDO OS DADOS DIRETO PARA O MAIN
            # Agora on_login_sucesso deve aceitar um argumento (ex: carregar_home(user))
            on_login_sucesso(resultado)
        else:
            mensagem.value = resultado 
            mensagem.color = ft.Colors.RED_400
            page.update()

    # --- ESTILO DO CAMPO (TextField Personalizado) ---
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

    usuario = estilo_campo("Usuário ou E-mail")
    
    def toggle_password(e):
        senha.password = not senha.password
        senha.suffix.icon = ft.Icons.VISIBILITY_OFF if senha.password else ft.Icons.VISIBILITY
        senha.update()

    senha = estilo_campo(
        label="Senha", 
        password=True, 
        on_submit=realizar_login,
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
        on_click=realizar_login,
    )

    logo = ft.Image(
        src="imgs/icon.png",
        width=200,
        height=200,
        fit="contain",
    )

    card_login = ft.Container(
        content=ft.Column(
           [
                ft.Text("LOGIN", size=30, weight=ft.FontWeight.BOLD, color="white"),
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