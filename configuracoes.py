import flet as ft

def configuracoes_page(page: ft.Page, on_back, on_change_theme):
    page.controls.clear()
    
    # Cores adaptáveis para a tela de config
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto = "white" if is_dark else "black"
    
    def alternar_tema(e):
        # Se estiver dark, muda para light e vice-versa
        novo_modo = "light" if page.theme_mode == ft.ThemeMode.DARK else "dark"
        on_change_theme(novo_modo)

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_back()),
        title=ft.Text("Configurações", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    # Componente de mudar tema
    btn_tema = ft.Container(
        content=ft.Row(
            [
                ft.Icon(
                    ft.Icons.WB_SUNNY if not is_dark else ft.Icons.NIGHTLIGHT_ROUND, 
                    color="#00bcd4"
                ),
                ft.Text("Tema do Aplicativo", size=16, color=cor_texto, expand=True),
                ft.Switch(
                    value=is_dark,
                    active_color="#00bcd4",
                    on_change=alternar_tema
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=20,
        bgcolor="#0A122A" if is_dark else "#E0E3EE",
        border_radius=15,
    )

    page.add(
        ft.Container( # Usamos o Container para dar o padding com segurança
            content=ft.Column(
                [
                    ft.Text("Aparência", size=20, weight="bold", color=cor_texto),
                    ft.Divider(height=10, color="transparent"),
                    btn_tema,
                    ft.Text(
                        "Alterne entre o modo claro e escuro para melhor visualização.",
                        size=12,
                        color=ft.Colors.BLUE
                    ),
                ],
                spacing=10,
            ),
            padding=20 # O padding fica aqui no Container
        )
    )
    page.update()