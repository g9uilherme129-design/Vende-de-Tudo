import flet as ft
from database import buscar_usuarios_db, buscar_nome_admin_por_id
from navigation import build_navigation_bar

def usuarios(page: ft.Page, on_home, on_stock, on_vendas, on_perfil, on_logout, on_adicionar_usuario, on_editar_usuario, on_desativar_usuario, on_reativar_user, user_data, on_log=None, mensagem=None):

    page.controls.clear()
    page.padding = 0

    # --- PADRONIZAÇÃO DE CORES ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#050f44" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_input = "#0A122A" if is_dark else "#F5F7FB"
    cor_secundaria =  "#1679f2" if is_dark else "#DA7D7D"
    cor_desat =  "#652121" if is_dark else "#FF865B"
    cor_bar =  "#1679f2" if is_dark else "#BA7272"
    cor_seg = "#ffffff" if is_dark else "#FFFFFF"
    cort_3 = "#36D900" if is_dark else "#FF6C03"

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
        
        # --- LÓGICA DE COR DO CONTAINER (ALTERADO AQUI) ---
        if eu_sou_este_usuario and is_dark:
            cor_bg_final = "#1A3A7A"
        elif not esta_ativo:
            cor_bg_final = cor_desat
        else:
            cor_bg_final = cor_fundo_card

        borda_card = ft.border.all(2, cor_texto_s) if eu_sou_este_usuario else ft.border.all(1, cor_borda)

        perfil_str = str(u.get("perfil", "")).lower()
        is_admin = "admin" in perfil_str
        icone_perfil = ft.Icons.SECURITY if is_admin else ft.Icons.PERSON
        cor_perfil = cor_texto_s if is_admin else ft.Colors.ORANGE_700

        info_desativacao = ft.Container(
            visible=not esta_ativo,
            padding=ft.padding.all(10),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            border_radius=10,
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, color=cor_texto_p, size=16),
                    ft.Text("DADOS DA DESATIVAÇÃO", size=11, weight="bold", color=cor_texto_p),
                ], spacing=5),
                ft.Text(f"Motivo: {u.get('motivo_desat', 'Não informado')}", size=12, color=cor_texto_p),
                ft.Text(f"Por: Admin {buscar_nome_admin_por_id(u.get('admin_desat'))}", size=11, italic=True, color=cor_texto_p),
            ], spacing=3)
        )

        return ft.Container(
            bgcolor=cor_bg_final, 
            border_radius=15, 
            padding=15,
            border=borda_card,
            opacity=1.0 if esta_ativo else 0.9, # Aumentei um pouco a opacidade para a cor aparecer melhor
            content=ft.Column(spacing=10, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Row([
                        ft.Text(f"ID: {id_do_card}", size=12, color=cor_secundaria if esta_ativo else "white", weight="bold"),
                        ft.Container(
                            content=ft.Text("VOCÊ", size=10, weight="bold", color="white"),
                            bgcolor=cor_texto_s,
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                            border_radius=5,
                            visible=eu_sou_este_usuario
                        )
                    ], spacing=10),
                    ft.Text(f"CPF: {u.get('cpf', '000.000.000-00')}", size=12, color=cor_secundaria if esta_ativo else "white"),
                ]),
                
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
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
                                    size=18, weight="bold", color=cor_texto_p, 
                                    style=ft.TextStyle(decoration=None if esta_ativo else ft.TextDecoration.LINE_THROUGH)
                                ),
                                ft.Row([
                                    ft.Text(perfil_str.upper(), size=11, color=cor_secundaria if esta_ativo else "white"),
                                    ft.Text(" • ", color=cor_secundaria if esta_ativo else "white"),
                                    ft.Text(f"{u.get('total_vendas', 0)} VENDAS", size=11, color=cort_3 if esta_ativo else "white", weight="bold"),
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
                    ft.Text(f"✉ {u.get('email_user', '---')}", size=12, color=cor_secundaria if esta_ativo else "white"),
                    ft.Text(f"Salário: {formatar_moeda(u.get('salario', 0))}", size=13, weight="bold", color=cor_seg),
                ]),

                ft.Divider(height=1, color=ft.Colors.WHITE10),
                
                ft.Row(alignment=ft.MainAxisAlignment.END, spacing=10, controls=[
                    ft.TextButton(
                        "Editar", 
                        icon=ft.Icons.EDIT_NOTE, 
                        icon_color=cor_texto_s if esta_ativo else "white",
                        on_click=lambda _: on_editar_usuario(id_do_card),
                        visible=esta_ativo
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.POWER_SETTINGS_NEW if esta_ativo else ft.Icons.PLAY_ARROW_ROUNDED, size=20),
                            ft.Text("Desativar" if esta_ativo else "REATIVAR", weight="bold"),
                        ], tight=True),
                        bgcolor="#c02429" if esta_ativo else "#15B065",
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        disabled=eu_sou_este_usuario, 
                        on_click=lambda _: on_desativar_usuario(u) if esta_ativo else on_reativar_user(u)
                    ),
                ])
            ])
        )

    def filtrar_usuarios(e=None):
        t = search_field.value.lower() if search_field.value else ""
        lista_usuarios_ui.controls.clear()
        for u in usuarios_db:
            if t in str(u.get("nome_user", "")).lower() or t in str(u.get("email_user", "")).lower():
                lista_usuarios_ui.controls.append(user_card(u))
        page.update()

    search_field = ft.TextField(
        hint_text="Buscar por nome ou e-mail...", prefix_icon=ft.Icons.SEARCH, expand=True,
        on_change=filtrar_usuarios, bgcolor=cor_input, border_radius=15,
        border_color=cor_borda, text_style=ft.TextStyle(color=cor_texto_p)
    )

    btn_filtro = ft.PopupMenuButton(icon=ft.Icons.FILTER_LIST, icon_color=cor_texto_p, items=[
        ft.PopupMenuItem(content=ft.Text("Todos"), on_click=lambda _: filtrar_usuarios()),
    ])

    page.appbar = ft.AppBar(
        bgcolor=cor_barra, title=ft.Text("Equipe de Vendas", color="white", weight="bold"),
        center_title=True, actions=[ft.IconButton(ft.Icons.EXIT_TO_APP, icon_color="white", on_click=lambda _: on_logout())]
    )

    def trocar_aba(e):
        idx = e.control.selected_index
        if idx == 0: on_home()
        elif idx == 1: on_vendas()
        elif idx == 2: on_stock()
        elif idx == 4: on_perfil()
        elif idx == 5:
            if on_log:
                on_log()

    build_navigation_bar(
        page=page,
        selected_label="Usuários",
        is_admin=True,
        callbacks={
            "on_home": on_home,
            "on_vendas": on_vendas,
            "on_stock": on_stock,
            "on_users": lambda: None,
            "on_log": on_log or (lambda: None),
            "on_perfil": on_perfil,
        },
        bgcolor=cor_barra,
        indicator_color=cor_bar,
    )

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
                    ft.Text("Gerenciar Usuários", size=24, weight="bold", color=cor_texto_p),
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        bgcolor=cor_texto_s,
                        tooltip="Novo Usuário",
                        mini=True, 
                        on_click=lambda _: on_adicionar_usuario()
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([search_field, btn_filtro]),
                lista_usuarios_ui
            ])
        )
    )
    
    filtrar_usuarios()

    if mensagem:
        page.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor="green")
        page.snack_bar.open = True
        page.update()