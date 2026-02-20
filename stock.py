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
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    search_field = ft.TextField(
        hint_text="Buscar...",
        prefix_icon=ft.Icons.SEARCH, # Usando o Icons corrigido
        border_radius=15,
        width=400,          # Defina uma largura fixa para teste
        height=50,          # Altura para garantir presença física
        bgcolor="#0d1626",  # Cor de fundo azulada da imagem
        border_color="#1e293b", # Cor da borda visível
        hint_style=ft.TextStyle(color="grey"),
        content_padding=10, # Espaçamento interno
    )

    page.add(
        header,
        ft.Text("PRODUTO", size=12, color="grey", weight="bold"), # Label igual à imagem
        search_field
        )

    page.add(header)

    def trocar_aba(e):
        index = nav.selected_index

        if index == 0:
            on_logout()  # 👈 volta para Home

        elif index == 1:
            pass  # já está no estoque

        elif index == 2:
            print("Equipe")

        elif index == 3:
            print("Perfil")

    nav = ft.NavigationBar(
        bgcolor="#0b1445",
        selected_index=1,  # Estoque está ativo
        on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label=""
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.INVENTORY_2_OUTLINED,
                selected_icon=ft.Icons.INVENTORY_2,
                label=""
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.GROUP_OUTLINED,
                selected_icon=ft.Icons.GROUP,
                label=""
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON_OUTLINE,
                selected_icon=ft.Icons.PERSON,
                label=""
            ),
        ]
    )

    page.navigation_bar = ft.Container(
        content=nav,
        margin=ft.margin.only(left=25, right=25, bottom=30),
        border_radius=40, 
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK)
        )
    )
    
    page.update()