import flet as ft
from database import cadastrar_usuario_db, gerar_id_char
from log import write_log


def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    return True


def novo_usuario(page: ft.Page, on_users):
    page.clean()
    page.scroll = ft.ScrollMode.AUTO

    # --- PADRONIZAÇÃO DE CORES (IDÊNTICO AO SEU PERFIL) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#0b1445" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_input = "#0A122A" if is_dark else "#F5F7FB"

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color="white",
            on_click=lambda _: on_users()
        ),
        title=ft.Text("Novo Usuário", size=20, weight="bold", color="white"),
        bgcolor=cor_barra,
        center_title=True,
    )

    # --- FUNÇÃO AUXILIAR COM CORES DO TEMA ---
    def estilo_input(label, hint="", password=False, keyboard_type=ft.KeyboardType.TEXT, limite=None):
        input_field = ft.TextField(
            hint_text=hint,
            password=password,
            can_reveal_password=password,
            border=ft.InputBorder.NONE,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
            text_style=ft.TextStyle(color=cor_texto_p),
            expand=False,
            width=340,
            height=45,
            keyboard_type=keyboard_type,
            max_length=limite,
            cursor_color=cor_texto_s,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
        )

        container = ft.Column(
            [
                ft.Text(f"  {label}", size=15, color=cor_texto_s, weight="bold"),
                ft.Container(
                    content=input_field,
                    bgcolor=cor_input,
                    border=ft.border.all(1, cor_borda),
                    border_radius=12,
                    padding=ft.padding.only(right=10, bottom=5),
                    width=340,
                )
            ],
            spacing=5,
            width=340,
        )
        return container, input_field
    
    def mostrar_snack(mensagem, cor="#B00020"):
        page.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor=cor)
        page.snack_bar.open = True
        page.update()

    def mascara_cpf(e):
        # Remove tudo o que não for número e limita a 11 dígitos
        valor = "".join(filter(str.isdigit, e.control.value))[:11]
        
        # Aplica o fatiamento progressivo baseado no tamanho do texto
        if len(valor) > 9:
            valor = f"{valor[:3]}.{valor[3:6]}.{valor[6:9]}-{valor[9:]}"
        elif len(valor) > 6:
            valor = f"{valor[:3]}.{valor[3:6]}.{valor[6:]}"
        elif len(valor) > 3:
            valor = f"{valor[:3]}.{valor[3:]}"
            
        e.control.value = valor
        page.update()

    def bloquear_numeros_nome(e):
        valor = e.control.value or ""
        novo_valor = "".join(ch for ch in valor if not ch.isdigit())
        if novo_valor != valor:
            e.control.value = novo_valor
            e.control.error_text = "Números não são permitidos"
        else:
            e.control.error_text = None
        page.update()

    # --- CAMPOS ---
    nome_c, nome_in = estilo_input("NOME COMPLETO", hint="Ex: Neymar Jr", limite=100)
    nome_in.on_change = bloquear_numeros_nome

    # 1. Cria o input deixando o limite livre para os 14 caracteres da máscara (000.000.000-00)
    cpf_c, cpf_in = estilo_input("CPF (Apenas números)",
        hint="123.456.789-00",
        keyboard_type=ft.KeyboardType.NUMBER,
        limite=14  # <--- Aumentado para 14 para caber os pontos e o hífen!
    )

    # 2. ASSOCIAÇÃO CORRETA: O evento on_change deve ir no 'cpf_in' (TextField) e não no 'cpf_c' (Container)
    cpf_in.on_change = mascara_cpf

    email_c, email_in = estilo_input("E-MAIL", hint="usuario@email.com", keyboard_type=ft.KeyboardType.EMAIL, limite=100)
    senha_c, senha_in = estilo_input("SENHA", hint="******", password=True, limite=32)

    salario_c, salario_in = estilo_input("SALÁRIO BASE", hint="0,00", keyboard_type=ft.KeyboardType.NUMBER, limite=15)
    salario_in.prefix_text = "R$ "

    perfil_dropdown = ft.Dropdown(
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
            ft.Text("  PERFIL / CARGO", size=9, color=cor_texto_s, weight="bold"),
            ft.Container(
                content=perfil_dropdown,
                bgcolor=cor_input,
                border=ft.border.all(1, cor_borda),
                border_radius=12,
                height=50,
                width=340,
            )
        ],
        spacing=5,
        width=340,
    )

    # ---------------- SALVAR ----------------
    def salvar_usuario(e):
        nome = nome_in.value.strip() if nome_in.value else ""
        email = email_in.value.strip() if email_in.value else ""
        senha = senha_in.value.strip() if senha_in.value else ""
        cpf = cpf_in.value.strip() if cpf_in.value else ""
        salario = salario_in.value.strip() if salario_in.value else "0"
        perfil = perfil_dropdown.value

        if not nome or not email or not senha or not perfil:
            mostrar_snack("Preencha os campos obrigatórios!", "#B00020")
            return

        # Validação: nome não deve conter dígitos
        if any(ch.isdigit() for ch in nome):
            mostrar_snack("Nome não pode conter números.", "#B00020")
            return

        # CPF validação (sem máscara)
        cpf_limpo = ''.join(filter(str.isdigit, cpf))

        if not validar_cpf(cpf_limpo):
            mostrar_snack("CPF inválido! Verifique o número informado.", "#B00020")
            return

        try:
            novo_id = gerar_id_char("usuario", "id_user", "U")

            sucesso, msg = cadastrar_usuario_db(
                id_user=novo_id,
                nome=nome,
                cpf=cpf_limpo,
                email=email,
                senha=senha,
                perfil=perfil,
                salario=salario
            )
            
            if sucesso:
                write_log('cadastrar_usuario', user_id=novo_id, details=f"nome:{nome} cpf:{cpf_limpo} perfil:{perfil}")
                mostrar_snack("✅ Usuário cadastrado com sucesso!", "#00b40d")
                import time
                time.sleep(1)
                on_users()
            else:
                mostrar_snack(f"❌ {msg}", "#FF4444")
        except Exception as ex:
            mostrar_snack(f"❌ Erro inesperado: {ex}", "red")

    # ---------------- FORM ----------------
    form_content = ft.Column(
        [
            nome_c,
            cpf_c,
            email_c,
            senha_c,
            salario_c,
            perfil_c,
            ft.Container(height=10),
            ft.ElevatedButton(
                "CADASTRAR USUÁRIO",
                on_click=salvar_usuario,
                width=400,
                height=55,
                style=ft.ButtonStyle(
                    bgcolor=cor_texto_s, # Azul no Dark / Rosa no Light
                    color="white",
                    shape=ft.RoundedRectangleBorder(radius=12),
                )
            ),
        ],
        spacing=20,
        width=400,
    )

    page.add(
        ft.Container(
            expand=True,
            bgcolor=cor_fundo_tela,
            content=ft.Row(
                [
                    ft.Container(
                        content=form_content,
                        padding=20,
                        bgcolor=cor_fundo_card,
                        border_radius=20,
                        border=ft.border.all(1, cor_borda)
                    )
                ],
                alignment="center" 
            )
        )
    )

    page.update()