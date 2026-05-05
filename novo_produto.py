import flet as ft
from database import cadastrar_produto_db, buscar_fornecedores_dropdown, buscar_categorias_dropdown
from datetime import datetime

def produto(page: ft.Page, on_stock):
    page.controls.clear()
    page.padding = 0

    # --- CORES E TEMA ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_input = "#0A122A" if is_dark else "#FFFFFF"
    cor_texto_input = "white" if is_dark else "black"
    cor_label = ft.Colors.TEAL_400 if is_dark else ft.Colors.TEAL_900
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK

    # --- LÓGICA DO CALENDÁRIO ---
    def mudar_data(e):
        val_in.value = date_picker.value.strftime("%d-%m-%Y")
        page.update()

    date_picker = ft.DatePicker(
        on_change=mudar_data,
        first_date=datetime(2023, 1, 1),
        last_date=datetime(2030, 12, 31),
    )

    if date_picker not in page.overlay:
        page.overlay.append(date_picker)

    # --- LÓGICA DE MÁSCARA DE MOEDA ---
    def formatar_moeda(e):
        valor = "".join(filter(str.isdigit, e.control.value))
        if not valor:
            e.control.value = "0,00"
        else:
            float_valor = float(valor) / 100
            e.control.value = f"{float_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        page.update()

    # --- COMPONENTES DROPDOWN ---
    drop_fornecedor = ft.Dropdown(
        expand=True, border=ft.InputBorder.NONE, 
        text_style=ft.TextStyle(color=cor_texto_input),
        hint_text="Selecione o Fornecedor"
    )
    
    drop_categoria = ft.Dropdown(
        expand=True, border=ft.InputBorder.NONE, 
        text_style=ft.TextStyle(color=cor_texto_input),
        hint_text="Selecione a Categoria"
    )

    # Carregamento seguro de dados
    try:
        for f in buscar_fornecedores_dropdown():
            drop_fornecedor.options.append(ft.dropdown.Option(key=str(f['id_fornecedor']), text=f['nome_fornecedor']))
        
        for c in buscar_categorias_dropdown():
            drop_categoria.options.append(ft.dropdown.Option(key=str(c['id_categoria']), text=c['nome_categoria']))
    except:
        pass

    def criar_container_input(label, component, col):
        return ft.Column([
            ft.Text(label, size=11, color=cor_label, weight="bold"),
            ft.Container(
                content=component, bgcolor=cor_fundo_input,
                border=ft.border.all(1, "#1E2B4E" if is_dark else "#D1D5DB"), 
                border_radius=10, padding=ft.padding.only(left=10, right=10, bottom=5),
            )
        ], spacing=5, col=col)

    def estilo_input(label, hint="", value="", col=None, keyboard_type=ft.KeyboardType.TEXT, on_change=None, suffix=None, read_only=False, limite=None):
        input_field = ft.TextField(
            value=value, 
            hint_text=hint, 
            border=ft.InputBorder.NONE,
            content_padding=15, 
            text_style=ft.TextStyle(color=cor_texto_input),
            expand=True, 
            keyboard_type=keyboard_type, 
            on_change=on_change, 
            suffix=suffix,
            read_only=read_only,
            max_length=limite,
        )
        return criar_container_input(label, input_field, col), input_field

    # --- CAMPOS ---
    nome_c, nome_in = estilo_input("NOME DO PRODUTO", col=12, limite=100)
    cod_c, cod_in = estilo_input("CÓDIGO DE BARRAS", col=12, limite=10)
    forn_c = criar_container_input("FORNECEDOR", drop_fornecedor, col=6)
    cat_c = criar_container_input("CATEGORIA", drop_categoria, col=6)
    
    qtd_c, qtd_in = estilo_input("QUANTIDADE", value="0", col=4, keyboard_type=ft.KeyboardType.NUMBER)
    lote_c, lote_in = estilo_input("LOTE", col=4, limite=30)
    emb_c, emb_in = estilo_input("EMBALAGEM", value="Unidade", col=4, limite=20)

    custo_c, custo_in = estilo_input("PREÇO CUSTO (R$)", value="0,00", col=6, on_change=formatar_moeda)
    venda_c, venda_in = estilo_input("PREÇO VENDA (R$)", value="0,00", col=6, on_change=formatar_moeda)
    
    val_c, val_in = estilo_input(
        "VALIDADE (AAAA-MM-DD)", 
        value=datetime.now().strftime("%Y-%m-%d"), 
        col=12,
        read_only=True,
        suffix=ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=lambda _: date_picker.open_picker())
    )

    def salvar_clique(e):
        if not drop_fornecedor.value or not drop_categoria.value:
            page.snack_bar = ft.SnackBar(ft.Text("Selecione Fornecedor e Categoria!"), bgcolor="orange")
            page.snack_bar.open = True
            page.update()
            return

        try:
            custo_final = float(custo_in.value.replace(".", "").replace(",", "."))
            venda_final = float(venda_in.value.replace(".", "").replace(",", "."))

            cadastrar_produto_db(
                drop_fornecedor.value,
                drop_categoria.value,
                nome_in.value,
                cod_in.value,
                val_in.value,
                datetime.now().strftime("%Y-%m-%d"),
                custo_final,
                venda_final,
                emb_in.value,
                int(qtd_in.value),
                lote_in.value
            )
            on_stock()
        except Exception as ex:
            print(f"Erro: {ex}")

    # --- CONTEÚDO PRINCIPAL ---
    layout_campos = ft.ResponsiveRow(
        controls=[nome_c, cod_c, forn_c, cat_c, qtd_c, lote_c, emb_c, custo_c, venda_c, val_c],
        spacing=15, run_spacing=15,
    )

    conteudo = ft.Column(
        expand=True,
        controls=[
            ft.Container(
                padding=ft.padding.only(top=20, left=10, right=10),
                content=ft.Row([
                    ft.Text("Novo Produto", size=26, weight="bold", color=cor_texto_principal),
                ])
            ),
            ft.Container(
                content=ft.Column([
                    layout_campos,
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Cadastrar no Sistema", 
                        on_click=salvar_clique, 
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
                padding=10
            )
        ]
    )

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_stock()),
        bgcolor="#0b1445",
        title=ft.Text("Vende de Tudo", color="white", weight="bold"),
        center_title=True,
    )

    page.add(
        ft.Column(
            expand=True,
            horizontal_alignment="center",
            controls=[
                ft.Container(
                    content=conteudo,
                    width=500, # Padronização
                    expand=True
                )
            ]
        )
    )
    page.update()