import flet as ft
from datetime import datetime
from database import desativar_usuario_db
from log import write_log

import flet as ft
from datetime import datetime
import time # Certifique-se de que o import está aqui
from database import desativar_usuario_db

def tela_desativar_usuario(page: ft.Page, user_data, on_voltar):
    # SEGURANÇA: Se não houver dados do admin logado, define um dicionário vazio para não quebrar
    admin_data = getattr(page, "user_data", {}) 
    if not admin_data:
        print("Aviso: page.user_data não encontrado. Verifique o login.")
        # Opcional: on_voltar() se o admin não estiver logado

    page.controls.clear()
    page.padding = 0
    
    # --- PADRONIZAÇÃO DE CORES ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D" 
    cor_barra = "#0b1445" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_input_bg = "#0A122A" if is_dark else "#F5F7FB"
    cor_alerta = "#FF4444"
    cor_secundaria =  "#1679f2" if is_dark else "#DA7D7D"

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_NEW,
            icon_color="white",
            on_click=lambda _: on_voltar()
        ),
        title=ft.Text("Confirmar Desativação", size=20, weight="bold", color="white"),
        bgcolor=cor_barra,
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
            text_style=ft.TextStyle(color=cor_texto_p),
            hint_style=ft.TextStyle(color=cor_secundaria),
            expand=True,
            cursor_color=cor_texto_s,
        )
        container = ft.Column([
            ft.Text(f"  {label}", size=11, color=cor_texto_s, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=input_field,
                bgcolor=cor_input_bg,
                border=ft.border.all(1, cor_borda),
                border_radius=10,
                padding=ft.padding.only(right=10) if not multiline else 10,
            )
        ], spacing=5)
        return container, input_field

    motivo_container, motivo_input = estilo_input("MOTIVO DA DESATIVAÇÃO", hint="Ex: Solicitação do colaborador...", multiline=True)
    senha_container, senha_input = estilo_input("SUA SENHA DE ADMINISTRADOR", hint="Confirme sua identidade", password=True)

    info_user = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.PERSON_OFF, color=cor_alerta, size=34),
            ft.Column([
                ft.Text(f"Desativando: {user_data.get('nome_user', 'N/A')}", size=16, weight="bold", color=cor_texto_p),
                ft.Text(f"ID: {user_data.get('id_user', 'N/A')}", size=12, color=cor_secundaria),
            ], spacing=0)
        ]),
        padding=20,
        bgcolor=ft.Colors.with_opacity(0.1, cor_alerta),
        border=ft.border.all(1, ft.Colors.with_opacity(0.2, cor_alerta)),
        border_radius=15,
    )

    def confirmar_desativacao(e):
        if not motivo_input.value or not senha_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Preencha o motivo e sua senha!"), bgcolor="#FF9800")
            page.snack_bar.open = True
            page.update()
            return

        senha_correta = admin_data.get('senha_user')
        if senha_input.value != senha_correta:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Senha de administrador incorreta!"), bgcolor="#FF4444")
            page.snack_bar.open = True
            page.update()
            return

        sucesso = desativar_usuario_db(
            id_usuario=user_data['id_user'],
            motivo=motivo_input.value,
            admin_id=admin_data.get('id_user')
        )

        if sucesso:
            admin_id = admin_data.get('id_user') if admin_data else None
            write_log('desativar_usuario', user_id=admin_id, details=f"desativou {user_data.get('id_user')} motivo:{motivo_input.value}")
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ Usuário {user_data.get('nome_user', 'N/A')} desativado com sucesso!"), bgcolor="#00b40d")
            page.snack_bar.open = True
            page.update()
            import time
            time.sleep(1)
            on_voltar()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Erro ao processar desativação!"), bgcolor="#FF4444")
            page.snack_bar.open = True
            page.update()

    # --- LAYOUT FINAL ---
    page.add(
        ft.Container(
            expand=True,
            bgcolor=cor_fundo_tela,
            content=ft.Column([
                ft.Container(
                    width=450,
                    padding=30,
                    bgcolor=cor_fundo_card if not is_dark else "transparent",
                    border_radius=20,
                    content=ft.Column([
                        ft.Icon(ft.Icons.GPP_MAYBE, color=cor_alerta, size=50),
                        ft.Text("Atenção!", size=24, weight="bold", color=cor_texto_p),
                        ft.Text(
                            "Esta ação impedirá o acesso do usuário ao sistema imediatamente.",
                            size=13, color=cor_secundaria, text_align=ft.TextAlign.CENTER
                        ),
                        ft.Divider(height=30, color="transparent"),
                        
                        info_user,
                        
                        ft.Divider(height=20, color="transparent"),
                        motivo_container,
                        senha_container,
                        
                        ft.Text(
                            f"Autorizado por (ID): {admin_data.get('id_user')}", 
                            size=11, color=cor_secundaria, italic=True
                        ),
                        
                        ft.Divider(height=30, color="transparent"),
                        
                        ft.ElevatedButton(
                            "CONFIRMAR DESATIVAÇÃO",
                            on_click=confirmar_desativacao,
                            width=400,
                            height=55,
                            style=ft.ButtonStyle(
                                bgcolor=cor_alerta, 
                                color="white", 
                                shape=ft.RoundedRectangleBorder(radius=12),
                                elevation=5
                            )
                        ),
                        ft.TextButton(
                            "Cancelar e Voltar", 
                            on_click=lambda _: on_voltar(), 
                            # AQUI ESTAVA O ERRO: Ajustado para usar style
                            style=ft.ButtonStyle(color=cor_secundaria) 
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    )
    page.update()