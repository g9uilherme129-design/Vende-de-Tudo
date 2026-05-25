import flet as ft
from database import buscar_produtos_estoque, buscar_categorias 
from datetime import datetime
from navigation import build_navigation_bar

def estoque(page: ft.Page, on_home, on_users, on_perfil, on_vendas, on_adicionar_produto, on_editar_produto, on_logout, on_fornecedores, on_categorias, on_log=None):

    page.controls.clear()
    page.padding = 0 # Padding zero para o container de fundo preencher tudo
    
    # --- VERIFICAÇÃO DE CARGO ---
    perfil_usuario = getattr(page, "tipo_usuario", "VENDEDOR")
    
    # Limpa espaços e joga para maiúsculo para evitar erros de digitação no banco
    perfil_limpo = str(perfil_usuario).upper().strip()
    
    # Se for "ADMIN", e_vendedor será False. Se for qualquer outra coisa, será True.
    e_vendedor = (perfil_limpo != "ADMIN")

    # --- PADRONIZAÇÃO DE CORES (IDÊNTICO ÀS OUTRAS TELAS) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#050f44" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_input = "#0A122A" if is_dark else "#F5F7FB"
    cor_secundaria =  "#1679f2" if is_dark else "#DA7D7D"
    cor_bar =  "#1679f2" if is_dark else "#BA7272"
    cort_3 = "#36D900" if is_dark else "#FF6C03"

    # --- FUNÇÃO AUXILIAR DATA ---
    def formatar_data_br(data_origem):
        try:
            if hasattr(data_origem, 'strftime'):
                return data_origem.strftime("%d/%m/%Y")
            dt = datetime.strptime(str(data_origem), "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except:
            return str(data_origem)

    # --- BUSCA DADOS REAIS ---
    try:
        produtos_db = buscar_produtos_estoque()
        categorias_reais = buscar_categorias() 
    except:
        produtos_db = []
        categorias_reais = []

    lista_produtos_ui = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)

    # --- CARD PRODUTO ---
    def card_produto(id_prod, nome, preco, marca, validade, quantidade, categoria_nome="Geral"):
        if quantidade > 15: cor_status = "#00b40d"
        elif quantidade > 0: cor_status = "#ff4545"
        else: cor_status = "#ff4444"

        return ft.Container(
            padding=15, 
            border_radius=15, 
            bgcolor=cor_fundo_card,
            border=ft.border.all(1, cor_borda),
            content=ft.Column(spacing=10, controls=[
                ft.Row(alignment="spaceBetween", controls=[
                    ft.Column([
                        ft.Text(f"ID: {id_prod} | {categoria_nome.upper()}", size=10, color=cor_secundaria, weight="bold"),
                        ft.Text(nome, size=18, weight="bold", color=cor_texto_p),
                    ], spacing=2, expand=True),
                    ft.Column([
                        ft.Text(f"R$ {preco:.2f}", weight="bold", size=18, color=cort_3),
                        ft.Text(marca, size=11, color=cor_secundaria),
                    ], horizontal_alignment="end"),
                ]),
                ft.Row(alignment="spaceBetween", controls=[
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_MONTH_OUTLINED, size=14, color=cor_secundaria),
                        ft.Text(f"Validade: {validade}", size=11, color=cor_secundaria),
                    ], spacing=5),
                    ft.Container(
                        content=ft.Text(f"{quantidade} UN", size=11, weight="bold", color="white"),
                        bgcolor=cor_status, 
                        padding=ft.padding.symmetric(horizontal=12, vertical=4), 
                        border_radius=20,
                    ),
                ]),
                ft.Divider(height=1, color=ft.Colors.WHITE10),
                ft.Row(
                    alignment="end", 
                    controls=[
                        ft.TextButton(
                            "Editar Produto", 
                            icon=ft.Icons.EDIT_OUTLINED, 
                            icon_color=cor_texto_s,
                            on_click=lambda _: on_editar_produto(id_prod)
                        ),
                    ],
                    # MODIFICAÇÃO: Se for vendedor, a linha de ações do card some (não edita)
                    visible=not e_vendedor 
                ),
            ])
        )

    # --- LÓGICA FILTRAGEM ---
    def filtrar_estoque(e=None):
        texto = search_field.value.lower().strip() if search_field.value else ""
        criterio = btn_filtro.data

        # Usa .get e str(...) para evitar KeyError ou AttributeError quando campos faltarem
        filtrados = [
            p for p in produtos_db
            if texto in str(p.get("nome_estoque", "")).lower()
            or texto in str(p.get("marca", "")).lower()
            or texto in str(p.get("nome_categoria", "")).lower()
        ]

        if criterio == "caro":
            filtrados.sort(key=lambda x: x.get("preco_venda", 0), reverse=True)
        elif criterio == "barato":
            filtrados.sort(key=lambda x: x.get("preco_venda", 0))
        elif criterio == "estoque_baixo":
            filtrados.sort(key=lambda x: x.get("quantidade", 0))
        elif criterio != "todos":
            filtrados = [p for p in filtrados if p.get("nome_categoria") == criterio]

        lista_produtos_ui.controls.clear()
        for p in filtrados:
            fornecedor_real = p.get("nome_fornecedor") or p.get("marca") or "Sem Fornecedor"

            lista_produtos_ui.controls.append(
                card_produto(
                    p.get("id_estoque"),
                    p.get("nome_estoque", "Produto sem nome"),
                    p.get("preco_venda", 0.0),
                    fornecedor_real,
                    formatar_data_br(p.get("data_validade", "")),
                    p.get("quantidade", 0),
                    p.get("nome_categoria", "Geral")
                )
            )
        page.update()
        return filtrados
    def mudar_f(c): 
        btn_filtro.data = c
        filtrados = filtrar_estoque()

    # --- COMPONENTES ---
    menu_items = [
        ft.PopupMenuItem(content=ft.Text("Todos os Produtos"), on_click=lambda _: mudar_f("todos")),
        ft.PopupMenuItem(content=ft.Text("Mais Caro"), on_click=lambda _: mudar_f("caro")),
        ft.PopupMenuItem(content=ft.Text("Mais Barato"), on_click=lambda _: mudar_f("barato")),
        ft.PopupMenuItem(content=ft.Text("Estoque Baixo"), on_click=lambda _: mudar_f("estoque_baixo")),
    ]

    if categorias_reais:
        menu_items.append(ft.PopupMenuItem(content=ft.Divider(height=1)))
        for cat in categorias_reais:
            menu_items.append(ft.PopupMenuItem(content=ft.Text(cat), on_click=lambda e, c=cat: mudar_f(c)))

    btn_filtro = ft.PopupMenuButton(content=ft.Text("Filtro", color=cor_texto_p), tooltip="Filtro", items=menu_items)
    btn_filtro.data = "todos"

    search_field = ft.TextField(
        hint_text="Buscar no estoque...", expand=True, on_change=filtrar_estoque,
        bgcolor=cor_input, border_radius=15, prefix_icon=ft.Icons.SEARCH,
        border_color=cor_borda, text_style=ft.TextStyle(color=cor_texto_p)
    )

    page.appbar = ft.AppBar(
        bgcolor=cor_barra, 
        title=ft.Text("Gestão de Estoque", color="white", weight="bold"),
        center_title=True, 
        actions=[ft.IconButton(ft.Icons.EXIT_TO_APP, icon_color="white", on_click=lambda _: on_logout())]
    )

    # --- 1. CRIAÇÃO DA LISTA DE NAVEGAÇÃO DINÂMICA ---
    destinos_navegacao = [
        ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
    ]

    if not e_vendedor:
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"))
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2, label="Estoque"))
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Usuários"))
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Logs"))
    else:
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2, label="Estoque"))
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Logs"))

    destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"))

    # Descobre a posição real da aba "Estoque" para manter selecionada corretamente
    index_estoque = 0
    for i, d in enumerate(destinos_navegacao):
        if d.label == "Estoque":
            index_estoque = i
            break

    # --- 2. FUNÇÃO TROCAR_ABA DINÂMICA ---
    def trocar_aba(e):
        aba_selecionada = destinos_navegacao[e.control.selected_index].label
        if aba_selecionada == "Inicial": on_home()
        elif aba_selecionada == "Vendas": on_vendas()
        elif aba_selecionada == "Estoque": pass
        elif aba_selecionada == "Usuários": on_users()
        elif aba_selecionada == "Perfil": on_perfil()
        elif aba_selecionada == "Logs":
            if on_log:
                on_log()

    build_navigation_bar(
        page=page,
        selected_label="Estoque",
        is_admin=not e_vendedor,
        callbacks={
            "on_home": on_home,
            "on_vendas": on_vendas,
            "on_stock": lambda: None,
            "on_users": on_users,
            "on_log": on_log,
            "on_perfil": on_perfil,
        },
        bgcolor=cor_barra,
        indicator_color=cor_bar,
    )

    # --- 3. CONTAINER DE BOTÕES DE AÇÃO FILTRADO ---
    botoes_acoes = ft.Row(spacing=5)
    
    # Só insere os botões de gerenciamento se NÃO for vendedor
    if not e_vendedor:
        botoes_acoes.controls.extend([
            ft.IconButton(
                icon=ft.Icons.CATEGORY_ROUNDED,
                icon_color=cor_texto_s,
                tooltip="Categorias",
                on_click=lambda _: on_categorias()
            ),
            ft.IconButton(
                icon=ft.Icons.BUSINESS,
                icon_color=cor_texto_s,
                tooltip="Fornecedores",
                on_click=lambda _: on_fornecedores()
            ),
            ft.FloatingActionButton(
                icon=ft.Icons.ADD, 
                bgcolor=cor_texto_s, 
                tooltip="Novo Produto",
                mini=True, 
                on_click=lambda _: on_adicionar_produto()
            ),
        ])

    page.add(
        ft.Container(
            expand=True, bgcolor=cor_fundo_tela, padding=20,
            content=ft.Column(expand=True, spacing=15, controls=[
                ft.Row([
                    ft.Text("Meus Produtos", size=24, weight="bold", color=cor_texto_p),
                    botoes_acoes # Passa o container contendo os botões (ou vazio se for vendedor)
                ], alignment="spaceBetween"),
                ft.Row([search_field, btn_filtro]),
                lista_produtos_ui
            ])
        )
    )
    
    filtrar_estoque()