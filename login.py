# Importa a biblioteca Flet
import flet as ft

# Função que cria a tela de login
def login_view(page: ft.Page, on_login_sucesso):
    page.bgcolor=ft.Colors.GREY # Cor de fundo da página

    avatar = ft.Container( # Container que representa o avatar
        content=ft.Icon( # Ícone dentro do container
            ft.Icons.PERSON, # Ícone de pessoa
            size=70, # Tamanho do ícone
            color=ft.Colors.WHITE # Cor branca do ícone.
        ),

        width=110, # Largura do Container
        height=110, # Altura do Container
        bgcolor=ft.Colors.LIGHT_BLUE, # Cor do fundo do Container
        border_radius=55, # Deixa o container redondo
        alignment=ft.Alignment.CENTER # Centraliza o conteúdo
    )

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
        border_color=ft.Colors.BLACK, # Cor da borda
        focused_border_color=ft.Colors.YELLOW_ACCENT_700, # Cor da borda quando focado
        bgcolor=ft.Colors.WHITE_30, # Cor de fundo do campo de usuário
    )


    senha = ft.TextField( # Campo de texto para senha
        label="Senha", # Rótulo
        password=True, # Oculta os caracteres
        can_reveal_password=True, # Permite mostrar/ocultar senha
        width=300, # Largura
        on_submit=login, # Executa login ao pressionar Enter
        border_color=ft.Colors.BLACK, # Cor da borda
        focused_border_color=ft.Colors.YELLOW_ACCENT_700, # Cor da borda quando focado
        bgcolor=ft.Colors.WHITE_30, # Cor de fundo do campo de senha
    )

    # Botão que chama a função login
    botao_login = ft.ElevatedButton("Entrar", on_click=login)
    

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

    return ft.Container(
        content=ft.Column(
            [
                avatar,
                ft.Text("Bem-vindo(a)!", size=20, weight=ft.FontWeight.BOLD),
                usuario,
                senha,
                botao_login,
                mensagem,
                link_senha,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15, # Espaçamento entre os elementos
        ),
        
        # Estilização do Container de fundo
        bgcolor=ft.Colors.LIGHT_BLUE_900,       # Cor do fundo do container
        padding=40,                    # Espaço interno entre borda e conteúdo
        border_radius=20,              # Arredondamento das bordas
        shadow=ft.BoxShadow(           # Adiciona uma sombra suave
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        ),
        width=400,                     # Largura do container branco
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
