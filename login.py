# Importa a biblioteca Flet
import flet as ft

# Função que cria a tela de login
def login_view(page: ft.Page, on_login_sucesso):
    page.bgcolor = ft.Colors.BLACK_45 # Cor de fundo da página

    # Texto para exibir mensagens (erro/sucesso)
    mensagem = ft.Text(value="")

    def login(e):
        # Verifica usuário e senha
        if usuario.value == "admin" and senha.value == "1234":
            # Chama função de sucesso
            on_login_sucesso()
        else:
            # Define mensagem de erro
            mensagem.value = "Usuário ou senha inválidos."
            # Cor Vermelho para a mensagem de erro
            mensagem.color = "red"
            # Atualiza a página
            page.update()

    usuario = ft.TextField(
        label="Usuário", # Rótulo do campo
        width=300, # Largura do campo
        height=40,
        border_color=ft.Colors.BLUE_900, # Cor da borda
        focused_border_color=ft.Colors.BLUE_500, # Cor da borda quando focado
        bgcolor=ft.Colors.BLUE_900, # Cor de fundo do campo de usuário
        label_style=ft.TextStyle(color=ft.Colors.WHITE), # Cor do rótulo
    )


    senha = ft.TextField( # Campo de texto para senha
        label="Senha", # Rótulo
        password=True, # Oculta os caracteres
        can_reveal_password=True, # Permite mostrar/ocultar senha
        width=300, # Largura
        height=40,
        on_submit=login, # Executa login ao pressionar Enter
        border_color=ft.Colors.BLUE_900, # Cor da borda
        focused_border_color=ft.Colors.BLUE_500, # Cor da borda quando focado
        bgcolor=ft.Colors.BLUE_900, # Cor de fundo do campo de senha
        label_style=ft.TextStyle(color=ft.Colors.WHITE) # Cor do rótulo
    )

    # Botão que chama a função login
    botao_login = ft.ElevatedButton(
        "ENTRAR",
        width=150,
        height=45,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=150),
        ),
        on_click=login
    )
    

    def esqueci_senha(e):

        # Mensagem informativa
        mensagem.value = "Função de recuperação de senha ainda não implementada."

        # Cor azul
        mensagem.color = "white"

        # Atualiza a tela
        page.update()

    link_senha = ft.TextButton("Esqueci minha senha", on_click=esqueci_senha, style=ft.ButtonStyle(
        color=ft.Colors.WHITE, # Cor do texto do link
    ),)

    logo = ft.Image(
        src="imgs/icon.png", 
        width=300,
        height=300,
        fit="contain",
    )

    return ft.Container(
        content=ft.Column(
            [
               logo,
            ft.Container(height=0),
                ft.Text("LOGIN", size=20, weight=ft.FontWeight.BOLD, style=ft.TextStyle(color=ft.Colors.WHITE)), # Título de boas-vindas
                usuario,
                senha,
                botao_login,
                mensagem,
                link_senha,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20, # Espaçamento entre os elementos
        ),
        
        # Estilização do Container de fundo
        bgcolor="#12193D",       # Cor do fundo do container
        padding=40,                    # Espaço interno entre borda e conteúdo
        border_radius=20,              # Arredondamento das bordas
        shadow=ft.BoxShadow(           # Adiciona uma sombra suave
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        ),
        width=400,                     # Largura do container branco
        height=700
    )

    # return ft.Column(
    #     [
    #         avatar,
    #         ft.Text("Bem-vindo(a)!", size=20, weight=ft.FontWeight.BOLD),
    #         usuario,
    #         senha,
    #         botao_login,
    #         mensagem,
    #         link_senha,
    #     ],
    #     alignment=ft.MainAxisAlignment.CENTER,
    #     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    # )
