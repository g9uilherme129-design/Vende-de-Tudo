import flet as ft
from database import registrar_venda_db, buscar_produtos_estoque
from datetime import datetime

def tela_registrar_venda(page: ft.Page, on_voltar):
    page.controls.clear()
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.navigation_bar = None 

    # --- TEMA E CORES (PADRÃO SEU) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_input = "#0A122A" if is_dark else "#F5F7FA"
    cor_borda_input = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto = "white" if is_dark else "#1A1A1A"
    cor_label = ft.Colors.TEAL_400 if is_dark else ft.Colors.TEAL_800

    # --- ESTADO DO CARRINHO ---
    carrinho = []
    produtos_db = buscar_produtos_estoque()
    mapa_produtos = {f"{p['nome_estoque']} (R$ {p['preco_venda']})": p for p in produtos_db if p['quantidade'] > 0}

    # --- CORREÇÃO DA SESSÃO ---
    try:
        # Tenta pegar o ID de quem logou, se não houver ninguém, 
        # usa um ID que EXISTE no banco (u789521) em vez de "1"
        user_id_inicial = str(page.session.get("user_id") or "u789521")
    except:
        try:
            user_id_inicial = str(page.session.get_item("user_id") or "u789521")
        except:
            user_id_inicial = "u789521"

    data_agora = datetime.now().strftime("%d/%m/%Y")
    hora_agora = datetime.now().strftime("%H:%M")

    # --- COMPONENTES DE UI ---
    txt_total = ft.Text("R$ 0,00", size=35, weight="bold", color=cor_label)
    lista_itens_ui = ft.Column(spacing=10)

    input_user_id = ft.TextField(value=user_id_inicial, label="ID Vendedor", bgcolor=cor_fundo_input, border_color=cor_borda_input, expand=True)
    input_data = ft.TextField(value=data_agora, label="Data", bgcolor=cor_fundo_input, border_color=cor_borda_input, expand=True)
    input_hora = ft.TextField(value=hora_agora, label="Hora", bgcolor=cor_fundo_input, border_color=cor_borda_input, expand=True)
    
    input_qtd = ft.TextField(value="1", label="Qtd", width=80, text_align="center", bgcolor=cor_fundo_input, border_color=cor_borda_input)
    
    ac_produto = ft.AutoComplete(
        suggestions=[ft.AutoCompleteSuggestion(key=nome, value=nome) for nome in mapa_produtos.keys()],
    )

    drop_pagamento = ft.Dropdown(
        label="Método de Pagamento",
        options=[ft.dropdown.Option("Dinheiro"), ft.dropdown.Option("Pix"), ft.dropdown.Option("Crédito"), ft.dropdown.Option("Débito")],
        bgcolor=cor_fundo_input,
        border_color=cor_borda_input,
        expand=True
    )

    # --- LÓGICA ---
    def atualizar_resumo():
        total = sum(item['preco'] * item['qtd'] for item in carrinho)
        txt_total.value = f"R$ {total:.2f}"
        
        lista_itens_ui.controls.clear()
        for i, item in enumerate(carrinho):
            lista_itens_ui.controls.append(
                ft.Container(
                    bgcolor=cor_fundo_input,
                    padding=10,
                    border_radius=12,
                    border=ft.border.all(1, cor_borda_input),
                    content=ft.Row([
                        ft.Text(f"{item['qtd']}x", weight="bold", color=cor_label),
                        ft.Text(item['nome'], expand=True, color=cor_texto),
                        ft.Text(f"R$ {item['preco'] * item['qtd']:.2f}", weight="bold", color=cor_texto),
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
            quantidade = int(input_qtd.value)
        except:
            quantidade = 1

        carrinho.append({
            "id": prod['id_estoque'],
            "nome": prod['nome_estoque'],
            "preco": float(prod['preco_venda']),
            "qtd": quantidade
        })
        
        ac_produto.value = ""
        input_qtd.value = "1"
        atualizar_resumo()

    def remover_item(index):
        carrinho.pop(index)
        atualizar_resumo()

    
    def finalizar_venda(e):
        if not carrinho:
            page.snack_bar = ft.SnackBar(ft.Text("Carrinho vazio!"), bgcolor="orange")
            page.snack_bar.open = True
            page.update()
            return

        # REMOVIDO O int() -> O ID no banco é VARCHAR (ex: u789521)
        vendedor_id = input_user_id.value if input_user_id.value else "u789521"
        
        erros = []
        for item in carrinho:
            sucesso, msg = registrar_venda_db(
                id_user=vendedor_id,        # Agora passa a string correta
                id_estoque=item['id'],
                qtd=item['qtd'],
                metodo=drop_pagamento.value or "Dinheiro",
                preco_venda=item['preco']
            )
            
            if not sucesso:
                erros.append(f"Erro no item {item['nome']}: {msg}")

        if erros:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("\n".join(erros)),
                bgcolor=ft.Colors.RED_ACCENT_700,
                duration=5000
            )
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Venda concluída com sucesso!"), bgcolor="green")
            # Pequeno delay para o user ver o feedback antes de voltar
            page.update()
            import time
            time.sleep(1) 
            on_voltar()
            
        page.snack_bar.open = True
        page.update()

    # --- LAYOUT ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_voltar()),
        title=ft.Text("Finalizar Venda", weight="bold", color="white"),
        bgcolor="#0b1445",
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
                    ft.Text("Produtos", size=20, weight="bold", color=cor_texto),
                    ft.Row([
                        ft.Container(content=ac_produto, expand=True, bgcolor=cor_fundo_input, border_radius=10, padding=5),
                        input_qtd,
                        ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=adicionar_ao_carrinho, bgcolor=cor_label)
                    ]),
                    lista_itens_ui,
                ], expand=2),
                ft.Column([
                    ft.Container(
                        bgcolor=cor_fundo_input,
                        padding=25,
                        border_radius=20,
                        border=ft.border.all(1, cor_borda_input),
                        content=ft.Column([
                            ft.Text("TOTAL", size=12, color=cor_texto),
                            txt_total,
                            drop_pagamento,
                            ft.ElevatedButton(
                                "CONCLUIR", 
                                on_click=finalizar_venda,
                                bgcolor="#1B4F9C", 
                                color="white",
                                height=55,
                                expand=True
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                ], expand=1)
            ])
        ])
    )
    page.update()