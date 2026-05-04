import flet as ft
from database import buscar_fornecedor_por_id, atualizar_fornecedor_db

def editar_fornecedor(page: ft.Page, on_back, id_fornecedor):
    page.controls.clear()
    
    # Busca os dados atuais no banco
    f = buscar_fornecedor_por_id(id_fornecedor)
    
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_input_fundo = "#0A122A" if is_dark else "#F0F2F5"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_back()),
        title=ft.Text(f"Editar Fornecedor #{id_fornecedor}", size=20, weight="bold", color="white"),
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
            text_style=ft.TextStyle(color=cor_texto),
            expand=True,
            max_length=limite, # Define o limite máximo
        )
        container = ft.Column([
            ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight="bold"),
            ft.Container(
                content=input_field, bgcolor=cor_input_fundo,
                border=ft.border.all(1, cor_borda), border_radius=10,
                padding=ft.padding.only(right=10, bottom=5), # Espaço para o contador
            )
        ], spacing=5, col=col)
        return container, input_field

    # --- CAMPOS COM LIMITES ---
    nome_c, nome_in = estilo_input("RAZÃO SOCIAL / NOME", value=f['nome_fornecedor'], col=12, limite=100)
    cnpj_c, cnpj_in = estilo_input("CNPJ", value=f['CNPJ'], read_only=False, col=6, limite=14)
    tel_c, tel_in = estilo_input("TELEFONE", value=f['telefone'], col=6, limite=11)
    email_c, email_in = estilo_input("E-MAIL", value=f.get('email_forn', ''), col=12, limite=100)
    
    # Campos de Endereço
    rua_c, rua_in = estilo_input("LOGRADOURO (RUA/AV)", value=f['endereco_logradouro'], col=9, limite=150)
    num_c, num_in = estilo_input("Nº", value=f['endereco_numero'], col=3, limite=10)
    bairro_c, bairro_in = estilo_input("BAIRRO", value=f['bairro'], col=5, limite=50)
    cid_c, cid_in = estilo_input("CIDADE", value=f['cidade'], col=5, limite=50)
    uf_c, uf_in = estilo_input("UF", value=f['estado'], col=2, limite=2)

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

    layout_campos = ft.ResponsiveRow(
        controls=[
            nome_c, cnpj_c, tel_c, email_c, 
            rua_c, num_c, bairro_c, cid_c, uf_c
        ],
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
                    on_click=salvar_alteracoes, 
                    width=250, height=50,
                    style=ft.ButtonStyle(
                        bgcolor="#1B4F9C", 
                        color="white", 
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                ),
                ft.Container(height=20) # Espaço extra no final
            ],
            spacing=10
        )
    )
    page.update()