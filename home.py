# Importa a biblioteca Flet
import flet as ft

# Função que cria a tela home
def home_page(page: ft.Page, on_logout):

    # ---------------------------
    # Função para sair do app (voltar para login)
    # ---------------------------
    def sair_app(e):
        # Chama a função que retorna para o login
        on_logout()

    # ---------------------------
    # Função para voltar da página produtos para HOME
    # ---------------------------
    def carregar_home():
        # Chama novamente a própria função para reconstruir a HOME
        home_page(page, on_logout)

    # ---------------------------
    # Limpa controles da página e configura AppBar
    # ---------------------------
    # Remove todos os elementos atuais da tela
    page.controls.clear()

    page.appbar = ft.AppBar(
        leading=ft.PopupMenuButton(
            icon=ft.Icons.MENU,
            items=[],
        ),
        title = ft.Text("Vende de Tudo"),
        actions=[
            ft.IconButton(ft.Icons.SEARCH),
            ft.IconButton(ft.Icons.MORE_VERT),
            ft.IconButton(
                icon=ft.Icons.EXIT_TO_APP,
                tooltip="Sair",
                on_click=sair_app
            )
        ],
        bgcolor=ft.Colors.SURFACE_CONTAINER,
    )

    # ---------------------------
    # Conteúdo central
    # ---------------------------

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(
                "Bem-vindo(a) ao Vende de Tudo!",
                size=22,
                weight=ft.FontWeight.BOLD
            )
        )
    )

    page.update()

ft.run(home_page)