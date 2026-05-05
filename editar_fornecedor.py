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

    # --- LISTA DE ESTADOS ---
    estados_brasil = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]

    # --- CORES E TEMA ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_input_fundo = "#0A122A" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_label = ft.Colors.TEAL_400 if is_dark else ft.Colors.TEAL_900

    # --- FUNÇÃO DE ESTILO ADAPTADA ---
    def estilo_input(label, value="", read_only=False, col=None, limite=None, is_dropdown=False):
        if is_dropdown:
            field = ft.Dropdown(
                value=value,
                options=[ft.dropdown.Option(st) for st in estados_brasil],
                border=ft.InputBorder.NONE,
                content_padding=ft.padding.only(left=15, top=0, bottom=0),
                text_style=ft.TextStyle(color=cor_texto_principal),
                expand=True,
            )
        else:
            field = ft.TextField(
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
                content=field, 
                bgcolor=cor_input_fundo,
                border=ft.border.all(1, cor_borda), 
                border_radius=12,
                padding=ft.padding.only(right=10),
                height=50 if is_dropdown else None # Garante altura consistente
            )
        ], spacing=5, col=col)
        return container, field

    # --- CAMPOS ---
    nome_c, nome_in = estilo_input("NOME DO FORNECEDOR", value=f.get('nome_fornecedor'), col=12, limite=150)
    cnpj_c, cnpj_in = estilo_input("CNPJ", value=f.get('CNPJ'), col=6, limite=14)
    tel_c, tel_in = estilo_input("TELEFONE", value=f.get('telefone'), col=6, limite=11)
    email_c, email_in = estilo_input("E-MAIL", value=f.get('email_forn', ''), col=12, limite=100)
    
    rua_c, rua_in = estilo_input("LOGRADOURO (RUA)", value=f.get('endereco_logradouro'), col=8, limite=150)
    num_c, num_in = estilo_input("Nº", value=f.get('endereco_numero'), col=4, limite=5)
    bairro_c, bairro_in = estilo_input("BAIRRO", value=f.get('bairro'), col=12, limite=100)
    cid_c, cid_in = estilo_input("CIDADE", value=f.get('cidade'), col=8, limite=100)
    
    # Campo UF agora como Dropdown
    uf_c, uf_in = estilo_input("UF", value=f.get('ESTADO'), col=4, is_dropdown=True)
    
    cep_c, cep_in = estilo_input("CEP", value=f.get('CEP'), col=4, limite=9)

    def salvar_alteracoes(e):
        try:
            atualizar_fornecedor_db(
                id_fornecedor,
                nome_in.value,
                cnpj_in.value,
                tel_in.value,   
                email_in.value,
                rua_in.value,
                num_in.value,
                bairro_in.value,
                cid_in.value,
                uf_in.value, # Pega o valor selecionado no Dropdown
                cep_in.value
            )
            page.snack_bar = ft.SnackBar(ft.Text("Fornecedor atualizado!"), bgcolor="green")
            page.snack_bar.open = True
            on_back() 
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    # --- LAYOUT ---
    layout_campos = ft.ResponsiveRow(
        controls=[
            nome_c, cnpj_c, tel_c, email_c, 
            rua_c, num_c, bairro_c, cid_c, uf_c, cep_c
        ],
        spacing=15, run_spacing=15,
    )

    # Organizando na tela com Scroll
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text(f"Editar Fornecedor #{id_fornecedor}", size=24, weight="bold", color=cor_texto_principal),
                ft.Divider(height=10, color="transparent"),
                layout_campos,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Salvar Alterações", 
                    on_click=salvar_alteracoes, 
                    width=300, height=50,
                    style=ft.ButtonStyle(
                        bgcolor="#1B4F9C", 
                        color="white", 
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                ),
                ft.Container(height=40) 
            ], scroll=ft.ScrollMode.ADAPTIVE, spacing=10),
            padding=20,
            expand=True
        )
    )
    page.update()