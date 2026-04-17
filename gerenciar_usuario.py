import flet as ft
from database import buscar_usuarios_db

def usuarios(page: ft.Page, on_home, on_stock, on_vendas, on_perfil, on_logout, on_adicionar_usuario, on_editar_usuario, on_desativar_usuario, on_reativar_user, user_data):

    page.controls.clear()
    page.padding = 20

    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_container_bg = "#0b1445" if is_dark else "#F0F2F8"
    cor_texto_principal = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_secundario = ft.Colors.GREY_500
    cor_fundo_busca = "#0d1626" if is_dark else "#FFFFFF"

    usuarios_db = buscar_usuarios_db()
    lista_usuarios_ui = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=10)

    def formatar_moeda(valor):
        try:
            return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except:
            return "R$ 0,00"

    def user_card(u):
        dados_sessao = user_data if user_data else {}
        
        id_do_card = u.get("id_user") or u.get("id_use")
        id_logado = dados_sessao.get("id_use") or dados_sessao.get("id_user")
        
        eu_sou_este_usuario = str(id_do_card) == str(id_logado) if id_logado else False
        esta_ativo = u.get("status_user") == 1
        
        status_texto = "ATIVO" if esta_ativo else "INATIVO"
        cor_status = "#00b40d" if esta_ativo else "#ff0008"
        opacidade_card = 1.0 if esta_ativo else 0.7
        
        cor_bg_final = "#1A3A7A" if eu_sou_este_usuario else cor_container_bg
        borda_card = ft.border.all(2, ft.Colors.BLUE_400) if eu_sou_este_usuario else None

        perfil_str = str(u.get("perfil", "")).lower()
        is_admin = "admin" in perfil_str
        icone_perfil = ft.Icons.SECURITY if is_admin else ft.Icons.PERSON
        cor_perfil = ft.Colors.BLUE_800 if is_admin else ft.Colors.ORANGE_700

        info_desativacao = ft.Container(
            visible=not esta_ativo,
            padding=10,
            margin=ft.margin.only(top=5),
            bgcolor=ft.Colors.with_opacity(0.1, "#ff0008"),
            border_radius=10,
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, size=14, color="#ff4444"),
                    ft.Text("DETALHES DA DESATIVAÇÃO", size=11, weight="bold", color="#ff4444"),
                ]),
                ft.Text(f"Motivo: {u.get('motivo_desat') or 'Não informado'}", size=12, italic=True, color=cor_texto_principal),
                ft.Row([
                    ft.Text(f"Data: {u.get('data_desat') or '---'}", size=11, color=cor_texto_secundario),
                    ft.Text(" • ", color=cor_texto_secundario),
                    ft.Text(f"Por: {u.get('admin_desat') or 'Admin'}", size=11, weight="w600", color=cor_texto_secundario),
                ])
            ], spacing=3)
        )

        return ft.Container(
            bgcolor=cor_bg_final, 
            border_radius=15, 
            padding=15,
            border=borda_card,
            opacity=opacidade_card,
            content=ft.Column(spacing=10, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Row([
                        ft.Text(f"ID: {id_do_card}", size=12, color=cor_texto_secundario, weight="bold"),
                        ft.Container(
                            content=ft.Text("VOCÊ", size=10, weight="bold", color="white"),
                            bgcolor=ft.Colors.BLUE_600,
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                            border_radius=5,
                            visible=eu_sou_este_usuario
                        )
                    ], spacing=10),
                    ft.Text(f"CPF: {u.get('cpf', '000.000.000-00')}", size=12, color=cor_texto_secundario),
                ]),
                
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                    vertical_alignment=ft.CrossAxisAlignment.CENTER, 
                    controls=[
                        ft.Row([
                            ft.CircleAvatar(
                                content=ft.Icon(icone_perfil, color="white", size=25),
                                bgcolor=cor_perfil if esta_ativo else ft.Colors.GREY_700,
                                radius=25,
                            ),
                            ft.Column([
                                ft.Text(
                                    u.get("nome_user", "Usuário"), 
                                    size=18, weight="bold", 
                                    color=cor_texto_principal, 
                                    style=ft.TextStyle(decoration=None if esta_ativo else ft.TextDecoration.LINE_THROUGH)
                                ),
                                ft.Row([
                                    ft.Text(perfil_str.upper(), size=11, color=ft.Colors.BLUE_GREY_400),
                                    ft.Text(" • ", color=cor_texto_secundario),
                                    ft.Text(f"{u.get('total_vendas', 0)} VENDAS", size=11, color="#08D345", weight="bold"),
                                ])
                            ], spacing=2),
                        ], spacing=15),
                        
                        ft.Container(
                            content=ft.Text(status_texto, size=10, weight="bold", color="white"),
                            bgcolor=cor_status, 
                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                            border_radius=20
                        )
                    ]
                ),
                
                info_desativacao,

                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text(f"✉ {u.get('email_user', '---')}", size=12, color=cor_texto_secundario),
                    ft.Text(f"Salário: {formatar_moeda(u.get('salario', 0))}", size=13, weight="bold", color=cor_texto_principal),
                ]),

                ft.Divider(height=1, color=ft.Colors.WHITE10),
                
                ft.Row(alignment=ft.MainAxisAlignment.END, spacing=10, controls=[
                    ft.TextButton(
                        "Editar", 
                        icon=ft.Icons.EDIT_NOTE, 
                        on_click=lambda _: on_editar_usuario(id_do_card),
                        visible=esta_ativo
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.POWER_SETTINGS_NEW if esta_ativo else ft.Icons.PLAY_ARROW_ROUNDED, size=20),
                            ft.Text("Desativar" if esta_ativo else "REATIVAR USUÁRIO", weight="bold"),
                        ], tight=True),
                        bgcolor="#991f23" if esta_ativo else "#00E676",
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=8,
                        ),
                        disabled=eu_sou_este_usuario, 
                        # Aqui decide qual função chamar baseado no status
                        on_click=lambda _: on_desativar_usuario(u) if esta_ativo else on_reativar_user(u)
                    ),
                ])
            ])
        )

    def filtrar_usuarios(e=None):
        t = search_field.value.lower() if search_field.value else ""
        c = btn_filtro.data
        
        filtrados = [u for u in usuarios_db if t in str(u.get("nome_user", "")).lower() or t in str(u.get("email_user", "")).lower()]

        if c == "id":
            filtrados.sort(key=lambda x: str(x.get("id_user") or x.get("id_use")))
        elif c == "vendas":
            filtrados.sort(key=lambda x: x.get("total_vendas", 0), reverse=True)
        elif c == "alfabetica":
            filtrados.sort(key=lambda x: str(x.get("nome_user", "")))
        elif c == "inativos":
            filtrados = [u for u in filtrados if u.get("status_user") == 0]
        elif c == "ativos":
            filtrados = [u for u in filtrados if u.get("status_user") == 1]

        lista_usuarios_ui.controls.clear()
        for u in filtrados:
            lista_usuarios_ui.controls.append(user_card(u))
        
        if not filtrados:
            lista_usuarios_ui.controls.append(
                ft.Container(
                    content=ft.Text("Nenhum usuário encontrado.", color=cor_texto_secundario),
                    alignment=ft.alignment.center, padding=20
                )
            )
        page.update()

    def mudar_f(c): 
        btn_filtro.data = c
        filtrar_usuarios()

    search_field = ft.TextField(
        hint_text="Buscar por nome ou e-mail...", prefix_icon=ft.Icons.SEARCH, expand=True,
        on_change=filtrar_usuarios, bgcolor=cor_fundo_busca, border_radius=15
    )

    btn_filtro = ft.PopupMenuButton(icon=ft.Icons.FILTER_LIST, items=[
        ft.PopupMenuItem(content=ft.Text("Todos"), on_click=lambda _: mudar_f("alfabetica")),
        ft.PopupMenuItem(content=ft.Text("Apenas Ativos"), on_click=lambda _: mudar_f("ativos")),
        ft.PopupMenuItem(content=ft.Text("Apenas Inativos"), on_click=lambda _: mudar_f("inativos")),
        ft.PopupMenuItem(content=ft.Text("Mais Vendas"), on_click=lambda _: mudar_f("vendas")),
        ft.PopupMenuItem(content=ft.Text("Por ID"), on_click=lambda _: mudar_f("id")),
    ])
    btn_filtro.data = "alfabetica"

    page.appbar = ft.AppBar(
        bgcolor="#0b1445", title=ft.Text("Equipe de Vendas", color="white", weight="bold"),
        center_title=True, actions=[ft.IconButton(ft.Icons.EXIT_TO_APP, icon_color="white", on_click=lambda _: on_logout())]
    )

    page.add(
        ft.Column(expand=True, controls=[
            ft.Row([
                ft.Text("Gerenciar Usuários", size=24, weight="bold", color=cor_texto_principal),
                ft.FloatingActionButton(icon=ft.Icons.ADD, bgcolor="#1B4F9C", mini=True, on_click=lambda _: on_adicionar_usuario())
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([search_field, btn_filtro]),
            lista_usuarios_ui
        ])
    )

    def trocar_aba(e):
        idx = e.control.selected_index
        if idx == 0: on_home()
        elif idx == 1: on_vendas()
        elif idx == 2: on_stock()
        elif idx == 3: pass
        elif idx == 4: on_perfil()

    nav = ft.NavigationBar(
        bgcolor="#0b1445", selected_index=3, on_change=trocar_aba,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
            ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"),
        ]
    )
    page.navigation_bar = ft.Container(content=nav, margin=ft.margin.only(left=25, right=25, bottom=30), border_radius=40, clip_behavior=ft.ClipBehavior.ANTI_ALIAS)
    
    filtrar_usuarios()