# Importa a biblioteca Flet
import flet as ft


def estoque(page: ft.Page, on_logout):

    page.controls.clear()
    page.appbar = None
    page.bgcolor = ft.Colors.BLACK_45

    header = ft.Row(
        controls=[
            ft.Text(
                "Consultar Estoque",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            ft.Container(
                content=ft.Image(
                    src="imgs/addicon.png",
                    width=35,
                    height=35,
                ),
                on_click=lambda e: print("Botão adicionar clicado!"),
                mouse_cursor=ft.MouseCursor.CLICK,
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    page.add(header)
    page.update()