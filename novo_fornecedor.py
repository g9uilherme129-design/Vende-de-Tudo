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

    # =========================================================
    # Máscara CNPJ
    def mascara_cnpj(e):
        valor = "".join(filter(str.isdigit, e.control.value))[:14]

        if len(valor) > 12:
            valor = f"{valor[:2]}.{valor[2:5]}.{valor[5:8]}/{valor[8:12]}-{valor[12:]}"
        elif len(valor) > 8:
            valor = f"{valor[:2]}.{valor[2:5]}.{valor[5:8]}/{valor[8:]}"
        elif len(valor) > 5:
            valor = f"{valor[:2]}.{valor[2:5]}.{valor[5:]}"
        elif len(valor) > 2:
            valor = f"{valor[:2]}.{valor[2:]}"
        
        e.control.value = valor
        page.update()

    # Máscara Telefone
    def mascara_telefone(e):
        valor = "".join(filter(str.isdigit, e.control.value))[:11]

        if len(valor) > 6:
            valor = f"({valor[:2]}) {valor[2:7]}-{valor[7:]}"
        elif len(valor) > 2:
            valor = f"({valor[:2]}) {valor[2:]}"
        
        e.control.value = valor
        page.update()

    # >>>>>>> SÓ ADICIONADO (MÁSCARA CEP) <<<<<<<<
    def mascara_cep(e):
        valor = "".join(filter(str.isdigit, e.control.value))[:8]

        if len(valor) > 5:
            valor = f"{valor[:5]}-{valor[5:]}"
        
        e.control.value = valor
        page.update()
    # =========================================================

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_voltar()),
        title=ft.Text("Novo Fornecedor", size=20, weight="bold", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    def estilo_input(label, hint="", value="", col=None, keyboard_type=ft.KeyboardType.TEXT, limite=None):
        input_field = ft.TextField(
            hint_text=hint, 
            border=ft.InputBorder.NONE,
            content_padding=15, 
            text_style=ft.TextStyle(color=cor_texto_input),
            expand=True, 
            keyboard_type=keyboard_type,
            max_length=limite,
        )
        container = ft.Column([
            ft.Text(label, size=11, color=cor_label, weight="bold"),
            ft.Container(
                content=input_field, 
                bgcolor=cor_fundo_input,
                border=ft.border.all(1, cor_borda_input), 
                border_radius=10,
                padding=ft.padding.only(right=10, bottom=5),
            )
        ], spacing=5, col=col)
        return container, input_field

    nome_c, nome_in = estilo_input("NOME DO FORNECEDOR", hint="Ex: Coca-Cola Brasil", col=12, limite=150)

    cnpj_c, cnpj_in = estilo_input("CNPJ", hint="00.000.000/0000-00", col=6, limite=18)
    cnpj_in.on_change = mascara_cnpj

    tel_c, tel_in = estilo_input("TELEFONE", hint="(31) 99999-9999", col=6, limite=15)
    tel_in.on_change = mascara_telefone

    email_c, email_in = estilo_input("E-MAIL", hint="contato@empresa.com", col=12, limite=100)

    rua_c, rua_in = estilo_input("LOGRADOURO (RUA)", hint="Rua...", col=8, limite=150)
    num_c, num_in = estilo_input("Nº", hint="123", col=3, limite=3)
    bairro_c, bairro_in = estilo_input("BAIRRO", col=9, limite=100)
    cidade_c, cidade_in = estilo_input("CIDADE", value="Curvelo", col=8, limite=100)
    uf_c, uf_in = estilo_input("ESTADO (UF)", value="MG", col=4, limite=2)

    # >>>>>>> AQUI FOI SÓ ADICIONADO O CEP <<<<<<<<
    cep_c, cep_in = estilo_input("CEP", hint="35790-000", col=4, limite=9)
    cep_in.on_change = mascara_cep

    def salvar_clique(e):
        if not nome_in.value or not cnpj_in.value:
            page.snack_bar = ft.SnackBar(ft.Text("Nome e CNPJ são obrigatórios!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        sucesso, msg = cadastrar_fornecedor_db(
            nome=nome_in.value, 
            cnpj=cnpj_in.value, 
            tel=tel_in.value, 
            email=email_in.value,
            logradouro=rua_in.value, 
            num=num_in.value, 
            bairro=bairro_in.value, 
            cidade=cidade_in.value, 
            uf=uf_in.value, 
            cep=cep_in.value
        )

        if sucesso:
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="green")
            page.snack_bar.open = True
            on_voltar()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {msg}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    layout_campos = ft.ResponsiveRow(
        controls=[
            nome_c, 
            cnpj_c, tel_c, 
            email_c,
            ft.Text("  ENDEREÇO", size=14, weight="bold", color=cor_label, col=12),
            rua_c,
            num_c, bairro_c,
            cidade_c, uf_c, cep_c
        ],
        spacing=15, 
        run_spacing=15,
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
                ft.ElevatedButton(
                    "CADASTRAR FORNECEDOR",
                    on_click=salvar_clique,
                    width=float("inf"),
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor="#1B4F9C",
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=12)
                    )
                ),
                ft.Container(height=40)
            ]
        ),
        width=500,
        padding=10,
    )

    page.add(ft.Row(controls=[corpo_formulario], alignment=ft.MainAxisAlignment.CENTER))
    page.update()