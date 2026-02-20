# Importa a biblioteca Flet
import flet as ft


def estoque(page: ft.Page, on_logout):  
    page.bgcolor = ft.Colors.BLACK_45


    header = ft.Row(
        controls=[
            ft.Text("Consultar Estoque", size=24, weight="bold", color="white"),
            # Substitua 'assets/botao_plus.png' pelo caminho real da sua imagem
            ft.Container(
                content=ft.Image(
                    src="https://cdn-icons-png.flaticon.com/512/1828/1828817.png", # Exemplo de URL
                    width=35,
                    height=35,
                    fit=ft.ImageFit.CONTAIN,
                ),
                on_click=lambda _: print("Botão adicionar clicado!"),
                mouse_cursor=ft.MouseCursor.CLICK,
            )
        ],
        alignment="spaceBetween"
    )