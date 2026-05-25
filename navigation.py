import flet as ft


def build_navigation_bar(
    page: ft.Page,
    selected_label: str,
    is_admin: bool,
    callbacks: dict,
    bgcolor: str = None,
    indicator_color: str = None,
):
    """Cria uma barra de navegação com layout uniforme para todas as telas."""
    bgcolor = bgcolor or "#050f44"
    indicator_color = indicator_color or "#1679f2"

    destinos = [
        ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
    ]

    if is_admin:
        destinos.extend([
            ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Logs"),
        ])
    else:
        destinos.extend([
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Logs"),
        ])

    destinos.append(ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"))

    def _noop(*args, **kwargs):
        return None

    def trocar_aba(e):
        label = destinos[e.control.selected_index].label
        if label == "Inicial":
            callbacks.get("on_home", _noop)()
        elif label == "Vendas":
            callbacks.get("on_vendas", _noop)()
        elif label == "Estoque":
            callbacks.get("on_stock", _noop)()
        elif label == "Usuários":
            callbacks.get("on_users", _noop)()
        elif label == "Logs":
            callbacks.get("on_log", _noop)()
        elif label == "Perfil":
            callbacks.get("on_perfil", _noop)()

    selected_index = 0
    for i, destino in enumerate(destinos):
        if destino.label == selected_label:
            selected_index = i
            break

    page.navigation_bar = ft.Container(
        content=ft.NavigationBar(
            bgcolor=bgcolor,
            selected_index=selected_index,
            on_change=trocar_aba,
            indicator_color=indicator_color,
            destinations=destinos,
        ),
        margin=ft.margin.only(left=25, right=25, bottom=20),
        border_radius=40,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )
