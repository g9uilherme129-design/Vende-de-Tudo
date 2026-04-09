import flet as ft
from database import cadastrar_fornecedor_db

def novo_fornecedor(page: ft.Page, on_voltar):
    page.controls.clear()
    page.padding = 20

    # --- CONFIGURAÇÃO DE TEMA ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_input = "#0A122A" if is_dark else "#FFFFFF"
    cor_borda_input = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_input = "white" if is_dark else "black"
    cor_label = ft.Colors.TEAL_700 if is_dark else ft.Colors.TEAL_900

    # --- APPBAR PADRÃO ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_voltar()),
        title=ft.Text("Novo Fornecedor", size=20, weight="bold", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    # --- FUNÇÃO DE ESTILO (PADRÃO PRODUTO) ---
    def estilo_input(label, hint="", value="", col=None, keyboard_type=ft.KeyboardType.TEXT):
        input_field = ft.TextField(
            value=value, 
            hint_text=hint, 
            border=ft.InputBorder.NONE,
            content_padding=15, 
            text_style=ft.TextStyle(color=cor_texto_input),
            expand=True, 
            keyboard_type=keyboard_type
        )
        container = ft.Column([
            ft.Text(label, size=11, color=cor_label, weight="bold"),
            ft.Container(
                content=input_field, 
                bgcolor=cor_fundo_input,
                border=ft.border.all(1, cor_borda_input), 
                border_radius=10,
                padding=ft.padding.only(right=10),
            )
        ], spacing=5, col=col)
        return container, input_field

    # --- CAMPOS DO FORMULÁRIO ---
    nome_c, nome_in = estilo_input("NOME DO FORNECEDOR", hint="Ex: Coca-Cola Brasil", col=12)
    cnpj_c, cnpj_in = estilo_input("CNPJ", hint="00.000.000/0000-00", col=12)
    tel_c, tel_in = estilo_input("TELEFONE", hint="(31) 99999-9999", col=6)
    email_c, email_in = estilo_input("E-MAIL", hint="contato@empresa.com", col=6)
    
    # Endereço
    rua_c, rua_in = estilo_input("LOGRADOURO (RUA)", hint="Rua...", col=9)
    num_c, num_in = estilo_input("Nº", hint="123", col=3)
    bairro_c, bairro_in = estilo_input("BAIRRO", col=6)
    cidade_c, cidade_in = estilo_input("CIDADE", value="Curvelo", col=6)
    uf_c, uf_in = estilo_input("ESTADO (UF)", value="MG", col=4)
    cep_c, cep_in = estilo_input("CEP", hint="35790-000", col=8)

    def salvar_clique(e):
        if not nome_in.value or not cnpj_in.value:
            page.snack_bar = ft.SnackBar(ft.Text("Nome e CNPJ são obrigatórios!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        sucesso, msg = cadastrar_fornecedor_db(
            nome_in.value, cnpj_in.value, tel_in.value, email_in.value,
            rua_in.value, num_in.value, bairro_in.value, cidade_in.value, uf_in.value, cep_in.value
        )

        if sucesso:
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="green")
            page.snack_bar.open = True
            on_voltar() # Volta para a lista
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {msg}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    # --- LAYOUT RESPONSIVO ---
    layout_campos = ft.ResponsiveRow(
        controls=[
            nome_c, cnpj_c, 
            tel_c, email_c,
            ft.Text("ENDEREÇO", size=14, weight="bold", color=cor_label, col=12), # Subtítulo
            rua_c, num_c,
            bairro_c, cidade_c,
            uf_c, cep_c
        ],
        spacing=15, 
        run_spacing=15,
    )

    page.add(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment="center",
            controls=[
                ft.Divider(height=10, color="transparent"),
                layout_campos,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "CADASTRAR FORNECEDOR", 
                    on_click=salvar_clique, 
                    width=300, 
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor="#1B4F9C", 
                        color="white", 
                        shape=ft.RoundedRectangleBorder(radius=12)
                    )
                ),
                ft.Container(height=40) # Respiro no fundo
            ]
        )
    )
    page.update()