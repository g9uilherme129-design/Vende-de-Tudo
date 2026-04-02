import flet as ft
from database import cadastrar_usuario_db

def novo_usuario(page: ft.Page, on_users):
    page.controls.clear()
    page.padding = 20

    # Lógica de cores adaptáveis
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_input = "#0A122A" if is_dark else "#FFFFFF"
    cor_borda_input = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_input = "white" if is_dark else "black"
    cor_label = ft.Colors.TEAL_700 if is_dark else ft.Colors.TEAL_900

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color="white",
            on_click=lambda _: on_users()
        ),
        title=ft.Text("Novo Usuário", size=20, weight="bold", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    def estilo_input(label, hint="", password=False, col=None):
        input_field = ft.TextField(
            hint_text=hint,
            password=password,
            can_reveal_password=password,
            border=ft.InputBorder.NONE,
            content_padding=15,
            text_style=ft.TextStyle(color=cor_texto_input),
            expand=True,
        )
        
        container = ft.Column(
            [
                ft.Text(label, size=11, color=cor_label, weight="bold"),
                ft.Container(
                    content=input_field,
                    bgcolor=cor_fundo_input,
                    border=ft.border.all(1, cor_borda_input),
                    border_radius=10,
                    padding=ft.padding.only(right=10),
                )
            ],
            spacing=5,
            col=col 
        )
        return container, input_field

    # --- CAMPOS DO FORMULÁRIO ---
    nome_c, nome_in = estilo_input("NOME COMPLETO", hint="Ex: Neymar Jr", col=12)
    cpf_c, cpf_in = estilo_input("CPF (Apenas números)", hint="12345678900", col=12)
    email_c, email_in = estilo_input("E-MAIL", hint="usuario@email.com", col=12)
    senha_c, senha_in = estilo_input("SENHA", hint="******", password=True, col=12)
    
    # Perfil (Cargo)
    perfil_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("admin", "ADMINISTRADOR"),
            ft.dropdown.Option("vendedor", "VENDEDOR"),
        ],
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(color=cor_texto_input),
        content_padding=ft.padding.only(left=15),
    )

    perfil_c = ft.Column(
        [
            ft.Text("PERFIL / CARGO", size=11, color=cor_label, weight="bold"),
            ft.Container(
                content=perfil_dropdown,
                bgcolor=cor_fundo_input,
                border=ft.border.all(1, cor_borda_input),
                border_radius=10,
                height=55,
            )
        ],
        spacing=5,
        col=12 
    )

    def salvar_usuario(e):
        if not nome_in.value or not email_in.value or not perfil_dropdown.value:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        try:
            cadastrar_usuario_db(
                nome=nome_in.value,
                cpf=cpf_in.value,
                email=email_in.value,
                senha=senha_in.value,
                perfil=perfil_dropdown.value
            )
            page.snack_bar = ft.SnackBar(ft.Text("Usuário cadastrado no MySQL!"), bgcolor="green")
            page.snack_bar.open = True
            on_users() # Volta para a lista
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    layout_campos = ft.ResponsiveRow(
        controls=[nome_c, cpf_c, email_c, senha_c, perfil_c],
        spacing=15,
        run_spacing=15,
    )

    page.add(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Divider(height=10, color="transparent"),
                layout_campos,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Cadastrar Usuário",
                    on_click=salvar_usuario,
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor="#1B4F9C",
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=12),
                    )
                ),
                ft.Container(height=40)
            ],
            spacing=10
        )
    )
    page.update()