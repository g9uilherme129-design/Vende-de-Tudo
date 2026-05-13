import flet as ft
from database import buscar_fornecedor_por_id, atualizar_fornecedor_db
import time

def editar_fornecedor(page: ft.Page, on_back, id_fornecedor):
    page.controls.clear()
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    
    # --- PADRONIZAÇÃO DE CORES ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D" 
    cor_barra = "#0b1445" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_input_bg = "#0A122A" if is_dark else "#F5F7FB"
    cor_secundaria =  "#1679f2" if is_dark else "#DA7D7D"

    # Busca os dados atuais no banco
    try:
        f = buscar_fornecedor_por_id(id_fornecedor)
        if not f:
            f = {}
    except Exception as ex:
        print(f"Erro ao buscar fornecedor: {ex}")
        f = {}

    estados_brasil = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]

    # --- FUNÇÃO DE ESTILO ---
    def estilo_input(label, value="", read_only=False, col=None, limite=None, is_dropdown=False):
        if is_dropdown:
            field = ft.Dropdown(
                value=value,
                options=[ft.dropdown.Option(st) for st in estados_brasil],
                border=ft.InputBorder.NONE,
                content_padding=ft.padding.only(left=15, top=0, bottom=0),
                text_style=ft.TextStyle(color=cor_texto_p),
                expand=True,
            )
        else:
            field = ft.TextField(
                value=str(value) if value is not None else "",
                border=ft.InputBorder.NONE,
                content_padding=15,
                read_only=read_only,
                text_style=ft.TextStyle(color=cor_texto_p),
                expand=True,
                max_length=limite,
                cursor_color=cor_texto_s,
            )

        container = ft.Column([
            ft.Text(f"  {label}", size=11, color=cor_texto_s, weight="bold"),
            ft.Container(
                content=field, 
                bgcolor=cor_input_bg,
                border=ft.border.all(1, cor_borda), 
                border_radius=12,
                padding=ft.padding.only(right=10),
                height=50 
            )
        ], spacing=5, col=col)
        return container, field

    # --- LÓGICA DE CAPTURA DE DADOS (CORREÇÃO DO CEP) ---
    # Isso garante que pegue 'cep' ou 'CEP' e 'estado' ou 'ESTADO'
    valor_cep = f.get('cep') if f.get('cep') is not None else f.get('CEP', '')
    valor_uf = f.get('estado') if f.get('estado') is not None else f.get('ESTADO', 'MG')

    # --- INSTANCIAÇÃO DOS CAMPOS ---
    nome_c, nome_in = estilo_input("NOME DO FORNECEDOR", value=f.get('nome_fornecedor', ''), col=12, limite=150)
    cnpj_c, cnpj_in = estilo_input("CNPJ", value=f.get('CNPJ', f.get('cnpj', '')), col=6, limite=14)
    tel_c, tel_in = estilo_input("TELEFONE", value=f.get('telefone', ''), col=6, limite=11)
    email_c, email_in = estilo_input("E-MAIL", value=f.get('email_forn', ''), col=12, limite=100)
    
    rua_c, rua_in = estilo_input("LOGRADOURO (RUA)", value=f.get('endereco_logradouro', ''), col=8, limite=150)
    num_c, num_in = estilo_input("Nº", value=f.get('endereco_numero', ''), col=4, limite=5)
    bairro_c, bairro_in = estilo_input("BAIRRO", value=f.get('bairro', ''), col=12, limite=100)
    cid_c, cid_in = estilo_input("CIDADE", value=f.get('cidade', ''), col=8, limite=100)
    uf_c, uf_in = estilo_input("UF", value=valor_uf, col=4, is_dropdown=True)
    cep_c, cep_in = estilo_input("CEP", value=valor_cep, col=12, limite=9)

    def salvar_alteracoes(e):
        try:
            if not nome_in.value or not cnpj_in.value:
                page.snack_bar = ft.SnackBar(ft.Text("Nome e CNPJ são obrigatórios!"), bgcolor="orange")
                page.snack_bar.open = True
                page.update()
                return

            # Note que usamos .value de cada componente
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
                uf=uf_in.value, 
                cep=cep_in.value
            )
            
            page.snack_bar = ft.SnackBar(ft.Text("Fornecedor atualizado com sucesso!"), bgcolor="#00b40d")
            page.snack_bar.open = True
            page.update()
            
            on_back() 

        except Exception as ex:
            print(f"Erro ao salvar: {ex}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao salvar: {ex}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    # --- INTERFACE ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_back()),
        title=ft.Text("Editar Fornecedor", color="white", weight="bold"),
        bgcolor=cor_barra, 
        center_title=True,
    )

    page.add(
        ft.Container(
            expand=True,
            bgcolor=cor_fundo_tela,
            padding=20,
            content=ft.Column([
                ft.Container(
                    width=550, 
                    padding=25,
                    bgcolor=cor_fundo_card,
                    border_radius=20,
                    border=ft.border.all(1, cor_borda),
                    content=ft.Column([
                        ft.Text(f"Edição #{id_fornecedor}", size=28, weight="bold", color=cor_texto_p),
                        ft.Text("Atualize os dados abaixo.", size=14, color=cor_secundaria),
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                        
                        ft.ResponsiveRow(
                            controls=[
                                nome_c, cnpj_c, tel_c, email_c, 
                                ft.Container(height=10, col=12),
                                ft.Text("ENDEREÇO", size=14, weight="bold", color=cor_texto_p),
                                rua_c, num_c, bairro_c, cid_c, uf_c, cep_c
                            ],
                            spacing=15, run_spacing=15,
                        ),
                        
                        ft.Container(height=30),
                        
                        ft.ElevatedButton(
                            "SALVAR ALTERAÇÕES", 
                            on_click=salvar_alteracoes, 
                            width=800, height=55,
                            style=ft.ButtonStyle(
                                bgcolor=cor_texto_s, 
                                color="white", 
                                shape=ft.RoundedRectangleBorder(radius=12),
                                elevation=5
                            )
                        ),
                    ], horizontal_alignment="center")
                )
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment="center"),
        )
    )
    
    page.update()