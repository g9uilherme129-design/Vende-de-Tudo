import flet as ft
from database import buscar_usuario_por_id, atualizar_usuario_db

def editar_usuario(page: ft.Page, on_users, id_usuario):
    page.controls.clear()
    
    # Busca dados reais do banco
    u = buscar_usuario_por_id(id_usuario)
    
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_input_fundo = "#0A122A" if is_dark else "#F0F2F5"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_NEW,
            icon_color="white",
            on_click=lambda _: on_users()
        ),
        title=ft.Text(f"Editar Usuário #{id_usuario}", size=20, weight="bold", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    def estilo_input(label, value="", read_only=False, col=None):
        input_field = ft.TextField(
            value=str(value),
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color=cor_texto),
            expand=True,
        )
        container = ft.Column([
            ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight="bold"),
            ft.Container(
                content=input_field, bgcolor=cor_input_fundo,
                border=ft.border.all(1, cor_borda), border_radius=10,
                padding=ft.padding.only(right=10),
            )
        ], spacing=5, col=col)
        return container, input_field

    # Campos preenchidos com dados do MySQL
    nome_c, nome_in = estilo_input("NOME COMPLETO", value=u['nome_user'], col=12)
    cpf_c, cpf_in = estilo_input("CPF", value=u['cpf'], col=12)
    email_c, email_in = estilo_input("E-MAIL", value=u['email_user'], col=12)

    # Dropdown de Perfil
    perfil_dropdown = ft.Dropdown(
        value=u['perfil'],
        options=[
            ft.dropdown.Option("admin", "ADMINISTRADOR"),
            ft.dropdown.Option("vendedor", "VENDEDOR"),
        ],
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(color=cor_texto),
        content_padding=ft.padding.only(left=15),
    )

    perfil_c = ft.Column([
        ft.Text("CARGO / PERFIL", size=11, color=ft.Colors.TEAL_700, weight="bold"),
        ft.Container(
            content=perfil_dropdown, bgcolor=cor_input_fundo,
            border=ft.border.all(1, cor_borda), border_radius=10, height=55,
        )
    ], spacing=5, col=12)

    def salvar_clique(e):
        try:
            atualizar_usuario_db(
                id_user=id_usuario,
                nome=nome_in.value,
                cpf=cpf_in.value,
                email=email_in.value,
                perfil=perfil_dropdown.value
            )
            page.snack_bar = ft.SnackBar(ft.Text("Usuário atualizado!"), bgcolor="green")
            page.snack_bar.open = True
            on_users()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    layout_campos = ft.ResponsiveRow(
        controls=[nome_c, cpf_c, email_c, perfil_c],
        spacing=15, run_spacing=15,
    )

    page.add(
        ft.Column(
            horizontal_alignment="center",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Divider(height=10, color="transparent"),
                layout_campos,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Salvar Alterações", 
                    on_click=salvar_clique, 
                    width=250, height=50,
                    style=ft.ButtonStyle(bgcolor="#1B4F9C", color="white", shape=ft.RoundedRectangleBorder(radius=10))
                ),
            ],
            spacing=10
        )
    )
    page.update()