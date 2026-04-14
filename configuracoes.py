import flet as ft
from database import salvar_tema_db

def configuracoes_page(page: ft.Page, on_back, user_data): # Adicionei user_data como parâmetro
    page.controls.clear()
    
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto = "white" if is_dark else "black"
    
    def alterar_tema(e):
        # e.control.value já é True ou False (do Switch)
        novo_valor_dark = e.control.value 
        
        # 1. Aplica visualmente no app
        page.theme_mode = ft.ThemeMode.DARK if novo_valor_dark else ft.ThemeMode.LIGHT
        
        # 2. Salva no banco (o database.py vai converter True/False para 1/0)
        user_id = user_data.get('id_user') or user_data.get('id_use')
        if user_id:
            salvar_tema_db(user_id, novo_valor_dark)
        
        # 3. Atualiza a página para refletir as cores
        configuracoes_page(page, on_back, user_data)

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_back()),
        title=ft.Text("Configurações", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    btn_tema = ft.Container(
        content=ft.Row(
            [
                ft.Row([
                    ft.Icon(
                        ft.Icons.WB_SUNNY if not is_dark else ft.Icons.NIGHTLIGHT_ROUND, 
                        color="#00bcd4"
                    ),
                    ft.Text("Tema do Aplicativo", size=16, color=cor_texto),
                ], spacing=10),
                ft.Switch(
                    value=is_dark,
                    active_color="#4CAF50",
                    on_change=alterar_tema
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=20,
        bgcolor="#0A122A" if is_dark else "#E0E3EE",
        border_radius=15,
    )

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Aparência", size=20, weight="bold", color=cor_texto),
                    ft.Divider(height=10, color="transparent"),
                    btn_tema,
                    ft.Text(
                        "Alterne entre o modo claro e escuro para melhor visualização.",
                        size=12,
                        color=ft.Colors.BLUE if not is_dark else ft.Colors.BLUE_200
                    ),
                ],
                spacing=10,
            ),
            padding=20
        )
    )
    page.update()