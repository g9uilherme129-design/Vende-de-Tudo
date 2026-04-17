import flet as ft
from database import buscar_categorias_detalhado, salvar_categoria_db, editar_categoria_db, alterar_status_categoria_db

def gerenciar_categorias(page: ft.Page, on_back):
    page.controls.clear()
    
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_container_bg = "#0b1445" if is_dark else "#F0F2F8"
    cor_fundo_busca = "#0d1626" if is_dark else "#FFFFFF"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    
    # Lista global para esta tela para evitar consultas repetidas ao banco durante a busca
    categorias_base = []
    lista_categorias_ui = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)

    # --- LÓGICA DE FILTRAGEM ---
    def filtrar_categorias(e=None):
        texto = search_field.value.lower()
        criterio = btn_filtro.data  # "todos", "Ativo" ou "Inativo"
        
        filtrados = [
            cat for cat in categorias_base 
            if texto in cat["nome_categoria"].lower()
        ]

        if criterio != "todos":
            filtrados = [cat for cat in filtrados if cat["status"] == criterio]

        lista_categorias_ui.controls.clear()
        for d in filtrados:
            lista_categorias_ui.controls.append(
                card_categoria(d['id_categoria'], d['nome_categoria'], d['status'])
            )
        page.update()

    def mudar_filtro(status_selecionado):
        btn_filtro.data = status_selecionado
        filtrar_categorias()

    # --- COMPONENTES DE BUSCA ---
    search_field = ft.TextField(
        hint_text="Buscar categoria...", 
        expand=True, 
        on_change=filtrar_categorias, # Filtra enquanto digita
        bgcolor=cor_fundo_busca, 
        border_radius=15, 
        prefix_icon=ft.Icons.SEARCH,
        border=ft.border.all(1, "#1E2B4E" if is_dark else "#D1D5DB")
    )

    btn_filtro = ft.PopupMenuButton(
        icon=ft.Icons.FILTER_LIST,
        items=[
            ft.PopupMenuItem(content=ft.Text("Todas"), on_click=lambda _: mudar_filtro("todos")),
            ft.PopupMenuItem(content=ft.Text("Apenas Ativas"), on_click=lambda _: mudar_filtro("Ativo")),
            ft.PopupMenuItem(content=ft.Text("Apenas Inativas"), on_click=lambda _: mudar_filtro("Inativo")),
        ]
    )
    btn_filtro.data = "todos" # Valor inicial

    # --- FUNÇÃO PARA ABRIR MODAL ---
    def abrir_modal_categoria(id_cat=None, nome_atual=""):
        txt_nome = ft.TextField(label="Nome da Categoria", value=nome_atual, autofocus=True)
        
        def salvar(e):
            if not txt_nome.value: return
            if id_cat:
                editar_categoria_db(id_cat, txt_nome.value)
            else:
                salvar_categoria_db(txt_nome.value)
            dialog.open = False
            carregar_categorias() # Recarrega a base e a UI
        
        dialog = ft.AlertDialog(
            title=ft.Text("Nova Categoria" if not id_cat else "Editar Categoria"),
            content=txt_nome,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: setattr(dialog, "open", False) or page.update()),
                ft.ElevatedButton("Salvar", on_click=salvar, bgcolor="#1B4F9C", color="white")
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # --- CARD DE CATEGORIA ---
    def card_categoria(id_cat, nome, status):
        cor_status = "#00b40d" if status == "Ativo" else "#ff4444"
        
        return ft.Container(
            padding=15, border_radius=15, bgcolor=cor_container_bg,
            content=ft.Row(alignment="spaceBetween", controls=[
                ft.Column([
                    ft.Text(f"ID: {id_cat}", size=10, color=ft.Colors.GREY_500),
                    ft.Text(nome, size=18, weight="bold", color=cor_texto_principal),
                    ft.Row([
                        ft.Container(bgcolor=cor_status, width=10, height=10, border_radius=5),
                        ft.Text(status, size=12, color=cor_status)
                    ])
                ], spacing=5),
                ft.Row([
                    ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE_400, 
                                  on_click=lambda _: abrir_modal_categoria(id_cat, nome)),
                    ft.IconButton(
                        ft.Icons.POWER_SETTINGS_NEW, 
                        icon_color=ft.Colors.RED_400 if status == "Ativo" else ft.Colors.GREEN_400,
                        on_click=lambda _: alternar_status(id_cat, status)
                    ),
                ])
            ])
        )

    def alternar_status(id_cat, status_atual):
        novo = "Inativo" if status_atual == "Ativo" else "Ativo"
        alterar_status_categoria_db(id_cat, novo)
        carregar_categorias()

    def carregar_categorias():
        nonlocal categorias_base
        categorias_base = buscar_categorias_detalhado()
        filtrar_categorias() # Atualiza a UI respeitando a busca/filtro atual

    # --- LAYOUT DA PÁGINA ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_back()),
        bgcolor="#0b1445",
        title=ft.Text("Gerenciar Categorias", color="white", weight="bold"),
        center_title=True
    )

    page.add(
        ft.Column(expand=True, controls=[
            ft.Row([
                ft.Text("Categorias", size=22, weight="bold"),
                ft.FloatingActionButton(
                    icon=ft.Icons.ADD, 
                    bgcolor="#1B4F9C", 
                    mini=True, 
                    on_click=lambda _: abrir_modal_categoria()
                )
            ], alignment="spaceBetween"),
            
            # BARRA DE PESQUISA E FILTRO
            ft.Row([search_field, btn_filtro], spacing=10),
            
            ft.Divider(height=10, color="transparent"),
            lista_categorias_ui
        ])
    )
    
    carregar_categorias()