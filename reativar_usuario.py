import flet as ft
from database import reativar_usuario_db, buscar_usuario_por_nome
from log import write_log

# Deixei o on_theme_change=None para não dar erro se você esquecer de passar no main.py
def reativar_user(page: ft.Page, user_data, on_gerenciar_usuario, on_theme_change=None):
    page.controls.clear()
    
    # --- PADRONIZAÇÃO DE CORES (IDÊNTICO AO SEU PERFIL) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#0b1445" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_destaque = "#08D345" 
    cor_input = "#0A122A" if is_dark else "#F5F7FB"

    # Dados do usuário
    user_id = user_data.get("id_user")
    nome_usuario = user_data.get("nome_user", "Usuário")
    admin_que_desativou = user_data.get("admin_desat")

    txt_senha_admin = ft.TextField(
        label="Senha do Administrador",
        password=True,
        can_reveal_password=True,
        width=300,
        bgcolor=cor_input,
        border_color=cor_borda,
        color=cor_texto_p,
        label_style=ft.TextStyle(color=cor_texto_s),
        focused_border_color=cor_texto_s
    )

    def validar_e_confirmar(e):
        if not txt_senha_admin.value:
            txt_senha_admin.error_text = "⚠️ Digite a senha do administrador!"
            page.update()
            return
        # Esperamos que o campo 'admin_desat' contenha o ID do admin que desativou
        from database import buscar_usuario_por_id
        admin_db = buscar_usuario_por_id(admin_que_desativou)

        if not admin_db:
            txt_senha_admin.error_text = "❌ Admin não encontrado"
            page.update()
            return

        # Só permite reativar se o perfil do responsável for 'admin'
        if str(admin_db.get('perfil','')).lower() != 'admin':
            txt_senha_admin.error_text = "❌ Somente administrador pode reativar"
            page.update()
            return

        if admin_db.get("senha_user") == txt_senha_admin.value:
            if reativar_usuario_db(user_id):
                # registra no log
                write_log('reativar_usuario', user_id=admin_que_desativou, details=f"reativou {user_id}")
                # Primeiro volta para a tela de usuários
                on_gerenciar_usuario()
                # Então mostra o snack_bar na página atual (que agora é a listagem)
                page.snack_bar = ft.SnackBar(ft.Text(f"✅ Usuário {nome_usuario} reativado com sucesso!"), bgcolor="#00b40d")
                page.snack_bar.open = True
                page.update()
        else:
            txt_senha_admin.error_text = "❌ Senha incorreta!"
        page.update()

    # --- APPBAR (ESTILO PERFIL) ---
    page.appbar = ft.AppBar(
        bgcolor=cor_barra, 
        title=ft.Text("Validação", color="white"), 
        center_title=True,
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_gerenciar_usuario()),
        actions=[
            # Só mostra o botão de tema se a função foi passada
            ft.IconButton(
                ft.Icons.LIGHT_MODE if is_dark else ft.Icons.DARK_MODE, 
                icon_color="white", 
                on_click=lambda _: on_theme_change() if on_theme_change else None
            )
        ]
    )

    # --- CONTEÚDO ---
    page.add(
        ft.Container(
            expand=True,
            bgcolor=cor_fundo_tela,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=30,
                        bgcolor=cor_fundo_card,
                        border_radius=20,
                        border=ft.border.all(1, cor_borda),
                        width=350,
                        content=ft.Column([
                            ft.Icon(ft.Icons.LOCK_RESET_ROUNDED, color=cor_texto_s, size=60),
                            ft.Text("Reativar Conta", size=20, weight="bold", color=cor_texto_p),
                            ft.Text(f"Usuário: {nome_usuario}", color=cor_texto_p, size=12),
                            ft.Text(f"Admin: {admin_que_desativou}", color=cor_texto_s, weight="bold", size=14),
                            ft.Container(height=5),
                            txt_senha_admin,
                            ft.Container(height=5),
                            ft.ElevatedButton(
                                "CONFIRMAR",
                                bgcolor=cor_destaque,
                                color=ft.Colors.WHITE,
                                width=250,
                                height=45,
                                on_click=validar_e_confirmar
                            ),
                        ], horizontal_alignment="center", spacing=10)
                    )
                ]
            )
        )
    )
    page.update()