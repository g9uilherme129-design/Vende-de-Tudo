import flet as ft
from database import registrar_venda_db, buscar_produtos_estoque
from datetime import datetime

def tela_registrar_venda(page: ft.Page, on_voltar):
    # --- FORMATAÇÃO MONETÁRIA BR ---
    def formatar_br(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    page.controls.clear()
    
    # --- PADRONIZAÇÃO DE CORES ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#0b1445" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_destaque = "#36D900" if is_dark else "#FF6C03"
    cor_input = "#0A122A" if is_dark else "#F5F7FB"

    # --- LOGICA DE DADOS ---
    carrinho = []
    produtos_db = buscar_produtos_estoque()
    mapa_produtos = {f"{p['nome_estoque']} ({formatar_br(p['preco_venda'])})": p for p in produtos_db if p['quantidade'] > 0}
    
    user_id_logado = page.user_data.get("id_user") if hasattr(page, "user_data") else "---"
    user_nome_logado = page.user_data.get("nome_user") if hasattr(page, "user_data") else "Vendedor"
    
    data_agora = datetime.now().strftime("%d/%m/%Y")
    hora_agora = datetime.now().strftime("%H:%M")

    # --- COMPONENTES ---
    txt_total = ft.Text(formatar_br(0), size=38, weight="bold", color=cor_destaque)
    lista_itens_ui = ft.Column(spacing=10)

    def estilo_input(label, value="", read_only=False, expand=False, width=None):
        return ft.TextField(
            label=label, value=value, read_only=read_only, expand=expand, width=width,
            bgcolor=cor_input, border_color=cor_borda, border_radius=12, color=cor_texto_p,
            label_style=ft.TextStyle(color=cor_texto_s),
            cursor_color=cor_texto_s,
            focused_border_color=cor_texto_s
        )

    input_user_id = estilo_input("ID Vendedor", value=str(user_id_logado), read_only=True, expand=True)
    input_data = estilo_input("Data", value=data_agora, read_only=True, expand=True)
    input_hora = estilo_input("Hora", value=hora_agora, read_only=True, expand=True)
    input_qtd = estilo_input("Qtd", value="1", width=80)
    
    ac_produto = ft.AutoComplete(
        suggestions=[ft.AutoCompleteSuggestion(key=nome, value=nome) for nome in mapa_produtos.keys()],
    )

    drop_pagamento = ft.Dropdown(
        label="Método de Pagamento",
        options=[ft.dropdown.Option("Dinheiro"), ft.dropdown.Option("Pix"), ft.dropdown.Option("Crédito"), ft.dropdown.Option("Débito")],
        bgcolor=cor_input, border_color=cor_borda, expand=True, value="Dinheiro", border_radius=12,
        color=cor_texto_p, label_style=ft.TextStyle(color=cor_texto_s)
    )

    # --- LISTA DE SELEÇÃO RÁPIDA (GRID) ---
    grid_produtos = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=150,
        child_aspect_ratio=0.8,
        spacing=10,
        run_spacing=10,
    )

    def atualizar_resumo():
        total = sum(item['preco'] * item['qtd'] for item in carrinho)
        txt_total.value = formatar_br(total)
        lista_itens_ui.controls.clear()
        for i, item in enumerate(carrinho):
            lista_itens_ui.controls.append(
                ft.Container(
                    bgcolor=cor_fundo_card, padding=15, border_radius=15, border=ft.border.all(1, cor_borda),
                    content=ft.Row([
                        ft.Text(f"{item['qtd']}x", weight="bold", color=cor_destaque, size=16),
                        ft.Text(item['nome'], expand=True, color=cor_texto_p),
                        ft.Text(formatar_br(item['preco'] * item['qtd']), weight="bold", color=cor_texto_p),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color="#B71C1C", on_click=lambda _, idx=i: remover_item(idx))
                    ])
                )
            )
        page.update()

    def adicionar_ao_carrinho(e, prod_rapido=None):
        if prod_rapido:
            prod = prod_rapido
        else:
            nome_sel = ac_produto.value
            if nome_sel not in mapa_produtos: return
            prod = mapa_produtos[nome_sel]
        
        try:
            q = int(input_qtd.value)
            if q <= 0: q = 1
        except: q = 1

        item_existente = next((item for item in carrinho if item["id"] == prod['id_estoque']), None)

        if item_existente:
            item_existente["qtd"] += q
        else:
            carrinho.append({
                "id": prod['id_estoque'], 
                "nome": prod['nome_estoque'], 
                "preco": float(prod['preco_venda']), 
                "qtd": q
            })

        ac_produto.value = ""
        input_qtd.value = "1"
        atualizar_resumo()

    def popular_grid():
        grid_produtos.controls.clear()
        for p in produtos_db:
            if p['quantidade'] > 0:
                grid_produtos.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.SHOPPING_BAG_OUTLINED, color=cor_texto_s, size=24),
                            ft.Text(p['nome_estoque'], size=11, weight="bold", text_align="center", max_lines=2),
                            ft.Text(formatar_br(p['preco_venda']), size=10, color=cor_destaque, weight="bold"),
                        ], alignment="center", horizontal_alignment="center", spacing=2),
                        bgcolor=cor_fundo_card,
                        padding=8,
                        border_radius=12,
                        border=ft.border.all(1, cor_borda),
                        on_click=lambda _, p=p: adicionar_ao_carrinho(None, prod_rapido=p)
                    )
                )

    def remover_item(index):
        carrinho.pop(index); atualizar_resumo()

    def finalizar_venda(e):
        if not carrinho: return
        for item in carrinho:
            registrar_venda_db(id_user=user_id_logado, id_estoque=item['id'], qtd=item['qtd'], metodo=drop_pagamento.value, preco_venda=item['preco'])
        
        page.snack_bar = ft.SnackBar(ft.Text("Venda Finalizada com Sucesso!", color="white"), bgcolor=cor_destaque)
        page.snack_bar.open = True
        on_voltar()

    # --- LAYOUT ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_voltar()),
        title=ft.Text(f"Nova Venda - {user_nome_logado}", weight="bold", color="white"),
        bgcolor=cor_barra, center_title=True
    )

    popular_grid()

    page.add(
        ft.Container(
            expand=True, bgcolor=cor_fundo_tela, padding=20,
            content=ft.ListView([ 
                ft.ResponsiveRow([
                    ft.Column([input_user_id], col={"sm": 12, "md": 4}),
                    ft.Column([input_data], col={"sm": 6, "md": 4}),
                    ft.Column([input_hora], col={"sm": 6, "md": 4}),
                ]),
                ft.Container(height=10),
                ft.Text("ITENS DO PEDIDO", size=12, weight="bold", color=cor_texto_s),
                ft.Row([
                    ft.Container(content=ac_produto, expand=True, bgcolor=cor_input, border_radius=12, padding=5, border=ft.border.all(1, cor_borda)),
                    input_qtd,
                    ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda e: adicionar_ao_carrinho(e), bgcolor=cor_texto_s)
                ]),
                ft.Container(height=10),
                
                ft.ResponsiveRow([
                    ft.Column([lista_itens_ui], col={"sm": 12, "md": 7}),
                    ft.Column([
                        # Bloco de Finalização
                        ft.Container(
                            bgcolor=cor_fundo_card, padding=25, border_radius=25, border=ft.border.all(1, cor_borda),
                            content=ft.Column([
                                ft.Text("TOTAL A PAGAR", size=11, color=cor_texto_s, weight="bold"),
                                txt_total,
                                ft.Divider(height=20, color=ft.Colors.WHITE10 if is_dark else ft.Colors.BLACK12),
                                drop_pagamento,
                                ft.Container(height=5),
                                ft.FilledButton(
                                    content=ft.Text("FINALIZAR VENDA", weight="bold", size=16),
                                    on_click=finalizar_venda,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE, bgcolor=cor_barra,
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                    ),
                                    height=55, width=400,
                                )
                            ], horizontal_alignment="center")
                        ),
                        ft.Container(height=20),
                        # Bloco de Seleção Rápida
                        ft.Text("PRODUTOS EM ESTOQUE", size=12, weight="bold", color=cor_texto_s),
                        ft.Container(
                            content=grid_produtos,
                            height=350, # Altura do scroll
                            padding=5,
                        )
                    ], col={"sm": 12, "md": 5}),
                ], spacing=20),
                ft.Container(height=100)
            ])
        )
    )
    page.update()