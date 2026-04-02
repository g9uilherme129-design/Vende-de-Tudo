import flet as ft
from datetime import datetime

def tela_desativar_usuario(page: ft.Page, user_data, on_voltar):
    page.controls.clear()
    page.title = "Desativar Usuário"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Lógica de cores adaptáveis (mesmo padrão da edição)
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_input_fundo = "#0A122A" if is_dark else "#F0F2F5"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_alerta = "#FF4444"

    # AppBar padronizado
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_NEW,
            icon_color="white",
            on_click=lambda _: on_voltar()
        ),
        title=ft.Text("Desativar Usuário", size=20, weight="bold", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    # Função de estilo para manter o padrão visual
    def estilo_input(label, hint="", password=False, multiline=False):
        input_field = ft.TextField(
            hint_text=hint,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_600),
            border=ft.InputBorder.NONE,
            content_padding=15,
            password=password,
            can_reveal_password=password,
            multiline=multiline,
            min_lines=3 if multiline else 1,
            text_style=ft.TextStyle(color=cor_texto),
            expand=True,
        )
        
        container = ft.Column(
            [
                ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=input_field,
                    bgcolor=cor_input_fundo,
                    border=ft.border.all(1, cor_borda),
                    border_radius=10,
                    padding=ft.padding.only(right=10) if not multiline else 10,
                )
            ],
            spacing=5,
        )
        return container, input_field

    # Criando os campos com o novo estilo
    motivo_container, motivo_input = estilo_input(
        "MOTIVO DA DESATIVAÇÃO", 
        hint="Ex: Solicitação do colaborador...", 
        multiline=True
    )
    
    senha_container, senha_input = estilo_input(
        "DEFINIR SENHA DE PROTOCOLO", 
        hint="Senha para futura reativação", 
        password=True
    )

    # Informações do Usuário (Visualização)
    info_user = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.PERSON_OFF, color=cor_alerta, size=30),
                ft.Column([
                    ft.Text(f"Usuário: {user_data.get('nome', 'N/A')}", size=16, weight="bold", color=cor_texto),
                    ft.Text(f"Código: {user_data.get('codigo', 'N/A')}", size=12, color=ft.Colors.GREY_500),
                ], spacing=0)
            ]
        ),
        padding=10,
        bgcolor=ft.Colors.with_opacity(0.05, cor_alerta),
        border_radius=10,
        border=ft.border.all(1, ft.Colors.with_opacity(0.2, cor_alerta))
    )

    def confirmar_desativacao(e):
        if not motivo_input.value or not senha_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos!"))
            page.snack_bar.open = True
            page.update()
            return
        
        print(f"Usuário {user_data['codigo']} desativado.")
        on_voltar()

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Divider(height=5, color="transparent"),
                info_user,
                ft.Divider(height=10, color="transparent"),
                motivo_container,
                senha_container,
                ft.Text(
                    f"Data do Protocolo: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                    size=11, color=ft.Colors.GREY_500
                ),
                ft.Divider(height=20, color="transparent"),
                
                # Botão de Ação Crítica
                ft.ElevatedButton(
                    "Confirmar Desativação",
                    on_click=confirmar_desativacao,
                    width=250,
                    style=ft.ButtonStyle(
                        bgcolor=cor_alerta,
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=10),
                    )
                ),
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda _: on_voltar(),
                    style=ft.ButtonStyle(color=ft.Colors.GREY_600)
                ),
                
                # Alerta de segurança no rodapé
                ft.Container(
                    content=ft.Text(
                        "Atenção: A senha definida será necessária para reativar este usuário no futuro.",
                        size=11, color="orange", italic=True, text_align=ft.TextAlign.CENTER
                    ),
                    padding=20
                )
            ],
            spacing=10
        )
    )
    page.update()