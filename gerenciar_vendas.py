import flet as ft
from database import buscar_vendas_detalhadas

def gerenciar_vendas(page: ft.Page, on_home, on_users, on_perfil, on_stock, on_registrar_venda, on_logout):
    page.controls.clear()
    page.padding = 20
    
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_container_bg = "#0b1445" if is_dark else "#F0F2F8"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = ft.Colors.GREY_500
    cor_fundo_busca = "#0d1626" if is_dark else "#FFFFFF"

    # Busca os dados no banco
    vendas_db = buscar_vendas_detalhadas()
    lista_vendas_ui = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)

    def formatar_moeda(valor):
        try:
            val = float(valor) if valor else 0.0
            return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except:
            return "0,00"

    def card_venda(id_venda, produto, valor_unitario, vendedor, data, qtd, metodo):
        # --- CORREÇÃO DA DATA ---
        # Definimos data_str antes de usá-la no ft.Text
        if data:
            try:
                data_str = data.strftime('%d/%m/%Y %H:%M') if hasattr(data, 'strftime') else str(data)
            except:
                data_str = str(data)
        else:
            data_str = "--/--/--"

        # 1. Garante que o valor unitário seja um número decimal
        try:
            v_unit = float(valor_unitario) if valor_unitario else 0.0
        except:
            v_unit = 0.0

        # 2. Garante que a quantidade seja um número inteiro (mínimo 1)
        try:
            q = int(qtd) if (qtd and int(qtd) > 0) else 1
        except:
            q = 1
            
        valor_total = v_unit * q
        
        return ft.Container(
            padding=15, border_radius=15, bgcolor=cor_container_bg,
            content=ft.Column(spacing=10, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Column([
                        ft.Text(f"VENDA #{id_venda} | {data_str}", 
                                size=10, color=cor_texto_secundario),
                        ft.Text(produto if produto else "Produto", size=18, weight="bold", color=cor_texto_principal),
                    ], spacing=2, expand=True),
                    ft.Column([
                        ft.Text(f"R$ {formatar_moeda(valor_total)}", weight="bold", size=18, color=ft.Colors.GREEN_ACCENT_400 if is_dark else ft.Colors.GREEN_700),
                        ft.Text(f"{q} UN x R$ {formatar_moeda(v_unit)}", size=11, color=cor_texto_secundario),
                    ], horizontal_alignment=ft.CrossAxisAlignment.END),
                ]),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Row([ft.Icon(ft.Icons.PERSON, size=14, color=cor_texto_secundario), ft.Text(f"Vendedor: {vendedor}", size=12, color=cor_texto_secundario)]),
                    ft.Container(
                        content=ft.Text(metodo.upper() if metodo else "PGTO", size=10, weight="bold", color="white"), 
                        bgcolor="#1B4F9C", 
                        padding=ft.padding.symmetric(horizontal=10, vertical=2), 
                        border_radius=10
                    ),
                ]),
            ])
        )

    def filtrar_vendas(e=None):
        texto = search_field.value.lower() if search_field.value else ""
        metodo_filtro = str(btn_filtro.data).lower()
        
        filtrados = [
            v for v in vendas_db 
            if (texto in (v.get("produto") or "").lower() or texto in (v.get("vendedor") or "").lower()) 
            and (metodo_filtro == "todos" or metodo_filtro in (v.get("metodo_pagamento") or "").lower())
        ]
        
        lista_vendas_ui.controls.clear()
        if not filtrados:
            lista_vendas_ui.controls.append(
                ft.Container(content=ft.Text("Nenhuma venda encontrada.", color=cor_texto_principal), padding=20)
            )
        else:
            for v in filtrados:
                lista_vendas_ui.controls.append(
                    card_venda(
                        v.get("id_venda"), 
                        v.get("produto"), 
                        v.get("preco_venda"), 
                        v.get("vendedor"), 
                        v.get("data_venda"), 
                        v.get("qtd_venda") or v.get("quantidade"),
                        v.get("metodo_pagamento")
                    )
                )
        if page: page.update()

    def mudar_f(m): 
        btn_filtro.data = m
        filtrar_vendas()

    btn_filtro = ft.PopupMenuButton(
        icon=ft.Icons.FILTER_LIST, 
        items=[
            ft.PopupMenuItem(content=ft.Text("Todas"), on_click=lambda _: mudar_f("todos")),
            ft.PopupMenuItem(content=ft.Text("Pix"), on_click=lambda _: mudar_f("pix")),
            ft.PopupMenuItem(content=ft.Text("Dinheiro"), on_click=lambda _: mudar_f("dinheiro")),
            ft.PopupMenuItem(content=ft.Text("Cartão"), on_click=lambda _: mudar_f("crédito")),
        ]
    )
    btn_filtro.data = "todos"
    
    search_field = ft.TextField(
        hint_text="Buscar produto ou vendedor...", 
        expand=True, 
        on_change=filtrar_vendas, 
        bgcolor=cor_fundo_busca, 
        border_radius=15, 
        prefix_icon=ft.Icons.SEARCH
    )

    page.appbar = ft.AppBar(
        bgcolor="#0b1445", 
        title=ft.Text("Histórico de Vendas", color="white", weight="bold"),
        center_title=True
    )
    
    page.add(
        ft.Column(
            expand=True, 
            spacing=15, 
            controls=[
                ft.Row([
                    ft.Text("Histórico de Vendas", size=22, weight="bold", color=cor_texto_principal),
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        bgcolor="#1B4F9C",
                        mini=True,
                        tooltip="Nova Venda",
                        on_click=lambda _: on_registrar_venda()
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([search_field, btn_filtro]), 
                lista_vendas_ui
            ]
        )
    )
    
    def trocar_aba(e):
        idx = e.control.selected_index
        if idx == 0: on_home()
        elif idx == 1: pass 
        elif idx == 2: on_stock()
        elif idx == 3: on_users()
        elif idx == 4: on_perfil()

    page.navigation_bar = ft.Container(
        content=ft.NavigationBar(
            bgcolor="#0b1445", selected_index=1, on_change=trocar_aba,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicial"),
                ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"),
                ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"),
                ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Usuários"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
            ]
        ),
        margin=ft.margin.only(left=25, right=25, bottom=30),
        border_radius=40, clip_behavior=ft.ClipBehavior.ANTI_ALIAS
    )

    filtrar_vendas()