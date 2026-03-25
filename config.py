import flet as ft

def configuracoes_page(page: ft.Page, on_perfil):
    page.controls.clear()
    
    # Função interna para atualizar o tema e salvar a preferência
    def alterar_cor(cor):
        page.theme = ft.Theme(color_scheme_seed=cor)
        page.update()

    def alternar_modo(e):
        page.theme_mode = ft.ThemeMode.LIGHT if e.control.value else ft.ThemeMode.DARK
        page.update()

    # Títulos e Seções
    header = ft.Text("Configurações de Visual", size=24, weight="bold")

    # Switch para Tema Claro/Escuro
    modo_switch = ft.ListTile(
        leading=ft.Icon(ft.Icons.BRIGHTNESS_4),
        title=ft.Text("Modo Claro"),
        subtitle=ft.Text("Alternar entre tema claro e escuro"),
        trailing=ft.Switch(
            value=page.theme_mode == ft.ThemeMode.LIGHT,
            on_change=alternar_modo
        ),
    )

    # Cores de Sub-tema
    cores = [
        ("Azul Padrão", ft.Colors.BLUE),
        ("Verde Natureza", ft.Colors.GREEN),
        ("Vermelho Alerta", ft.Colors.RED),
        ("Roxo Moderno", ft.Colors.PURPLE),
        ("Laranja Energia", ft.Colors.ORANGE),
    ]

    # Criando os botões de cores usando Grid Responsivo
    botoes_cores = []
    for nome, cor in cores:
        botoes_cores.append(
            ft.Container(
                content=ft.Column([
                    ft.Container(bgcolor=cor, width=40, height=40, border_radius=20),
                    ft.Text(nome, size=10, text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=10,
                border_radius=15,
                bgcolor="#0A122A" if page.theme_mode == ft.ThemeMode.DARK else "#F0F2F5",
                on_click=lambda _, c=cor: alterar_cor(c),
                col={"xs": 4, "sm": 2.4} # 3 por linha no celular, 5 no PC
            )
        )

    layout_cores = ft.ResponsiveRow(controls=botoes_cores, spacing=10)

    # Conteúdo da Página
    page.add(
        ft.Column([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: on_perfil()),
            header,
            ft.Divider(height=20, color="transparent"),
            ft.Text("TEMA PRINCIPAL", size=12, weight="bold", color="teal"),
            modo_switch,
            ft.Divider(height=20, color="transparent"),
            ft.Text("CORES DO SISTEMA", size=12, weight="bold", color="teal"),
            layout_cores,
        ], scroll=ft.ScrollMode.AUTO)
    )
    page.update()