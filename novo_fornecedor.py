import flet as ft
import re
from database import cadastrar_fornecedor_db

ESTADOS_BR = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", 
    "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"
]

def novo_fornecedor(page: ft.Page, on_voltar):
    page.controls.clear()
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_input = "#0A122A" if is_dark else "#FFFFFF"
    cor_borda_input = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_input = "white" if is_dark else "black"
    cor_label = ft.Colors.TEAL_700 if is_dark else ft.Colors.TEAL_900

    # --- FUNÇÕES DE MÁSCARA AUTOMÁTICA ---
    def formatar_cep(e):
        # Remove tudo que não é dígito
        valor = re.sub(r"\D", "", e.control.value)
        if len(valor) > 5:
            # Coloca o hífen após o 5º dígito: 00000-000
            e.control.value = f"{valor[:5]}-{valor[5:8]}"
        else:
            e.control.value = valor
        e.control.update()

    def formatar_telefone(e):
        valor = re.sub(r"\D", "", e.control.value)
        if len(valor) <= 2:
            e.control.value = valor
        elif len(valor) <= 7:
            e.control.value = f"({valor[:2]}) {valor[2:]}"
        else:
            # Formato (31) 99999-9999
            e.control.value = f"({valor[:2]}) {valor[2:7]}-{valor[7:11]}"
        e.control.update()

    # --- FUNÇÃO DE ESTILO (ADAPTADA PARA RECEBER ON_CHANGE) ---
    def estilo_input(label, hint="", col=None, keyboard_type=ft.KeyboardType.TEXT, limite=None, on_change=None):
        input_field = ft.TextField(
            hint_text=hint, 
            border=ft.InputBorder.NONE,
            content_padding=15, 
            text_style=ft.TextStyle(color=cor_texto_input),
            expand=True, 
            keyboard_type=keyboard_type,
            max_length=limite,
            on_change=on_change,
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
    nome_c, nome_in = estilo_input("NOME DO FORNECEDOR", hint="Ex: Coca-Cola", col=12)
    cnpj_c, cnpj_in = estilo_input("CNPJ", hint="00.000.000/0000-00", col=12, limite=18)
    
    # Telefone com máscara (15 é o tamanho com a máscara visual)
    tel_c, tel_in = estilo_input("TELEFONE", hint="(31) 99999-9999", col=6, 
                                 keyboard_type=ft.KeyboardType.PHONE, on_change=formatar_telefone, limite=15)
    
    email_c, email_in = estilo_input("E-MAIL", hint="contato@empresa.com", col=6)
    
    rua_c, rua_in = estilo_input("LOGRADOURO (RUA)", hint="Rua...", col=9)
    num_c, num_in = estilo_input("Nº", hint="123", col=3)
    bairro_c, bairro_in = estilo_input("BAIRRO", col=6)
    
    # CEP com máscara (9 é o tamanho visual: 35790-000)
    cep_c, cep_in = estilo_input("CEP", hint="00000-000", col=6, 
                                 keyboard_type=ft.KeyboardType.NUMBER, on_change=formatar_cep, limite=9)

    # Função de dropdown (mantida igual)
    def estilo_dropdown(label, options, value=None, col=None):
        dd = ft.Dropdown(options=[ft.dropdown.Option(opt) for opt in options], value=value,
                         border=ft.InputBorder.NONE, content_padding=15, text_style=ft.TextStyle(color=cor_texto_input), expand=True)
        return ft.Column([ft.Text(label, size=11, color=cor_label, weight="bold"),
                          ft.Container(content=dd, bgcolor=cor_fundo_input, border=ft.border.all(1, cor_borda_input), border_radius=10)], spacing=5, col=col), dd

    uf_c, uf_in = estilo_dropdown("ESTADO (UF)", options=ESTADOS_BR, value="MG", col=4)
    cidade_c, cidade_in = estilo_input("CIDADE", hint="Curvelo", col=8)

    def salvar_clique(e):
        if not nome_in.value or not cnpj_in.value:
            page.snack_bar = ft.SnackBar(ft.Text("Nome e CNPJ são obrigatórios!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # LIMPEZA CRUCIAL PARA O BANCO (Remove as máscaras visuais)
        telefone_limpo = re.sub(r"\D", "", tel_in.value)
        cep_limpo = re.sub(r"\D", "", cep_in.value)

        sucesso, msg = cadastrar_fornecedor_db(
            nome_in.value, cnpj_in.value, telefone_limpo, email_in.value,
            rua_in.value, num_in.value, bairro_in.value, cidade_in.value, uf_in.value, cep_limpo
        )

        if sucesso:
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="green")
            page.snack_bar.open = True
            on_voltar()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {msg}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    # --- RESTO DO LAYOUT ---
    layout_campos = ft.ResponsiveRow(
        controls=[nome_c, cnpj_c, tel_c, email_c, 
                  ft.Text("ENDEREÇO", size=14, weight="bold", color=cor_label, col=12),
                  rua_c, num_c, bairro_c, cep_c, uf_c, cidade_c],
        spacing=15, run_spacing=15,
    )

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_voltar()),
        title=ft.Text("Novo Fornecedor", size=20, weight="bold", color="white"),
        bgcolor="#0b1445", center_title=True,
    )

    corpo_formulario = ft.Container(
        content=ft.Column(
            horizontal_alignment="center",
            controls=[
                ft.Divider(height=10, color="transparent"),
                layout_campos,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton("CADASTRAR FORNECEDOR", on_click=salvar_clique, width=float("inf"), height=50,
                                  style=ft.ButtonStyle(bgcolor="#1B4F9C", color="white", shape=ft.RoundedRectangleBorder(radius=12))),
                ft.Container(height=40)
            ]
        ),
        width=500, padding=10,
    )

    page.add(ft.Row(controls=[corpo_formulario], alignment=ft.MainAxisAlignment.CENTER))
    page.update()