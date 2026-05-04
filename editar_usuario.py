import flet as ft
from database import buscar_usuario_por_id, atualizar_usuario_db

def editar_usuario(page: ft.Page, on_users, id_usuario):
    page.controls.clear()
    
    u = buscar_usuario_por_id(id_usuario)
    if not u:
        page.snack_bar = ft.SnackBar(ft.Text("Erro: Usuário não encontrado!"), bgcolor="red")
        page.snack_bar.open = True
        on_users()
        return

    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_input_fundo = "#0A122A" if is_dark else "#F0F2F5"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"

    page.appbar = ft.AppBar(
        leading=ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_users()),
        title=ft.Text(f"Editar Usuário #{id_usuario}", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    # --- FUNÇÃO DE ESTILO COM LIMITE ---
    def estilo_input(label, value="", col=None, is_password=False, limite=None):
        input_field = ft.TextField(
            value=str(value),
            border=ft.InputBorder.NONE,
            content_padding=15,
            text_style=ft.TextStyle(color=cor_texto),
            expand=True,
            password=is_password,
            can_reveal_password=is_password,
            max_length=limite, # Define o limite
        )
        return ft.Column([
            ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight="bold"),
            ft.Container(
                content=input_field, 
                bgcolor=cor_input_fundo, 
                border=ft.border.all(1, cor_borda), 
                border_radius=10,
                padding=ft.padding.only(bottom=5) # Espaço para o contador
            )
        ], col=col), input_field

    # --- CAMPOS COM LIMITES ---
    nome_c, nome_in = estilo_input("NOME COMPLETO", u.get('nome_user', ''), {"sm": 12, "md": 6}, limite=100)
    cpf_c, cpf_in = estilo_input("CPF", u.get('cpf', ''), {"sm": 12, "md": 6}, limite=11)
    email_c, email_in = estilo_input("E-MAIL", u.get('email_user', ''), {"sm": 12, "md": 8}, limite=100)
    salario_c, salario_in = estilo_input("SALÁRIO", f"{float(u.get('salario', 0)):.2f}", {"sm": 12, "md": 4}, limite=15)
    senha_c, senha_in = estilo_input("NOVA SENHA (OPCIONAL)", "", {"sm": 12, "md": 6}, True, limite=32)

    perfil_dropdown = ft.Dropdown(
        value=u.get('perfil', 'vendedor'),
        options=[ft.dropdown.Option("admin", "ADMINISTRADOR"), ft.dropdown.Option("vendedor", "VENDEDOR")],
        border=ft.InputBorder.NONE,
    )
    perfil_c = ft.Column([
        ft.Text("PERFIL", size=11, color=ft.Colors.TEAL_700, weight="bold"),
        ft.Container(content=perfil_dropdown, bgcolor=cor_input_fundo, border=ft.border.all(1, cor_borda), border_radius=10, height=55)
    ], col={"sm": 12, "md": 6})

    def salvar(e):
        sucesso, msg = atualizar_usuario_db(
            id_usuario, nome_in.value, cpf_in.value, email_in.value, 
            perfil_dropdown.value, salario_in.value.replace(",", "."), senha_in.value
        )
        page.snack_bar = ft.SnackBar(ft.Text("Salvo!" if sucesso else msg), bgcolor="green" if sucesso else "red")
        page.snack_bar.open = True
        if sucesso: on_users()
        page.update()

    page.add(
        ft.Container(
            padding=20, 
            content=ft.Column([
                ft.ResponsiveRow([nome_c, cpf_c, email_c, salario_c, perfil_c, senha_c]),
                ft.Container(height=10),
                ft.ElevatedButton(
                    "SALVAR ALTERAÇÕES", 
                    on_click=salvar, 
                    width=400, 
                    height=55,
                    style=ft.ButtonStyle(
                        bgcolor="#1B4F9C",
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                )
            ], horizontal_alignment="center", scroll=ft.ScrollMode.AUTO)
        )
    )
    page.update()