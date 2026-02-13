import flet as ft

def main(page: ft.Page):
    page.title = "Tela de Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#f0f2f5" # Cor de fundo da página (cinza claro)

    # Este é o Container que ficará atrás de tudo
    login_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.CircleAvatar(
                    foreground_image_src="https://sua-imagem.png", # Ou use ft.Icon(ft.icons.PERSON, size=50)
                    radius=50,
                    bgcolor=ft.Colors.BLUE,
                ),
                ft.Text("Bem-vindo(a)!", size=25, weight=ft.FontWeight.BOLD),
                
                ft.TextField(label="Usuário", border_radius=10, bgcolor=ft.Colors.BLUE_400),
                ft.TextField(label="Senha", password=True, can_reveal_password=True, border_radius=10, bgcolor=ft.Colors.BLUE_400),
                
                ft.ElevatedButton("Entrar", width=150),
                ft.TextButton("Esqueci minha senha"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        # PROPRIEDADES DO CONTAINER (O "CARTÃO" ATRÁS)
        bgcolor=ft.Colors.WHITE,
        padding=40,
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        ),
        width=400, # Largura fixa do container
    )

    page.add(login_container)

ft.app(target=main)