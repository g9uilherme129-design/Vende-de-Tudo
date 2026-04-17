import flet as ft
from database import cadastrar_usuario_db, gerar_id_char

def novo_usuario(page: ft.Page, on_users):
    page.controls.clear()
    page.scroll = ft.ScrollMode.AUTO

    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_input = "#0A122A" if is_dark else "#FFFFFF"
    cor_borda_input = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_input = "white" if is_dark else "black"
    cor_label = ft.Colors.TEAL_400 if is_dark else ft.Colors.TEAL_900

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

    # Função auxiliar para manter seu estilo visual
    def estilo_input(label, hint="", password=False, keyboard_type=ft.KeyboardType.TEXT):
        input_field = ft.TextField(
            hint_text=hint,
            password=password,
            can_reveal_password=password,
            border=ft.InputBorder.NONE,
            content_padding=15,
            text_style=ft.TextStyle(color=cor_texto_input),
            expand=True,
            keyboard_type=keyboard_type
        )
        
        container = ft.Column(
            [
                ft.Text(f"  {label}", size=12, color=cor_label, weight="bold"),
                ft.Container(
                    content=input_field,
                    bgcolor=cor_fundo_input,
                    border=ft.border.all(1, cor_borda_input),
                    border_radius=12,
                    padding=ft.padding.only(right=10),
                )
            ],
            spacing=5,
        )
        return container, input_field

    # Criando os campos
    nome_c, nome_in = estilo_input("NOME COMPLETO", hint="Ex: Neymar Jr")
    cpf_c, cpf_in = estilo_input("CPF (Apenas números)", hint="12345678900", keyboard_type=ft.KeyboardType.NUMBER)
    email_c, email_in = estilo_input("E-MAIL", hint="usuario@email.com", keyboard_type=ft.KeyboardType.EMAIL)
    senha_c, senha_in = estilo_input("SENHA", hint="******", password=True)
    # Novo campo de Salário
    salario_c, salario_in = estilo_input("SALÁRIO BASE", hint="2.500,00", keyboard_type=ft.KeyboardType.NUMBER)# Após criar, você acessa o TextField (salario_in) e define o prefixo:
    salario_in.prefix_text = "R$ "
    salario_in.hint_text = "0,00"

    perfil_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("admin", "ADMINISTRADOR"),
            ft.dropdown.Option("vendedor", "VENDEDOR"),
        ],
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(color=cor_texto_input),
        content_padding=ft.padding.only(left=15),
        expand=True,
    )

    perfil_c = ft.Column(
        [
            ft.Text("  PERFIL / CARGO", size=12, color=cor_label, weight="bold"),
            ft.Container(
                content=perfil_dropdown,
                bgcolor=cor_fundo_input,
                border=ft.border.all(1, cor_borda_input),
                border_radius=12,
                height=55,
            )
        ],
        spacing=5,
    )

    def salvar_usuario(e):
        # 1. Limpa espaços e valida
        nome = nome_in.value.strip() if nome_in.value else ""
        email = email_in.value.strip() if email_in.value else ""
        senha = senha_in.value.strip() if senha_in.value else ""
        cpf = cpf_in.value.strip() if cpf_in.value else ""
        salario = salario_in.value.strip() if salario_in.value else "0"
        perfil = perfil_dropdown.value

        if not nome or not email or not senha or not perfil:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha os campos obrigatórios!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Gerar ID único (ex: U10005)
            novo_id = gerar_id_char("usuario", "id_user", "U")

            # Chama o banco
            sucesso, msg = cadastrar_usuario_db(
                id_user=novo_id,
                nome=nome,
                cpf=cpf,
                email=email,
                senha=senha,
                perfil=perfil,
                salario=salario
            )
            
            if sucesso:
                page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="green")
                page.snack_bar.open = True
                page.update()
                # Pequena pausa para o usuário ver a mensagem antes de mudar de tela
                on_users() 
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {msg}"), bgcolor="red")
                page.snack_bar.open = True
                page.update()

        except Exception as ex:
            print(f"Erro na UI: {ex}") # Isso aparece no seu terminal do VS Code
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro inesperado: {ex}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    form_content = ft.Column(
        [
            nome_c,
            cpf_c,
            email_c,
            senha_c,
            salario_c, # Adicionado no layout
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
        spacing=18,
        width=400,
    )

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=form_content,
                    padding=20,
                )
            ],
            alignment="center" # Centraliza o formulário na tela
        )
    )
    
    page.update()