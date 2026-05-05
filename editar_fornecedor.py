import flet as ft
from database import buscar_fornecedor_por_id, atualizar_fornecedor_db

def editar_fornecedor(page: ft.Page, on_back, id_fornecedor):
    page.controls.clear()
    page.padding = 0
    
    # Busca os dados atuais no banco
    try:
        f = buscar_fornecedor_por_id(id_fornecedor)
    except Exception as ex:
        print(f"Erro ao buscar fornecedor: {ex}")
        f = {}

    # --- CORES E TEMA ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = ft.Colors.GREY_500
    cor_input_fundo = "#0A122A" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_label = ft.Colors.TEAL_400 if is_dark else ft.Colors.TEAL_900

    # --- APPBAR ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_NEW, 
            icon_color="white", 
            on_click=lambda _: on_back()
        ),
        title=ft.Text("Vende de Tudo", color="white", weight="bold"),
        bgcolor="#0b1445",
        center_title=True,
    )

    # --- FUNÇÃO DE ESTILO COM LIMITE ---
    def estilo_input(label, value="", read_only=False, col=None, limite=None):
        input_field = ft.TextField(
            value=str(value) if value else "",
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color=cor_texto_principal),
            expand=True,
            max_length=limite,
        )
        container = ft.Column([
            ft.Text(f"  {label}", size=11, color=cor_label, weight="bold"),
            ft.Container(
                content=input_field, 
                bgcolor=cor_input_fundo,
                border=ft.border.all(1, cor_borda), 
                border_radius=12,
                padding=ft.padding.only(right=10),
            )
        ], spacing=5, col=col)
        return container, input_field

    # --- CAMPOS COM LIMITES ---
    nome_c, nome_in = estilo_input("RAZÃO SOCIAL / NOME", value=f.get('nome_fornecedor', ''), col=12, limite=100)
    cnpj_c, cnpj_in = estilo_input("CNPJ", value=f.get('CNPJ', ''), col=6, limite=14)
    tel_c, tel_in = estilo_input("TELEFONE", value=f.get('telefone', ''), col=6, limite=11)
    email_c, email_in = estilo_input("E-MAIL", value=f.get('email_forn', ''), col=12, limite=100)
    
    # Endereço
    rua_c, rua_in = estilo_input("LOGRADOURO (RUA/AV)", value=f.get('endereco_logradouro', ''), col=9, limite=150)
    num_c, num_in = estilo_input("Nº", value=f.get('endereco_numero', ''), col=3, limite=10)
    bairro_c, bairro_in = estilo_input("BAIRRO", value=f.get('bairro', ''), col=5, limite=50)
    cid_c, cid_in = estilo_input("CIDADE", value=f.get('cidade', ''), col=5, limite=50)
    uf_c, uf_in = estilo_input("UF", value=f.get('estado', ''), col=2, limite=2)

    def salvar_alteracoes(e):
        try:
            atualizar_fornecedor_db(
                id_forn=id_fornecedor,
                nome=nome_in.value,
                cnpj=cnpj_in.value,
                tel=tel_in.value,
                email=email_in.value,
                logradouro=rua_in.value,
                num=num_in.value,
                bairro=bairro_in.value,
                cidade=cid_in.value,
                uf=uf_in.value
            )
            page.snack_bar = ft.SnackBar(ft.Text("Fornecedor atualizado com sucesso!"), bgcolor="green")
            page.snack_bar.open = True
            on_back() 
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao atualizar: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    # --- LAYOUT E ESTRUTURA ---
    layout_campos = ft.ResponsiveRow(
        controls=[
            nome_c, cnpj_c, tel_c, email_c, 
            rua_c, num_c, bairro_c, cid_c, uf_c
        ],
        spacing=15, run_spacing=15,
    )

    form_content = ft.Column(
        expand=True,
        controls=[
            ft.Container(
                padding=ft.padding.only(top=20, bottom=10),
                content=ft.Text(f"Editar Fornecedor #{id_fornecedor}", size=24, weight="bold", color=cor_texto_principal)
            ),
            ft.Container(
                content=ft.Column([
                    layout_campos,
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Salvar Alterações", 
                        on_click=salvar_alteracoes, 
                        width=500, 
                        height=50,
                        style=ft.ButtonStyle(
                            bgcolor="#1B4F9C", 
                            color="white", 
                            shape=ft.RoundedRectangleBorder(radius=12)
                        )
                    ),
                    ft.Container(height=40)
                ], scroll=ft.ScrollMode.AUTO),
                expand=True,
            )
        ]
    )

    page.add(
        ft.Column(
            expand=True,
            horizontal_alignment="center",
            controls=[
                ft.Container(
                    content=form_content,
                    width=500, # Padronização de largura
                    padding=20,
                    expand=True
                )
            ]
        )
    )
    page.update()