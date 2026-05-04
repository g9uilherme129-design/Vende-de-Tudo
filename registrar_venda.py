import flet as ft
from database import registrar_venda_db, buscar_produtos_estoque
from datetime import datetime

def tela_registrar_venda(page: ft.Page, on_voltar):
    # --- FORMATAÇÃO MONETÁRIA BR ---
    def formatar_br(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    page.controls.clear()
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    
    # --- CORES ESTILO HOME ---
    page.bgcolor = "#000000" if is_dark else "#F0F4FF"
    cor_fundo_card = "#0b1445" if is_dark else "#E1E8FA"
    cor_texto = "white" if is_dark else "#0b1445"
    cor_borda = "#1E2B4E" if is_dark else "#BCCAE3"
    cor_destaque = "#08D345" # Verde da Home
    cor_input = "#0A122A" if is_dark else "#FFFFFF"

    # --- LOGICA DE DADOS ---
    carrinho = []
    produtos_db = buscar_produtos_estoque()
    mapa_produtos = {f"{p['nome_estoque']} ({formatar_br(p['preco_venda'])})": p for p in produtos_db if p['quantidade'] > 0}
    dados_logado = getattr(page, "data", {}) or {}
    user_id_logado = dados_logado.get("user_id")
    user_nome_logado = dados_logado.get("user_nome") or "Vendedor"
    data_agora = datetime.now().strftime("%d/%m/%Y")
    hora_agora = datetime.now().strftime("%H:%M")

    # --- COMPONENTES ---
    txt_total = ft.Text(formatar_br(0), size=38, weight="bold", color=cor_destaque)
    lista_itens_ui = ft.Column(spacing=10)

    def estilo_input(label, value="", read_only=False, expand=False, width=None):
        return ft.TextField(
            label=label, value=value, read_only=read_only, expand=expand, width=width,
            bgcolor=cor_input, border_color=cor_borda, border_radius=12, color=cor_texto,
            label_style=ft.TextStyle(color=ft.Colors.BLUE_200 if is_dark else ft.Colors.BLUE_900)
        )

    input_user_id = estilo_input("ID Vendedor", value=str(user_id_logado) if user_id_logado else "NÃO IDENTIFICADO", read_only=True, expand=True)
    input_data = estilo_input("Data", value=data_agora, read_only=True, expand=True)
    input_hora = estilo_input("Hora", value=hora_agora, read_only=True, expand=True)
    input_qtd = estilo_input("Qtd", value="1", width=80)
    
    ac_produto = ft.AutoComplete(
        suggestions=[ft.AutoCompleteSuggestion(key=nome, value=nome) for nome in mapa_produtos.keys()],
    )

    drop_pagamento = ft.Dropdown(
        label="Método de Pagamento",
        options=[ft.dropdown.Option("Dinheiro"), ft.dropdown.Option("Pix"), ft.dropdown.Option("Crédito"), ft.dropdown.Option("Débito")],
        bgcolor=cor_input, border_color=cor_borda, expand=True, value="Dinheiro", border_radius=12
    )

    def atualizar_resumo():
        total = sum(item['preco'] * item['qtd'] for item in carrinho)
        txt_total.value = formatar_br(total)
        lista_itens_ui.controls.clear()
        for i, item in enumerate(carrinho):
            lista_itens_ui.controls.append(
                ft.Container(
                    bgcolor=cor_input, padding=15, border_radius=15, border=ft.border.all(1, cor_borda),
                    content=ft.Row([
                        ft.Text(f"{item['qtd']}x", weight="bold", color=cor_destaque, size=16),
                        ft.Text(item['nome'], expand=True, color=cor_texto),
                        ft.Text(formatar_br(item['preco'] * item['qtd']), weight="bold", color=cor_texto),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color="red", on_click=lambda _, idx=i: remover_item(idx))
                    ])
                )
            )
        page.update()

    def adicionar_ao_carrinho(e):
        nome_sel = ac_produto.value
        if nome_sel not in mapa_produtos: 
            return
        
        prod = mapa_produtos[nome_sel]
        
        try:
            q = int(input_qtd.value)
            if q <= 0: q = 1
        except: 
            q = 1

        # --- LÓGICA DE MESCLAGEM ---
        # Procurar se o produto já existe no carrinho
        item_existente = next((item for item in carrinho if item["id"] == prod['id_estoque']), None)

        if item_existente:
            # Se já existe, apenas soma a quantidade
            item_existente["qtd"] += q
        else:
            # Se não existe, adiciona um novo dicionário
            carrinho.append({
                "id": prod['id_estoque'], 
                "nome": prod['nome_estoque'], 
                "preco": float(prod['preco_venda']), 
                "qtd": q
            })

        # Limpa os campos e atualiza a interface
        ac_produto.value = ""
        input_qtd.value = "1"
        atualizar_resumo()

    def remover_item(index):
        carrinho.pop(index); atualizar_resumo()

    def finalizar_venda(e):
        if not carrinho: return
        for item in carrinho:
            registrar_venda_db(id_user=input_user_id.value, id_estoque=item['id'], qtd=item['qtd'], metodo=drop_pagamento.value, preco_venda=item['preco'])
        page.snack_bar = ft.SnackBar(ft.Text("Venda Finalizada!"), bgcolor=cor_destaque)
        page.snack_bar.open = True
        on_voltar()

    # --- LAYOUT ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_voltar()),
        title=ft.Text(f"Venda - {user_nome_logado}", weight="bold", color="white"),
        bgcolor="#0b1445", center_title=True
    )

    page.add(
        ft.Column([
            ft.ResponsiveRow([
                ft.Column([input_user_id], col={"sm": 12, "md": 4}),
                ft.Column([input_data], col={"sm": 6, "md": 4}),
                ft.Column([input_hora], col={"sm": 6, "md": 4}),
            ]),
            ft.Row([
                ft.Column([
                    ft.Text("ITENS DO PEDIDO", size=14, weight="bold", color=cor_texto),
                    ft.Row([
                        ft.Container(content=ac_produto, expand=True, bgcolor=cor_input, border_radius=12, padding=5),
                        input_qtd,
                        ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=adicionar_ao_carrinho, bgcolor=cor_destaque)
                    ]),
                    lista_itens_ui,
                ], expand=2),
                ft.Column([
                    ft.Container(
                        bgcolor=cor_fundo_card, padding=30, border_radius=25, border=ft.border.all(1, cor_borda),
                        content=ft.Column([
                            ft.Text("TOTAL", size=12, color=ft.Colors.BLUE_200, weight="bold"),
                            txt_total,
                            ft.Divider(height=20, color="transparent"),
                            drop_pagamento,
                            ft.ElevatedButton(
                                "FINALIZAR VENDA", on_click=finalizar_venda,
                                bgcolor="#1B4F9C", color="white", height=60, width=300,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
                            ),
                        ], horizontal_alignment="center")
                    )
                ], expand=1)
            ], vertical_alignment=ft.CrossAxisAlignment.START, spacing=20)
        ], spacing=20)
    )
    page.update()