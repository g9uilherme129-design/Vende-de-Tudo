import flet as ft
from database import buscar_categorias_detalhado, salvar_categoria_db, editar_categoria_db, alterar_status_categoria_db

def gerenciar_categorias(page: ft.Page, on_back):
    page.controls.clear()
    page.padding = 0

    # --- PADRONIZAÇÃO DE CORES ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#0b1445" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_input = "#0A122A" if is_dark else "#F5F7FB"
    cor_secundaria =  "#1679f2" if is_dark else "#DA7D7D"
    cor_bar =  "#1679f2" if is_dark else "#BA7272"
    
    categorias_base = []
    lista_categorias_ui = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)

    # --- CARD DE CATEGORIA ---
    def criar_card_categoria(c):
        status = c.get("status", "Ativo")
        esta_ativo = status == "Ativo"
        cor_status = "#00b40d" if esta_ativo else "#ff4444"
        
        return ft.Container(
            bgcolor=cor_fundo_card,
            border_radius=15,
            padding=15,
            border=ft.border.all(1, cor_borda),
            content=ft.Row([
                ft.Icon(ft.Icons.CATEGORY_ROUNDED, color=cor_texto_s),
                ft.Column([
                    ft.Text(c["nome_categoria"].upper(), size=16, weight="bold", color=cor_texto_p),
                    ft.Text(f"ID: {c['id_categoria']}", size=11, color=cor_secundaria),
                ], expand=True),
                ft.Container(
                    content=ft.Text(status.upper(), size=10, weight="bold", color="white"),
                    bgcolor=cor_status,
                    padding=ft.padding.symmetric(horizontal=10, vertical=2),
                    border_radius=10
                ),
                ft.IconButton(
                    icon=ft.Icons.EDIT_OUTLINED,
                    icon_color=cor_texto_s,
                    on_click=lambda _: abrir_modal_edicao(c)
                ),
                ft.IconButton(
                    icon=ft.Icons.POWER_SETTINGS_NEW,
                    icon_color=ft.Colors.RED_400 if esta_ativo else ft.Colors.GREEN_400,
                    on_click=lambda _: alternar_status(c["id_categoria"], status)
                ),
            ])
        )

    # --- LÓGICA ---
    def carregar_dados():
        nonlocal categorias_base
        categorias_base = buscar_categorias_detalhado()
        filtrar_categorias()

    def filtrar_categorias(e=None):
        texto = search_field.value.lower() if search_field.value else ""
        criterio = btn_filtro.data
        
        filtrados = [c for c in categorias_base if texto in c["nome_categoria"].lower()]
        if criterio != "todos":
            filtrados = [c for c in filtrados if c.get("status") == criterio]

        lista_categorias_ui.controls.clear()
        for c in filtrados:
            lista_categorias_ui.controls.append(criar_card_categoria(c))
        page.update()

    def mudar_filtro(f):
        btn_filtro.data = f
        filtrar_categorias()

    def alternar_status(id_cat, status_atual):
        novo = "Inativo" if status_atual == "Ativo" else "Ativo"
        alterar_status_categoria_db(id_cat, novo)
        carregar_dados()

    # --- MODAIS (ADICIONAR / EDITAR) ---
    def abrir_modal_novo(e):
        nome_input = ft.TextField(
            label="Nome da Categoria", 
            border_radius=10,
            border_color=cor_borda,
            bgcolor=cor_input,
            color=cor_texto_p
        )
        
        def salvar(e):
            if nome_input.value:
                salvar_categoria_db(nome_input.value)
                dlg.open = False
                carregar_dados()

        dlg = ft.AlertDialog(
            bgcolor=cor_fundo_card,
            title=ft.Text("Nova Categoria", color=cor_texto_p),
            content=nome_input,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: setattr(dlg, "open", False)),
                ft.ElevatedButton("Salvar", bgcolor=cor_texto_s, color="white", on_click=salvar)
            ]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def abrir_modal_edicao(cat):
        nome_edit = ft.TextField(
            label="Nome", 
            value=cat["nome_categoria"], 
            border_radius=10,
            border_color=cor_borda,
            bgcolor=cor_input,
            color=cor_texto_p
        )
        
        def atualizar(e):
            editar_categoria_db(cat["id_categoria"], nome_edit.value)
            dlg.open = False
            carregar_dados()

        dlg = ft.AlertDialog(
            bgcolor=cor_fundo_card,
            title=ft.Text("Editar Categoria", color=cor_texto_p),
            content=nome_edit,
            actions=[
                ft.ElevatedButton("Atualizar", bgcolor=cor_texto_s, color="white", on_click=atualizar)
            ]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # --- UI COMPONENTS ---
    search_field = ft.TextField(
        hint_text="Buscar categoria...", expand=True, on_change=filtrar_categorias,
        bgcolor=cor_input, border_radius=15, prefix_icon=ft.Icons.SEARCH,
        border_color=cor_borda, text_style=ft.TextStyle(color=cor_texto_p)
    )

    btn_filtro = ft.PopupMenuButton(
        icon=ft.Icons.FILTER_ALT_OUTLINED,
        icon_color=cor_bar,
        items=[
            ft.PopupMenuItem(content=ft.Text("Todas"), on_click=lambda _: mudar_filtro("todos")),
            ft.PopupMenuItem(content=ft.Text("Ativas"), on_click=lambda _: mudar_filtro("Ativo")),
            ft.PopupMenuItem(content=ft.Text("Inativas"), on_click=lambda _: mudar_filtro("Inativo")),
        ]
    )
    btn_filtro.data = "todos"

    # --- LAYOUT ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color="white", on_click=lambda _: on_back()),
        bgcolor=cor_barra,
        title=ft.Text("Categorias", color="white", weight="bold"),
        center_title=True,
    )

    page.add(
        ft.Container(
            expand=True, bgcolor=cor_fundo_tela, padding=20,
            content=ft.Column(expand=True, controls=[
                ft.Row([
                    ft.Text("Gestão de Categorias", size=24, weight="bold", color=cor_texto_p),
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, 
                        bgcolor=cor_texto_s, 
                        mini=True, 
                        on_click=abrir_modal_novo
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([search_field, btn_filtro]),
                lista_categorias_ui
            ])
        )
    )
    
    carregar_dados()