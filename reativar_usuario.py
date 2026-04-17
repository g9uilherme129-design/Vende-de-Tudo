import flet as ft
from database import reativar_usuario_db, buscar_usuario_por_nome

def reativar_user(page: ft.Page, user_data, on_gerenciar_usuario):
    page.controls.clear()
    
    # Dados do usuário alvo (o que será reativado)
    user_id = user_data.get("id_user")
    nome_usuario = user_data.get("nome_user", "Usuário")
    
    # O banco guardou quem desativou (admin_desat)
    # Precisamos do ID ou nome desse admin para validar a senha
    admin_que_desativou = user_data.get("admin_desat") 

    # Campo de senha para o admin digitar
    txt_senha_admin = ft.TextField(
        label="Senha do Administrador",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=ft.Colors.GREEN
    )

    def validar_e_confirmar(e):
        if not txt_senha_admin.value:
            txt_senha_admin.error_text = "Por favor, digite a senha!"
            page.update()
            return

        # 2. Busca o administrador no banco de dados
        admin_db = buscar_usuario_por_nome(admin_que_desativou)

        if admin_db:
            if admin_db.get("senha_user") == txt_senha_admin.value:
                sucesso = reativar_usuario_db(user_id)
                
                if sucesso:
                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"Usuário {nome_usuario} reativado com sucesso!"),
                        bgcolor=ft.Colors.GREEN_700
                    )
                    page.snack_bar.open = True
                    # Volta para a tela de gerenciamento
                    on_gerenciar_usuario()
                else:
                    txt_senha_admin.error_text = "Erro crítico ao atualizar o banco!"
            else:
                txt_senha_admin.error_text = "Senha de administrador incorreta!"
        else:
            # Agora ele vai encontrar o admin pelo nome!
            txt_senha_admin.error_text = f"Erro: Admin '{admin_que_desativou}' não encontrado."
        
        page.update()

    # --- Interface ---
    page.add(
        ft.Container(
            alignment=ft.Alignment(0, 0),
            expand=True,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.LOCK_RESET_ROUNDED, color=ft.Colors.GREEN, size=80),
                    ft.Text("Validação de Segurança", size=24, weight="bold"),
                    ft.Text(
                        f"Para reativar {nome_usuario}, digite a senha do administrador que realizou a desativação ({admin_que_desativou}):",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    txt_senha_admin,
                    ft.Container(height=10),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.TextButton("Cancelar", on_click=lambda _: on_gerenciar_usuario()),
                            ft.ElevatedButton(
                                "Confirmar e Reativar",
                                bgcolor=ft.Colors.GREEN,
                                color=ft.Colors.WHITE,
                                on_click=validar_e_confirmar
                            ),
                        ]
                    )
                ]
            )
        )
    )
    page.update()