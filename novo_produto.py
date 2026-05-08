import flet as ft
from database import cadastrar_produto_db, buscar_fornecedores_dropdown, buscar_categorias_dropdown
from datetime import datetime

def produto(page: ft.Page, on_stock):
    page.controls.clear()
    page.padding = 0

    # --- PADRONIZAÇÃO DE CORES (IDÊNTICO AO SEU PERFIL) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#0b1445" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_input = "#0A122A" if is_dark else "#F5F7FB"

    # --- LÓGICA DE TRATAMENTO DE DATA (MANTIDA) ---
    def formatar_data(e):
        valor = "".join(filter(str.isdigit, e.control.value))
        if len(valor) > 8: valor = valor[:8]
        if len(valor) >= 5:
            e.control.value = f"{valor[:2]}/{valor[2:4]}/{valor[4:]}"
        elif len(valor) >= 3:
            e.control.value = f"{valor[:2]}/{valor[2:]}"
        else:
            e.control.value = valor
        page.update()
    # Máscara da Data
    def mascara_data(e):
        valor = "".join(filter(str.isdigit, e.control.value))
        valor = valor[:8]

        if len(valor) > 4:
            valor = f"{valor[:2]}/{valor[2:4]}/{valor[4:]}"
        elif len(valor) > 2:
            valor = f"{valor[:2]}/{valor[2:]}"

        e.control.value = valor
        e.control.selection_start = len(valor)
        e.control.selection_end = len(valor)
        page.update()
    # ---------------------------------------

    # --- LÓGICA DE TRATAMENTO DE DATA ---
    def formatar_para_banco(data_br):
        try:
            dt = datetime.strptime(data_br, "%d/%m/%Y")
            return dt.strftime("%Y-%m-%d")
        except:
            return datetime.now().strftime("%Y-%m-%d")

    def formatar_moeda(e):
        valor = "".join(filter(str.isdigit, e.control.value))
        if not valor:
            e.control.value = "0,00"
        else:
            float_valor = float(valor) / 100
            e.control.value = f"{float_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        page.update()

    # --- ESTILO DOS CAMPOS PADRONIZADO ---
    def criar_campo(label, control, col=None):
        return ft.Column([
            ft.Text(f"  {label}", size=11, color=cor_texto_s, weight="bold"),
            ft.Container(
                content=control, 
                bgcolor=cor_input,
                border=ft.border.all(1, cor_borda), 
                border_radius=12,
                padding=ft.padding.symmetric(horizontal=10)
            )
        ], spacing=5, col=col)

    # --- CONFIGURAÇÃO DOS CONTROLES COM CORES DO TEMA ---
    estilo_texto = ft.TextStyle(color=cor_texto_p)

    in_nome = ft.TextField(hint_text="Nome do Item", border=ft.InputBorder.NONE, expand=True, max_length=100, text_style=estilo_texto)
    in_cod = ft.TextField(hint_text="0000000000", border=ft.InputBorder.NONE, expand=True, max_length=10, text_style=estilo_texto)
    
    drop_forn = ft.Dropdown(hint_text="Selecione", border=ft.InputBorder.NONE, expand=True, text_style=estilo_texto)
    drop_cat = ft.Dropdown(hint_text="Selecione", border=ft.InputBorder.NONE, expand=True, text_style=estilo_texto)

    in_qtd = ft.TextField(value="0", border=ft.InputBorder.NONE, expand=True, keyboard_type=ft.KeyboardType.NUMBER, text_style=estilo_texto)
    in_lote = ft.TextField(hint_text="Lote", border=ft.InputBorder.NONE, expand=True, max_length=9, text_style=estilo_texto)
    
    drop_emb = ft.Dropdown(
        value="UN",
        options=[ft.dropdown.Option("UN"), ft.dropdown.Option("CX"), ft.dropdown.Option("KG"), ft.dropdown.Option("LT"), ft.dropdown.Option("PCT")],
        border=ft.InputBorder.NONE, expand=True, text_style=estilo_texto
    )

    in_custo = ft.TextField(value="0,00", border=ft.InputBorder.NONE, expand=True, on_change=formatar_moeda, text_style=estilo_texto)
    in_venda = ft.TextField(value="0,00", border=ft.InputBorder.NONE, expand=True, on_change=formatar_moeda, text_style=estilo_texto)
    
    in_validade = ft.TextField(
        hint_text="DD/MM/AAAA", border=ft.InputBorder.NONE, expand=True, 
        max_length=10, on_change=formatar_data, keyboard_type=ft.KeyboardType.NUMBER, text_style=estilo_texto, on_change=mascara_data
    )
    # ------------------------------------

    # Carregar Dropdowns (MANTIDO)
    try:
        for f in buscar_fornecedores_dropdown():
            drop_forn.options.append(ft.dropdown.Option(key=str(f['id_fornecedor']), text=f['nome_fornecedor']))
        for c in buscar_categorias_dropdown():
            drop_cat.options.append(ft.dropdown.Option(key=str(c['id_categoria']), text=f['nome_categoria']))
    except: pass

    def salvar_clique(e):
        # Lógica de salvamento mantida...
        try:
            data_limpa = in_validade.value.strip().replace("-", "/")
            dt = datetime.strptime(data_limpa, "%d/%m/%Y")
            data_formatada = dt.strftime("%Y-%m-%d")
            
            custo_final = float(in_custo.value.replace(".", "").replace(",", "."))
            venda_final = float(in_venda.value.replace(".", "").replace(",", "."))

            cadastrar_produto_db(
                drop_forn.value,
                drop_cat.value,
                in_nome.value,
                in_cod.value,
                data_formatada, 
                formatar_para_banco(in_validade.value),
                datetime.now().strftime("%Y-%m-%d"), 
                custo_final,
                venda_final,
                drop_emb.value,
                int(in_qtd.value),
                in_lote.value
            )
            page.snack_bar = ft.SnackBar(ft.Text("Produto cadastrado!"), bgcolor="#08D345")
            page.snack_bar.open = True
            on_stock()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    # --- LAYOUT E APPBAR ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_stock()),
        title=ft.Text("Novo Produto", color="white", weight="bold"),
        bgcolor=cor_barra, center_title=True,
    )
    
    page.add(
        ft.Container(
            expand=True,
            bgcolor=cor_fundo_tela,
            content=ft.Column(
                horizontal_alignment="center", 
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        width=600, 
                        padding=25,
                        margin=ft.margin.only(top=20),
                        bgcolor=cor_fundo_card,
                        border_radius=20,
                        border=ft.border.all(1, cor_borda),
                        content=ft.Column([
                            ft.Text("Cadastro de Estoque", size=22, weight="bold", color=cor_texto_p),
                            ft.ResponsiveRow([
                                criar_campo("NOME DO PRODUTO", in_nome, 12),
                                criar_campo("CÓDIGO DE BARRAS", in_cod, 12),
                                criar_campo("CATEGORIA", drop_cat, 6),
                                criar_campo("FORNECEDOR", drop_forn, 6),
                                criar_campo("PREÇO CUSTO", in_custo, 6),
                                criar_campo("PREÇO VENDA", in_venda, 6),
                                criar_campo("QUANTIDADE", in_qtd, 4),
                                criar_campo("EMBALAGEM", drop_emb, 4),
                                criar_campo("LOTE", in_lote, 4),
                                criar_campo("VALIDADE (DD/MM/AAAA)", in_validade, 12),
                            ], spacing=15),
                            ft.Container(height=20),
                            ft.ElevatedButton(
                                "CADASTRAR PRODUTO", 
                                on_click=salvar_clique,
                                bgcolor=cor_texto_s, # Azul/Rosa conforme o tema
                                color="white", 
                                height=55, 
                                width=600,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                            ),
                            ft.Container(height=20)
                        ])
                    ),
                    ft.Container(height=40)
                ]
            )
        )
    )
    page.update()