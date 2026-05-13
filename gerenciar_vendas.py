import flet as ft
from database import buscar_vendas_detalhadas

def gerenciar_vendas(page: ft.Page, on_home, on_users, on_perfil, on_stock, on_registrar_venda, on_editar_venda, on_logout):
    page.controls.clear()
    page.padding = 0 # Ajustado para o fundo cobrir tudo

    # --- PADRONIZAÇÃO DE CORES (IDÊNTICO AO SEU PERFIL) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#11259c" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_input = "#0A122A" if is_dark else "#F5F7FB"
    cor_secundaria =  "#1679f2" if is_dark else "#DA7D7D"
    cort_3 = "#36D900" if is_dark else "#FF6C03"
    cor_bar =  "#1679f2" if is_dark else "#BA7272"

    vendas_db = buscar_vendas_detalhadas()
    lista_vendas_ui = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)

    def formatar_moeda(valor):
        try:
            val = float(valor) if valor else 0.0
            return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except:
            return "0,00"

    def card_venda(id_venda, produto, valor_unitario, vendedor, data, qtd, metodo, categoria):
        if data:
            try:
                data_str = data.strftime('%d/%m/%Y %H:%M') if hasattr(data, 'strftime') else str(data)
            except:
                data_str = str(data)
        else:
            data_str = "--/--/--"

        v_unit = float(valor_unitario) if valor_unitario else 0.0
        q = int(qtd) if (qtd and int(qtd) > 0) else 1
        valor_total = v_unit * q
        cat_nome = str(categoria).upper() if categoria else "GERAL"
        
        return ft.Container(
            padding=15, 
            border_radius=15, 
            bgcolor=cor_fundo_card,
            border=ft.border.all(1, cor_borda),
            content=ft.Column(spacing=10, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Column([
                        ft.Text(f"VENDA #{id_venda} | {data_str} | {cat_nome}", 
                                size=10, color=cor_secundaria),
                        ft.Text(produto if produto else "Produto", size=18, weight="bold", color=cor_texto_p),
                    ], spacing=2, expand=True),
                    
                    ft.Row([
                        ft.Column([
                            ft.Text(f"R$ {formatar_moeda(valor_total)}", weight="bold", size=18, 
                                    color=cort_3),
                            ft.Text(f"{q} UN x R$ {formatar_moeda(v_unit)}", size=11, color=cor_secundaria),
                        ], horizontal_alignment=ft.CrossAxisAlignment.END),
                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            icon_color=cor_texto_s,
                            tooltip="Editar Venda",
                            on_click=lambda _: on_editar_venda(id_venda)
                        )
                    ], spacing=10)
                ]),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON, size=14, color=cor_secundaria), 
                        ft.Text(f"Vendedor: {vendedor}", size=12, color=cor_secundaria)
                    ]),
                    ft.Container(
                        content=ft.Text(metodo.upper() if metodo else "PGTO", size=10, weight="bold", color="white"), 
                        bgcolor=cor_texto_s, 
                        padding=ft.padding.symmetric(horizontal=10, vertical=2), 
                        border_radius=10
                    ),
                ]),
            ])
        )

    def filtrar_vendas(e=None):
        nonlocal vendas_db
        vendas_db = buscar_vendas_detalhadas() 
        texto = search_field.value.lower() if search_field.value else ""
        metodo_filtro = str(btn_filtro.data).lower()
        
        filtrados = [
            v for v in vendas_db 
            if (texto in (v.get("produto") or "").lower() or 
                texto in (v.get("vendedor") or "").lower() or
                texto in (v.get("categoria") or "").lower()) 
            and (metodo_filtro == "todos" or metodo_filtro in (v.get("metodo_pagamento") or "").lower())
        ]
        
        lista_vendas_ui.controls.clear()
        for v in filtrados:
            lista_vendas_ui.controls.append(
                card_venda(v.get("id_venda"), v.get("produto"), v.get("preco_venda"), 
                           v.get("vendedor"), v.get("data_venda"), v.get("qtd_venda"), 
                           v.get("metodo_pagamento"), v.get("categoria"))
            )
        page.update()

    def mudar_f(m): 
        btn_filtro.data = m
        filtrar_vendas()

    # --- ELEMENTOS DE UI PADRONIZADOS ---
    btn_filtro = ft.PopupMenuButton(
        icon=ft.Icons.FILTER_LIST, 
        icon_color=cor_texto_p,
        items=[
            ft.PopupMenuItem(content=ft.Text("Todas"), on_click=lambda _: mudar_f("todos")),
            ft.PopupMenuItem(content=ft.Text("Pix"), on_click=lambda _: mudar_f("pix")),
            ft.PopupMenuItem(content=ft.Text("Dinheiro"), on_click=lambda _: mudar_f("dinheiro")),
            ft.PopupMenuItem(content=ft.Text("Cartão"), on_click=lambda _: mudar_f("crédito")),
        ]
    )
    btn_filtro.data = "todos"
    
    search_field = ft.TextField(
        hint_text="Buscar venda...", 
        expand=True, 
        on_change=filtrar_vendas, 
        bgcolor=cor_input, 
        border_radius=15, 
        border_color=cor_borda,
        prefix_icon=ft.Icons.SEARCH,
        text_style=ft.TextStyle(color=cor_texto_p),
        hint_style=ft.TextStyle(color=cor_secundaria)
    )

    page.appbar = ft.AppBar(
        bgcolor=cor_barra, 
        title=ft.Text("Histórico de Vendas", color="white", weight="bold"),
        center_title=True
    )

    def trocar_aba(e):
        idx = e.control.selected_index
        if idx == 0: on_home()
        elif idx == 1: pass 
        elif idx == 2: on_stock()
        elif idx == 3: on_users()
        elif idx == 4: on_perfil()

    # --- BARRA DE NAVEGAÇÃO CUSTOMIZADA ---
    page.navigation_bar = ft.Container(
        content=ft.NavigationBar(
            bgcolor=cor_barra, 
            selected_index=1, 
            on_change=trocar_aba,
            indicator_color=cor_bar,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
                ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT, label="Vendas"),
                ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"),
                ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Usuários"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
            ]
        ),
        margin=ft.margin.only(left=25, right=25, bottom=20),
        border_radius=40, 
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS
    )

    # --- CONTEÚDO PRINCIPAL ---
    page.add(
        ft.Container(
            expand=True,
            bgcolor=cor_fundo_tela,
            padding=20,
            content=ft.Column(
                expand=True, 
                spacing=15, 
                controls=[
                    ft.Row([
                        ft.Text("Vendas Realizadas", size=24, weight="bold", color=cor_texto_p),
                        ft.FloatingActionButton(
                            icon=ft.Icons.ADD,
                            bgcolor=cor_texto_s,
                            tooltip="Registrar venda",
                            mini=True,
                            on_click=lambda _: on_registrar_venda()
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([search_field, btn_filtro]), 
                    lista_vendas_ui
                ]
            )
        )
    )
    
    filtrar_vendas()