import flet as ft
from database import atualizar_venda_db, buscar_venda_por_id, excluir_item_venda_db
from datetime import datetime

def editar_venda(page: ft.Page, id_venda, on_back):
    # --- FORMATAÇÃO MONETÁRIA BR ---
    def formatar_br(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    page.controls.clear()
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    
    # --- CORES ---
    page.bgcolor = "#000000" if is_dark else "#F0F4FF"
    cor_fundo_card = "#0b1445" if is_dark else "#E1E8FA"
    cor_texto = "white" if is_dark else "#0b1445"
    cor_texto_secundario = ft.Colors.GREY_500 # DEFINIDA AQUI
    cor_borda = "#1E2B4E" if is_dark else "#BCCAE3"
    cor_destaque = "#08D345" 
    cor_input = "#0A122A" if is_dark else "#FFFFFF"

    # --- BUSCA DADOS DA VENDA ---
    venda_atual = buscar_venda_por_id(id_venda)
    
    if not venda_atual:
        page.snack_bar = ft.SnackBar(ft.Text("Venda não encontrada!"), bgcolor="red")
        page.snack_bar.open = True
        on_back()
        return

    # Usando .get(chave, valor_padrao) para evitar KeyError
    preco_unitario = float(venda_atual.get('preco_venda', 0))
    quantidade_atual = int(venda_atual.get('quantidade', 0))
    nome_produto = venda_atual.get('produto', 'Produto não encontrado')

    # --- COMPONENTES ---
    txt_total = ft.Text(
        formatar_br(preco_unitario * quantidade_atual), 
        size=38, weight="bold", color=cor_destaque
    )

    def estilo_input(label, value="", read_only=False, expand=False, width=None):
        return ft.TextField(
            label=label, value=value, read_only=read_only, expand=expand, width=width,
            bgcolor=cor_input, border_color=cor_borda, border_radius=12, color=cor_texto,
            label_style=ft.TextStyle(color=ft.Colors.BLUE_200 if is_dark else ft.Colors.BLUE_900)
        )

    input_venda_id = estilo_input("ID Venda", value=str(id_venda), read_only=True, expand=True)
    input_vendedor = estilo_input("Vendedor", value=venda_atual['vendedor'], read_only=True, expand=True)
    input_produto = estilo_input("Produto", value=venda_atual['produto'], read_only=True, expand=True)
    
    input_qtd = ft.TextField(
        label="Quantidade", 
        value=str(venda_atual['quantidade']), 
        width=120,
        bgcolor=cor_input, border_color=cor_borda, border_radius=12, color=cor_texto,
        on_change=lambda _: atualizar_calculo_total()
    )

    drop_pagamento = ft.Dropdown(
        label="Método de Pagamento",
        options=[
            ft.dropdown.Option("Dinheiro"), 
            ft.dropdown.Option("Pix"), 
            ft.dropdown.Option("Crédito"), 
            ft.dropdown.Option("Débito")
        ],
        bgcolor=cor_input, border_color=cor_borda, expand=True, 
        value=venda_atual['metodo_pagamento'], border_radius=12
    )

    def atualizar_calculo_total():
        try:
            q = int(input_qtd.value) if input_qtd.value else 0
            novo_total = q * float(venda_atual['preco_venda'])
            txt_total.value = formatar_br(novo_total)
        except:
            txt_total.value = formatar_br(0)
        page.update()

    def salvar_edicao(e):
        try:
            nova_qtd = int(input_qtd.value)
            if nova_qtd <= 0: raise ValueError
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Quantidade inválida!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        sucesso, msg = atualizar_venda_db(id_venda, nova_qtd, drop_pagamento.value)
        if sucesso:
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=cor_destaque)
            on_back() # Volta para a tela de histórico
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {msg}"), bgcolor="red")
        
        page.snack_bar.open = True
        page.update()

    def excluir_venda(e):
        def confirmar_exclusao(confirma):
            if confirma:
                sucesso, msg = excluir_item_venda_db(id_venda)
                if sucesso:
                    page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="red")
                    on_back()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {msg}"))
                page.snack_bar.open = True
            dlg_modal.open = False
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text("Deseja realmente excluir esta venda? O estoque será devolvido."),
            actions=[
                ft.TextButton("Não", on_click=lambda _: confirmar_exclusao(False)),
                ft.TextButton("Sim, Excluir", on_click=lambda _: confirmar_exclusao(True), icon_color="red"),
            ],
        )
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    # --- LAYOUT ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_back()),
        title=ft.Text(f"Editar Venda #{id_venda}", weight="bold", color="white"),
        bgcolor="#0b1445", center_title=True
    )

    page.add(
        ft.Column([
            ft.ResponsiveRow([
                ft.Column([input_venda_id], col={"sm": 12, "md": 4}),
                ft.Column([input_vendedor], col={"sm": 12, "md": 4}),
                ft.Column([input_produto], col={"sm": 12, "md": 4}),
            ]),
            
            ft.Row([
                ft.Column([
                    ft.Text("DADOS DA VENDA", size=14, weight="bold", color=cor_texto),
                    ft.Container(
                        bgcolor=cor_input, padding=20, border_radius=15, border=ft.border.all(1, cor_borda),
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.INVENTORY, color=cor_destaque), 
                                ft.Text(venda_atual['produto'], size=20, weight="bold", color=cor_texto)
                            ]),
                            ft.Divider(color=cor_borda),
                            ft.Row([
                                input_qtd,
                                ft.Text(f"x {formatar_br(venda_atual['preco_venda'])} (Unitário)", color=cor_texto_secundario)
                            ]),
                        ])
                    ),
                    ft.Container(padding=10), # Espaçador
                    ft.ElevatedButton(
                        "EXCLUIR / CANCELAR VENDA", 
                        icon=ft.Icons.DELETE_FOREVER,
                        on_click=excluir_venda,
                        color="red", bgcolor=ft.Colors.with_opacity(0.1, "red"),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                    )
                ], expand=2),
                
                ft.Column([
                    ft.Container(
                        bgcolor=cor_fundo_card, padding=30, border_radius=25, border=ft.border.all(1, cor_borda),
                        content=ft.Column([
                            ft.Text("VALOR ATUALIZADO", size=12, color=ft.Colors.BLUE_200, weight="bold"),
                            txt_total,
                            ft.Divider(height=20, color="transparent"),
                            drop_pagamento,
                            ft.ElevatedButton(
                                "SALVAR ALTERAÇÕES", on_click=salvar_edicao,
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