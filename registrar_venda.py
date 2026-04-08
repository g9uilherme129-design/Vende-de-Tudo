import flet as ft
from database import registrar_venda_db, buscar_produtos_estoque
from datetime import datetime

def tela_registrar_venda(page: ft.Page, on_voltar):
    page.controls.clear()
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO
    page.navigation_bar = None 

    # --- TEMA E CORES ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_input = "#0A122A" if is_dark else "#F5F7FA"
    cor_borda_input = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto = "white" if is_dark else "#1A1A1A"
    cor_label = ft.Colors.TEAL_400 if is_dark else ft.Colors.TEAL_800

    # --- DADOS INICIAIS DA SESSÃO ---
    try:
        user_id_inicial = str(page.session.get("user_id") if page.session.get("user_id") else "1")
        user_nome_inicial = str(page.session.get("user_nome") if page.session.get("user_nome") else "Admin")
    except:
        user_id_inicial = "1"
        user_nome_inicial = "Admin"

    data_agora = datetime.now().strftime("%d/%m/%Y")
    hora_agora = datetime.now().strftime("%H:%M")

    # --- FUNÇÃO DE ESTILO PARA CAMPOS ---
    def criar_campo_venda(label, icon, value="", read_only=False, hint=""):
        txt_field = ft.TextField(
            value=value,
            hint_text=hint,
            border=ft.InputBorder.NONE,
            text_style=ft.TextStyle(color=cor_texto, size=14),
            content_padding=15,
            read_only=read_only,
            cursor_color=cor_label,
            expand=True
        )
        return ft.Column([
            ft.Row([
                ft.Icon(icon, size=16, color=cor_label),
                ft.Text(label, size=12, weight="bold", color=cor_label),
            ], spacing=10),
            ft.Container(
                content=txt_field,
                bgcolor=cor_fundo_input,
                border=ft.border.all(1, cor_borda_input),
                border_radius=12,
            )
        ], spacing=8), txt_field

    # --- CAMPOS EDITÁVEIS ---
    col_user, input_user_id = criar_campo_venda("ID VENDEDOR", ft.Icons.PERSON, value=user_id_inicial)
    col_data, input_data = criar_campo_venda("DATA (DD/MM/AAAA)", ft.Icons.CALENDAR_MONTH, value=data_agora)
    col_hora, input_hora = criar_campo_venda("HORA (HH:MM)", ft.Icons.ACCESS_TIME, value=hora_agora)

    # --- PESQUISA INTELIGENTE DE PRODUTO (AutoComplete) ---
    produtos_db = buscar_produtos_estoque()
    # Mapeamento Nome -> ID
    mapa_produtos = {f"{p['nome_estoque']} (R$ {p['preco_venda']})": p['id_estoque'] for p in produtos_db if p['quantidade'] > 0}
    
    # Criando o componente AutoComplete corrigido
    ac_produto = ft.AutoComplete(
        suggestions=[ft.AutoCompleteSuggestion(key=nome, value=nome) for nome in mapa_produtos.keys()],
    )

    campo_produto = ft.Column([
        ft.Row([
            ft.Icon(ft.Icons.SEARCH, size=16, color=cor_label),
            ft.Text("PESQUISAR PRODUTO", size=12, weight="bold", color=cor_label),
        ], spacing=10),
        ft.Container(
            content=ac_produto,
            bgcolor=cor_fundo_input,
            border=ft.border.all(1, cor_borda_input),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=10, vertical=5)
        )
    ], spacing=8)

    # --- CAMPO PAGAMENTO ---
    drop_pagamento = ft.Dropdown(
        options=[ft.dropdown.Option("Dinheiro"), ft.dropdown.Option("PIX"), ft.dropdown.Option("Cartão")],
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(color=cor_texto),
        hint_text="Selecione o método...",
        expand=True
    )
    campo_pagamento = ft.Column([
        ft.Row([
            ft.Icon(ft.Icons.PAYMENTS, size=16, color=cor_label),
            ft.Text("MÉTODO DE PAGAMENTO", size=12, weight="bold", color=cor_label),
        ], spacing=10),
        ft.Container(
            content=drop_pagamento, 
            bgcolor=cor_fundo_input, 
            border=ft.border.all(1, cor_borda_input), 
            border_radius=12, 
            padding=ft.padding.symmetric(horizontal=10)
        )
    ], spacing=8)

    # --- APPBAR ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_voltar()),
        title=ft.Text("Nova Venda", weight="bold", color="white"),
        bgcolor="#0b1445",
    )

    def finalizar(e):
        # Validação do AutoComplete
        produto_selecionado = ac_produto.value
        
        if not produto_selecionado or produto_selecionado not in mapa_produtos:
            page.snack_bar = ft.SnackBar(ft.Text("Selecione um produto da lista!"), bgcolor="orange")
            page.snack_bar.open = True
            page.update()
            return

        if not drop_pagamento.value:
            page.snack_bar = ft.SnackBar(ft.Text("Escolha a forma de pagamento!"), bgcolor="orange")
            page.snack_bar.open = True
            page.update()
            return

        # Tentar converter a data digitada
        try:
            data_raw = input_data.value
            data_convertida = datetime.strptime(data_raw, "%d/%m/%Y").strftime("%Y-%m-%d")
        except:
            data_convertida = datetime.now().strftime("%Y-%m-%d")

        try:
            sucesso = registrar_venda_db(
                id_user=int(input_user_id.value),
                id_estoque=mapa_produtos[produto_selecionado],
                metodo_pagamento=drop_pagamento.value,
                data_venda=data_convertida
            )

            if sucesso:
                page.snack_bar = ft.SnackBar(ft.Text("Venda registrada com sucesso!"), bgcolor="green")
                page.snack_bar.open = True
                on_voltar()
            else:
                raise Exception("Erro no banco")
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao salvar: {ex}"), bgcolor="red")
            page.snack_bar.open = True
        
        page.update()

    # --- LAYOUT FINAL ---
    page.add(
        ft.Column([
            ft.Text("Checkout de Venda", size=24, weight="bold", color=cor_texto),
            ft.Text("Ajuste os dados se necessário e confirme a operação", size=14, color=ft.Colors.GREY_500),
            ft.Divider(height=20, color="transparent"),
            
            ft.ResponsiveRow([
                ft.Column([col_user], col={"sm": 12, "md": 4}),
                ft.Column([col_data], col={"sm": 6, "md": 4}),
                ft.Column([col_hora], col={"sm": 6, "md": 4}),
                ft.Column([campo_produto], col=12),
                ft.Column([campo_pagamento], col=12),
            ], run_spacing=20),
            
            ft.Divider(height=30, color="transparent"),
            
            ft.Row([
                ft.ElevatedButton(
                    "CONCLUIR VENDA",
                    icon=ft.Icons.CHECK_CIRCLE,
                    on_click=finalizar,
                    style=ft.ButtonStyle(
                        bgcolor="#1B4F9C",
                        color="white",
                        padding=25,
                        shape=ft.RoundedRectangleBorder(radius=12)
                    ),
                    expand=True
                ),
                ft.TextButton(
                    "CANCELAR",
                    on_click=lambda _: on_voltar(),
                    style=ft.ButtonStyle(color=ft.Colors.RED_400),
                )
            ], spacing=20)
        ])
    )
    page.update()