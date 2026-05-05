import flet as ft
from database import cadastrar_produto_db, buscar_fornecedores_dropdown, buscar_categorias_dropdown
from datetime import datetime

def produto(page: ft.Page, on_stock):
    page.controls.clear()
    page.padding = 0

    # --- CORES E TEMA ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_input = "#0A122A" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_label = ft.Colors.TEAL_400 if is_dark else ft.Colors.TEAL_900

    # --- LÓGICA DE TRATAMENTO DE DATA ---
    def formatar_para_banco(data_br):
        try:
            # Converte de DD/MM/AAAA para AAAA-MM-DD
            dt = datetime.strptime(data_br, "%d/%m/%Y")
            return dt.strftime("%Y-%m-%d")
        except:
            # Se o usuário digitar errado, envia a data de hoje para não quebrar o banco
            return datetime.now().strftime("%Y-%m-%d")

    # --- MASCARA DE MOEDA ---
    def formatar_moeda(e):
        valor = "".join(filter(str.isdigit, e.control.value))
        if not valor:
            e.control.value = "0,00"
        else:
            float_valor = float(valor) / 100
            e.control.value = f"{float_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        page.update()

    # --- ESTILO DOS CAMPOS ---
    def criar_campo(label, control, col=None):
        return ft.Column([
            ft.Text(f"  {label}", size=11, color=cor_label, weight="bold"),
            ft.Container(
                content=control, bgcolor=cor_fundo_input,
                border=ft.border.all(1, cor_borda), border_radius=12,
                padding=ft.padding.symmetric(horizontal=10)
            )
        ], spacing=5, col=col)

    # --- CAMPOS ---
    in_nome = ft.TextField(hint_text="Nome do Item", border=ft.InputBorder.NONE, expand=True, max_length=100)
    in_cod = ft.TextField(hint_text="0000000000", border=ft.InputBorder.NONE, expand=True, max_length=10)
    
    drop_forn = ft.Dropdown(hint_text="Selecione o Fornecedor", border=ft.InputBorder.NONE, expand=True)
    drop_cat = ft.Dropdown(hint_text="Selecione a Categoria", border=ft.InputBorder.NONE, expand=True)

    in_qtd = ft.TextField(value="0", border=ft.InputBorder.NONE, expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    in_lote = ft.TextField(hint_text="Lote", border=ft.InputBorder.NONE, expand=True, max_length=9)
    
    drop_emb = ft.Dropdown(
        value="UN",
        options=[ft.dropdown.Option("UN"), ft.dropdown.Option("CX"), ft.dropdown.Option("KG"), ft.dropdown.Option("LT"), ft.dropdown.Option("PCT")],
        border=ft.InputBorder.NONE, expand=True
    )

    in_custo = ft.TextField(value="0,00", border=ft.InputBorder.NONE, expand=True, on_change=formatar_moeda)
    in_venda = ft.TextField(value="0,00", border=ft.InputBorder.NONE, expand=True, on_change=formatar_moeda)
    
    # Validade agora é manual igual ao Editar
    in_validade = ft.TextField(
        hint_text="DD/MM/AAAA", 
        border=ft.InputBorder.NONE, expand=True, 
        max_length=10
    )

    # Carregar Dropdowns
    try:
        for f in buscar_fornecedores_dropdown():
            drop_forn.options.append(ft.dropdown.Option(key=str(f['id_fornecedor']), text=f['nome_fornecedor']))
        for c in buscar_categorias_dropdown():
            drop_cat.options.append(ft.dropdown.Option(key=str(c['id_categoria']), text=c['nome_categoria']))
    except: pass

    def salvar_clique(e):
        if not drop_forn.value or not drop_cat.value or not in_nome.value or not in_validade.value:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos obrigatórios!"), bgcolor="orange")
            page.snack_bar.open = True
            page.update()
            return

        try:
            custo_final = float(in_custo.value.replace(".", "").replace(",", "."))
            venda_final = float(in_venda.value.replace(".", "").replace(",", "."))

            cadastrar_produto_db(
                drop_forn.value,
                drop_cat.value,
                in_nome.value,
                in_cod.value,
                formatar_para_banco(in_validade.value), # Converte o que foi digitado
                datetime.now().strftime("%Y-%m-%d"), 
                custo_final,
                venda_final,
                drop_emb.value,
                int(in_qtd.value),
                in_lote.value
            )
            page.snack_bar = ft.SnackBar(ft.Text("Produto cadastrado com sucesso!"), bgcolor="#08D345")
            page.snack_bar.open = True
            on_stock()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    # --- LAYOUT ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_stock()),
        title=ft.Text("Novo Produto", color="white", weight="bold"),
        bgcolor="#0b1445", center_title=True,
    )

    page.add(
        ft.Column(
            expand=True, horizontal_alignment="center", scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    width=600, padding=25,
                    content=ft.Column([
                        ft.Text("Cadastro de Estoque", size=22, weight="bold"),
                        ft.ResponsiveRow([
                            criar_campo("NOME DO PRODUTO (Máx 100)", in_nome, 12),
                            criar_campo("CÓDIGO DE BARRAS (Máx 10)", in_cod, 12),
                            criar_campo("CATEGORIA", drop_cat, 6),
                            criar_campo("FORNECEDOR", drop_forn, 6),
                            criar_campo("PREÇO CUSTO", in_custo, 6),
                            criar_campo("PREÇO VENDA", in_venda, 6),
                            criar_campo("QUANTIDADE", in_qtd, 4),
                            criar_campo("EMBALAGEM", drop_emb, 4),
                            criar_campo("LOTE (Máx 9)", in_lote, 4),
                            criar_campo("VALIDADE (DD/MM/AAAA)", in_validade, 12),
                        ], spacing=15),
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "CADASTRAR PRODUTO", on_click=salvar_clique,
                            bgcolor="#1B4F9C", color="white", height=55, width=600,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                        ),
                        ft.Container(height=40)
                    ])
                )
            ]
        )
    )
    page.update()