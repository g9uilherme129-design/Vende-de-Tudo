# Importa a biblioteca Flet
import flet as ft


def estoque(page: ft.Page, on_logout):  
    page.bgcolor = ft.Colors.BLACK_45

    
    header = ft.Row(
            controls=[
                ft.Text("Consultar Estoque", size=24, weight="bold", color="white"),
                ft.Container(
                    content=ft.Image(
                        src="imgs/addicon.png",
                        width=35,
                        height=35,
                    ),
                    on_click=lambda _: print("Botão adicionar clicado!"),
                    mouse_cursor=ft.MouseCursor.CLICK,
                )
            ],
            alignment="spaceBetween"
        )
