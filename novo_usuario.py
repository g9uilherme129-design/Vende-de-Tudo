import flet as ft

def novo_usuario(page: ft.Page, on_users):
    page.controls.clear()
    # Cores dinâmicas baseadas no tema
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

    def estilo_input(label, hint="", value="", read_only=False, col=None):
        input_field = ft.TextField(
            value=value,
            hint_text=hint,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color=cor_texto_input),
            expand=True,
        )
        
        container = ft.Column(
            [
                ft.Text(label, size=11, color=cor_label, weight=ft.FontWeight.BOLD),
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

    # Nome Completo
    nome_container, nome_input = estilo_input("NOME COMPLETO", hint="Nome do funcionário", col=12)
    
    # Dropdown de Cargo adaptado
    cargo_dropdown = ft.Dropdown(
        hint_text="Selecione o cargo",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
        options=[
            ft.dropdown.Option("ADMINISTRADOR"),
            ft.dropdown.Option("VENDEDOR"),
        ],
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(color=cor_texto_input),
        content_padding=ft.padding.only(left=15, right=0),
    )

    cargo_container = ft.Column(
        [
            ft.Text("CARGO", size=11, color=cor_label, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=cargo_dropdown,
                bgcolor=cor_fundo_input,
                border=ft.border.all(1, cor_borda_input),
                border_radius=10,
                height=55,
            )
        ],
        spacing=5,
        col=6 
    )

    salario_container, salario_input = estilo_input("SALÁRIO", hint="R$ 0,00", col=12)
    data_container, data_input = estilo_input("DATA DE CONTRATAÇÃO", hint="dd/mm/aaaa", col=12)

    def salvar_usuario(e):
        # Aqui você pode adicionar a lógica do banco depois
        page.snack_bar = ft.SnackBar(ft.Text("Usuário cadastrado com sucesso!"), bgcolor="green")
        page.snack_bar.open = True
        page.update()

        try:
            cadastrar_usuario_db(
                nome=nome_in.value,
                cpf=cpf_in.value,
                email=email_in.value,
                senha=senha_in.value,
                perfil=perfil_dropdown.value
            )
            
            page.snack_bar = ft.SnackBar(ft.Text("Usuário cadastrado com sucesso!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()
            
            # time.sleep(1)
            on_users() 

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao salvar: {ex}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    # Arrumando o problema do max_width: 
    # Usamos um Column com width fixo (400) que funciona bem em mobile e desktop
    form_content = ft.Column(
        [
            nome_c,
            cpf_c,
            email_c,
            senha_c,
            perfil_c,
            ft.Container(height=10),
            ft.ElevatedButton(
                "CADASTRAR USUÁRIO",
                on_click=salvar_usuario,
                width=400,
                height=55,
                style=ft.ButtonStyle(
                    bgcolor="#1B4F9C",
                    color="white",
                    shape=ft.RoundedRectangleBorder(radius=12),
                )
            ),
        ],
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
                    "Adicionar",
                    on_click=salvar_usuario,
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor="#1B4F9C",
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=12),
                    )
                ),
            ],
            spacing=10
        )
    )
    page.update()