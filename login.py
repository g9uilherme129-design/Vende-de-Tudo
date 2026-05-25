import flet as ft
from database import validar_login 
import time

def login_view(page: ft.Page, on_login_sucesso, on_recuperar_senha):
    # Configuração inicial da página
    page.bgcolor = "#050505" 
    page.controls.clear()
    page.padding = 0  # Garante preenchimento total em telas menores
    
    mensagem = ft.Text(value="", color=ft.Colors.RED_400, size=12, weight="bold")

    # --- FUNÇÃO DE LOGIN CONECTADA AO BANCO ---
    def realizar_login(e):
        if not usuario.value or not senha.value:
            mensagem.value = "Por favor, preencha todos os campos."
            page.update()
            return

        sucesso, resultado = validar_login(usuario.value, senha.value)

        if sucesso:
            mensagem.value = f"Bem-vindo, {resultado.get('nome_user', 'Usuário')}!"
            mensagem.color = ft.Colors.GREEN_400
            page.update()
            on_login_sucesso(resultado)
        else:
            mensagem.value = resultado 
            mensagem.color = ft.Colors.RED_400
            page.update()

    # --- ELEMENTOS DA UI INSTANCIADOS COMO OBJETOS CONFIGURÁVEIS ---
    def estilo_campo(label, password=False, suffix=None, on_submit=None):
        return ft.TextField(
            label=label,
            password=password,
            border_color="#1E2B4E",
            focused_border_color=ft.Colors.BLUE_500,
            bgcolor="#0A122A",
            border_radius=12,
            label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_200),
            color=ft.Colors.WHITE,
            suffix=suffix,
            on_submit=on_submit 
        )

    usuario = estilo_campo("Usuário ou E-mail", on_submit=realizar_login)
    
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

    link_senha = ft.TextButton(
        "Esqueci minha senha",
        on_click=lambda _: on_recuperar_senha(),
        style=ft.ButtonStyle(color=ft.Colors.BLUE_GREY_200),
    )

    botao_login = ft.ElevatedButton(
        "ENTRAR",
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
        fit="contain",
    )

    texto_titulo = ft.Text("LOGIN", weight=ft.FontWeight.BOLD, color="white")

    card_login = ft.Container(
        content=ft.Column(
            [
                texto_titulo,
                ft.Divider(height=5, color="transparent"),
                usuario,
                senha,
                ft.Row([link_senha], alignment=ft.MainAxisAlignment.END),
                ft.Divider(height=5, color="transparent"),
                botao_login,
                mensagem,
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor="#081035",
        border_radius=25,
        border=ft.border.all(1, "#1E2B4E"),
    )

    # --- CONTEÚDO PRINCIPAL RENDERIZADO DENTRO DE UM CONTAINER ---
    layout_principal = ft.Column(
        [
            logo,
            card_login
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
    )

    container_retorno = ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=layout_principal,
        padding=15
    )

    # --- FUNÇÃO DE REDIMENSIONAMENTO DINÂMICO (RESPONSIVIDADE REAL-TIME) ---
    def ajustar_responsividade(e=None):
        # Captura a largura atual de forma segura
        largura_atual = page.width if page.width else (page.client_size.width if page.client_size else 800)
        
        if largura_atual < 600:
            # Configuração para Smartphones
            tamanho_logo = min(140, int(largura_atual * 0.4))
            largura_card = int(largura_atual - 30)  # Margem fina nas laterais
            altura_campo = 46
            padding_interno = 20
            largura_botao = int(largura_card * 0.7)
            tamanho_fonte_titulo = 24
        elif largura_atual < 1000:
            # Configuração para Tablets
            tamanho_logo = 180
            largura_card = 460
            altura_campo = 52
            padding_interno = 32
            largura_botao = 240
            tamanho_fonte_titulo = 28
        else:
            # Configuração para Desktops / Telas Grandes
            tamanho_logo = 220
            largura_card = 500
            altura_campo = 56
            padding_interno = 40
            largura_botao = 280
            tamanho_fonte_titulo = 32

        # Redimensiona os componentes em tempo de execução
        logo.width = tamanho_logo
        logo.height = tamanho_logo
        
        card_login.width = largura_card
        card_login.padding = padding_interno
        
        texto_titulo.size = tamanho_fonte_titulo
        
        usuario.height = altura_campo
        senha.height = altura_campo
        
        botao_login.height = altura_campo
        botao_login.width = largura_botao
        
        page.update()

    # Define o gatilho para atualizar o layout sempre que a tela mudar de tamanho ou rotacionar
    page.on_resized = ajustar_responsividade
    
    # Executa a primeira calibragem dos tamanhos
    ajustar_responsividade()

    return container_retorno