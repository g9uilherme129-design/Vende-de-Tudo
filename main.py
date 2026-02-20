# Importa a biblioteca Flet
import flet as ft

# Importa login_view do arquivo login.py
from login import login_view

# Importa home_page do arquivo home.py
from home import home_page

# Função principal do app (recebe a página do Flet)
def main(page: ft.Page):
    # Define o título da janela/aplicação
    page.title = "Vende de Tudo"
    
    # Define espaçamento interno da página
    page.padding = 20
    
    # Define o tema como claro
    page.theme_mode = "light"
    
    # Centraliza os elementos verticalmente
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Centraliza os elementos horizontalmente
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ---------------------------
    # Função para carregar a HOME
    # ---------------------------

    # Função que abre a tela principal
    def carregar_home():
        # Aqui será chamada a tela home
        # Envia a página e a função de logout
        home_page(page, on_logout=carregar_login)

    # ---------------------------
    # Função para carregar LOGIN
    # ---------------------------

    # Função que abre a tela de login
    def carregar_login():
        # Remove a barra superior (AppBar)
        page.appbar = None
        
        # Limpa todos os elementos da tela
        page.controls.clear()
        
        # Adiciona a tela de login passa a função para ir à home após logado no sistema
        page.add(login_view(page, on_login_sucesso=carregar_home))
        
        # Atualiza a interface
        page.update()

    def carregar_stock():
        # Aqui será chamada a tela home
        # Envia a página e a função de logout
        estoque_page(page, on_logout=carregar_home)

    # ---------------------------
    # Inicia o app no LOGIN
    # ---------------------------
    # Quando o aplicativo iniciar, ele abrirá diretamente a tela de login
    carregar_login()

# Executa a aplicação
ft.run(main)
