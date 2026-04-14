import flet as ft
from datetime import datetime
from database import desativar_usuario_db

def tela_desativar_usuario(page: ft.Page, user_data, on_voltar):
    page.controls.clear()
    
    # DADOS DO ADMINISTRADOR (QUEM ESTÁ LOGADO)
    # Pegamos do page.user_data que você configurou no main.py
    admin_data = page.user_data 
    
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_input_fundo = "#0A122A" if is_dark else "#F0F2F5"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_alerta = "#FF4444"

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_NEW,
            icon_color="white",
            on_click=lambda _: on_voltar()
        ),
        title=ft.Text("Confirmar Desativação", size=20, weight="bold", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    def estilo_input(label, hint="", password=False, multiline=False):
        input_field = ft.TextField(
            hint_text=hint,
            border=ft.InputBorder.NONE,
            content_padding=15,
            password=password,
            can_reveal_password=password,
            multiline=multiline,
            min_lines=3 if multiline else 1,
            text_style=ft.TextStyle(color=cor_texto),
            expand=True,
        )
        container = ft.Column([
            ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=input_field,
                bgcolor=cor_input_fundo,
                border=ft.border.all(1, cor_borda),
                border_radius=10,
                padding=ft.padding.only(right=10) if not multiline else 10,
            )
        ], spacing=5)
        return container, input_field

    motivo_container, motivo_input = estilo_input("MOTIVO DA DESATIVAÇÃO", hint="Ex: Solicitação do colaborador...", multiline=True)
    
    # MUDANÇA AQUI: Agora pede a SUA senha de acesso
    senha_container, senha_input = estilo_input("SUA SENHA DE ADMINISTRADOR", hint="Digite sua senha para confirmar", password=True)

    info_user = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.PERSON_OFF, color=cor_alerta, size=30),
            ft.Column([
                ft.Text(f"Desativando: {user_data.get('nome_user', 'N/A')}", size=16, weight="bold", color=cor_texto),
                ft.Text(f"ID do Alvo: {user_data.get('id_user', 'N/A')}", size=12, color=ft.Colors.GREY_500),
            ], spacing=0)
        ]),
        padding=10,
        bgcolor=ft.Colors.with_opacity(0.05, cor_alerta),
        border_radius=10,
    )

    def confirmar_desativacao(e):
        # 1. Verifica se os campos estão vazios
        if not motivo_input.value or not senha_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha o motivo e sua senha!"), bgcolor="orange")
            page.snack_bar.open = True
            page.update()
            return

        # 2. VALIDAÇÃO DE SEGURANÇA: Compara a senha digitada com a senha do admin logado
        # Buscamos 'senha_user' que veio do banco no login
        senha_correta = admin_data.get('senha_user')

        if senha_input.value != senha_correta:
            page.snack_bar = ft.SnackBar(ft.Text("Senha de administrador incorreta!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # 3. Se a senha estiver certa, desativa no banco
        # Removi o argumento 'senha_protocolo' já que agora usamos a do admin
        sucesso = desativar_usuario_db(
            id_usuario=user_data['id_user'],
            motivo=motivo_input.value,
            admin_nome=admin_data.get('nome_user')
        )

        if sucesso:
            page.snack_bar = ft.SnackBar(ft.Text(f"Usuário {user_data['nome_user']} desativado!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()
            import time
            time.sleep(1)
            on_voltar()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao desativar no banco de dados!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    form_content = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        width=400,
        controls=[
            ft.Divider(height=5, color="transparent"),
            info_user,
            ft.Divider(height=10, color="transparent"),
            motivo_container,
            senha_container,
            ft.Text(f"Operação realizada por: {admin_data.get('nome_user')}", size=11, color=ft.Colors.GREY_500),
            ft.Divider(height=20, color="transparent"),
            ft.ElevatedButton(
                "Confirmar Desativação",
                on_click=confirmar_desativacao,
                width=400,
                height=50,
                style=ft.ButtonStyle(bgcolor=cor_alerta, color="white", shape=ft.RoundedRectangleBorder(radius=10))
            ),
            ft.TextButton("Cancelar", on_click=lambda _: on_voltar(), width=400),
        ]
    )

    page.add(ft.Row([form_content], alignment=ft.MainAxisAlignment.CENTER))
    page.update()