import flet as ft
from database import buscar_usuario_por_id, atualizar_usuario_db, Validar_senha_atual_db
from log import write_log

def editar_usuario(page: ft.Page, on_users, id_usuario):
    page.controls.clear()
    page.scroll = ft.ScrollMode.AUTO

    # --- PADRONIZAÇÃO DE CORES ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#0b1445" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_input = "#0A122A" if is_dark else "#F5F7FB"

    # Busca os dados do usuário
    u = buscar_usuario_por_id(id_usuario)
    if not u:
        on_users()
        page.snack_bar = ft.SnackBar(ft.Text("Erro: Usuário não encontrado!"), bgcolor="red")
        page.snack_bar.open = True
        return

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color="white",
            on_click=lambda _: on_users()
        ),
        title=ft.Text(f"Editar Usuário #{id_usuario}", size=20, weight="bold", color="white"),
        bgcolor=cor_barra,
        center_title=True,
    )

    # --- FUNÇÃO AUXILIAR DE ESTILO ---
    def estilo_input(label, hint="", value="", password=False, keyboard_type=ft.KeyboardType.TEXT, limite=None):
        input_field = ft.TextField(
            value=str(value),
            hint_text=hint,
            password=password,
            can_reveal_password=password,
            border=ft.InputBorder.NONE,
            content_padding=15,
            text_style=ft.TextStyle(color=cor_texto_p),
            expand=True,
            keyboard_type=keyboard_type,
            max_length=limite,
            cursor_color=cor_texto_s,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
        )
        
        container = ft.Column(
            [
                ft.Text(f"  {label}", size=12, color=cor_texto_s, weight="bold"),
                ft.Container(
                    content=input_field,
                    bgcolor=cor_input,
                    border=ft.border.all(1, cor_borda),
                    border_radius=12,
                    padding=ft.padding.only(right=10, bottom=5),
                )
            ],
            spacing=5,
        )
        return container, input_field

    # --- CAMPOS COM DADOS CARREGADOS ---
    nome_c, nome_in = estilo_input("NOME COMPLETO", value=u.get('nome_user', ''), limite=100)
    cpf_c, cpf_in = estilo_input("CPF (Apenas números)", value=u.get('cpf', ''), keyboard_type=ft.KeyboardType.NUMBER, limite=11)
    email_c, email_in = estilo_input("E-MAIL", value=u.get('email_user', ''), keyboard_type=ft.KeyboardType.EMAIL, limite=100)
    
    salario_val = f"{float(u.get('salario', 0)):.2f}".replace(".", ",")
    salario_c, salario_in = estilo_input("SALÁRIO BASE", value=salario_val, keyboard_type=ft.KeyboardType.NUMBER, limite=15)
    salario_in.prefix_text = "R$ "

    perfil_dropdown = ft.Dropdown(
        value=u.get('perfil', 'vendedor'),
        options=[
            ft.dropdown.Option("admin", "ADMINISTRADOR"),
            ft.dropdown.Option("vendedor", "VENDEDOR"),
        ],
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(color=cor_texto_p),
        content_padding=ft.padding.only(left=15),
        expand=True,
    )

    perfil_c = ft.Column(
        [
            ft.Text("  PERFIL / CARGO", size=12, color=cor_texto_s, weight="bold"),
            ft.Container(
                content=perfil_dropdown,
                bgcolor=cor_input,
                border=ft.border.all(1, cor_borda),
                border_radius=12,
                height=55,
            )
        ],
        spacing=5,
    )

    # Campos de Segurança
    senha_atual_c, senha_atual_in = estilo_input("CONFIRMAR SENHA ATUAL", password=True)
    senha_c, senha_in = estilo_input("NOVA SENHA (Opcional)", password=True, limite=32)
    senha_conf_c, senha_conf_in = estilo_input("CONFIRMAR NOVA SENHA", password=True)

    def salvar_edicao(e):
        nova_senha = senha_in.value.strip() if senha_in.value else ""
        
        # Lógica de validação de senha
        if nova_senha:
            if not senha_atual_in.value:
                page.snack_bar = ft.SnackBar(ft.Text("Digite a senha atual para autorizar a mudança!"), bgcolor="orange")
                page.snack_bar.open = True
                page.update()
                return
            
            if nova_senha != senha_conf_in.value:
                page.snack_bar = ft.SnackBar(ft.Text("A nova senha e a confirmação não coincidem!"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return
            
            if not Validar_senha_atual_db(id_usuario, senha_atual_in.value):
                page.snack_bar = ft.SnackBar(ft.Text("Senha atual incorreta!"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return

        # CHAMADA CORRIGIDA: id_user em vez de id_usuario para bater com o database.py
        sucesso, msg = atualizar_usuario_db(
            id_user=id_usuario, 
            nome=nome_in.value,
            cpf=cpf_in.value,
            email=email_in.value,
            perfil=perfil_dropdown.value,
            salario=salario_in.value.replace(",", "."),
            senha=nova_senha if nova_senha else None
        )
        
        if sucesso:
            on_users()
            page.snack_bar = ft.SnackBar(ft.Text("Usuário atualizado com sucesso!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()
            write_log('atualizar_usuario', user_id=id_usuario, details=f"nome:{nome_in.value} perfil:{perfil_dropdown.value}")
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {msg}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    # Layout do Formulário
    form_content = ft.Column(
        [
            nome_c,
            cpf_c,
            email_c,
            salario_c,
            perfil_c,
            ft.Divider(height=20, color=cor_borda),
            ft.Text("ALTERAR SEGURANÇA", size=12, color=cor_texto_s, weight="bold"),
            senha_atual_c,
            senha_c,
            senha_conf_c,
            ft.Container(height=10),
            ft.ElevatedButton(
                "SALVAR ALTERAÇÕES",
                on_click=salvar_edicao,
                width=400,
                height=55,
                style=ft.ButtonStyle(
                    bgcolor=cor_texto_s,
                    color="white",
                    shape=ft.RoundedRectangleBorder(radius=12),
                )
            ),
        ],
        spacing=18,
        width=400,
    )

    page.add(
        ft.Container(
            expand=True,
            bgcolor=cor_fundo_tela,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=form_content,
                                padding=25,
                                bgcolor=cor_fundo_card,
                                border_radius=20,
                                border=ft.border.all(1, cor_borda)
                            )
                        ],
                        alignment="center" 
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                alignment="center"
            )
        )
    )
    
    page.update()