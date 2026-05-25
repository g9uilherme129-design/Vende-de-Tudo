import flet as ft
from navigation import build_navigation_bar
from datetime import datetime
from database import (
    obter_resumo_vendas_vendedor, 
    obter_ultimo_produto_vendedor, 
    buscar_dados_completos_perfil
)

def perfil_page(page: ft.Page, on_home, on_stock, on_vendas, on_users, on_logout, on_game, on_config, on_theme_change, on_log=None):
    page.controls.clear()
    
    # --- VERIFICAÇÃO DE CARGO ---
    perfil_usuario = getattr(page, "tipo_usuario", "VENDEDOR")
    
    # Limpa espaços e joga para maiúsculo para evitar erros de digitação no banco
    perfil_limpo = str(perfil_usuario).upper().strip()
    
    # Se for "ADMIN", e_vendedor será False. Se for qualquer outra coisa, será True.
    e_vendedor = (perfil_limpo != "ADMIN")
    
    # 1. Dados do Usuário
    id_usuario_logado = page.user_data.get("id_user")
    dados_banco = buscar_dados_completos_perfil(id_usuario_logado)
    resumo_vendas = obter_resumo_vendas_vendedor(id_usuario_logado)
    ultimo_p_vendido = obter_ultimo_produto_vendedor(id_usuario_logado)

    if dados_banco:
        nome_usuario = dados_banco.get("nome_user") or "Usuário"
        perfil_usuario = dados_banco.get("perfil") or "Cargo não definido"
        id_usuario = dados_banco.get("id_user") or "---"
        email_usuario = dados_banco.get("email_user") or "não cadastrado"
        cpf_usuario = dados_banco.get("cpf") or "000.000.000-00"
        salario_usuario = float(dados_banco.get("salario") or 0.0)
    else:
        nome_usuario, perfil_usuario, id_usuario = "Usuário", "N/A", id_usuario_logado
        email_usuario, cpf_usuario, salario_usuario = "Erro", "000", 0.0

    total_vendas = resumo_vendas.get("total_vendas", 0)
    valor_total_vendido = resumo_vendas.get("valor_total", 0.0)

    # --- LÓGICA DE CORES (Mantida) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#050f44" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_sair = "#E21717" if is_dark else "#FF0000"
    cor_bar =  "#1679f2" if is_dark else "#BA7272"

    def criar_info_box(label, valor, icone, col=12):
        return ft.Container(
            padding=15, border_radius=12, bgcolor=cor_fundo_card,
            border=ft.border.all(1, cor_borda), col=col,
            content=ft.Row([
                ft.Icon(icone, color=cor_texto_s, size=20),
                ft.Column([
                    ft.Text(label.upper(), size=10, color=cor_texto_s, weight="bold"),
                    ft.Text(valor, size=15, color=cor_texto_p, weight="w500"),
                ], spacing=2, expand=True)
            ])
        )

    header = ft.Column([
        ft.Container(
            content=ft.Icon(ft.Icons.PERSON, size=60, color=cor_texto_s),
            width=100, height=100, border_radius=50, border=ft.border.all(2, cor_texto_s),
        ),
        ft.Text(nome_usuario, size=22, weight="bold", color=cor_texto_p),
        ft.Container(
            content=ft.Text(perfil_usuario, size=12, color="white", weight="bold"),
            bgcolor=cor_texto_s, padding=ft.padding.symmetric(horizontal=15, vertical=5),
            border_radius=15
        ),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)

    # Botão de Troca de Tema (Ações na AppBar)
    page.appbar = ft.AppBar(
        bgcolor=cor_barra, title=ft.Text("Meu Perfil", color="white"), center_title=True,
        actions=[
            ft.IconButton(
                ft.Icons.LIGHT_MODE if is_dark else ft.Icons.DARK_MODE, 
                icon_color="white", on_click=lambda _: on_theme_change()
            )
        ]
    )

    page.add(
        ft.Container(
            expand=True, bgcolor=cor_fundo_tela, padding=20,
            content=ft.Column([
                header,
                ft.Container(height=20),
                ft.Text("Dados Cadastrais", size=14, weight="bold", color=cor_texto_s),
                ft.ResponsiveRow([
                    criar_info_box("ID Usuário", f"#{id_usuario}", ft.Icons.FINGERPRINT, 6),
                    criar_info_box("CPF", cpf_usuario, ft.Icons.BADGE, 6),
                    criar_info_box("E-mail", email_usuario, ft.Icons.EMAIL),
                    criar_info_box("Salário Base", f"R$ {salario_usuario:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), ft.Icons.PAYMENTS),
                ], spacing=10),
                ft.Container(height=15),
                ft.Text("Resumo de Vendas", size=14, weight="bold", color=cor_texto_s),
                ft.ResponsiveRow([
                    criar_info_box("Qtd Vendas", str(total_vendas), ft.Icons.SHOPPING_CART, 6),
                    criar_info_box("Total Vendido", f"R$ {valor_total_vendido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), ft.Icons.MONETIZATION_ON, 6),
                    criar_info_box("Último Produto Vendido", ultimo_p_vendido, ft.Icons.HISTORY),
                ], spacing=10),
                
                ft.Container(height=30),

                # --- BOTÃO: PASSATEMPO ---
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.POLICY_OUTLINED, color="white"), 
                        ft.Text("Termos e Políticas", color="white", weight="bold")
                    ], alignment="center"),
                    bgcolor=cor_texto_s, height=50, border_radius=12,
                    on_click=lambda _: on_game()
                ),
                ft.Container(height=10),

                # Botão Sair
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.LOGOUT, color="white"), ft.Text("SAIR DA CONTA", color="white", weight="bold")], alignment="center"),
                    bgcolor=cor_sair, height=50, border_radius=12, on_click=lambda _: on_logout()
                ),
                ft.Container(height=100) 
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment="center")
        )
    )

    # --- 1. CONFIGURAÇÃO DA LISTA DE NAVEGAÇÃO DINÂMICA ---
    destinos_navegacao = [
        ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicial"),
    ]

    if not e_vendedor:
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"))
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"))
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Usuários"))
    else:
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"))

    destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"))

    # Descobre dinamicamente a posição atual da aba "Perfil"
    index_perfil = 0
    for i, d in enumerate(destinos_navegacao):
        if d.label == "Perfil":
            index_perfil = i
            break

    build_navigation_bar(
        page=page,
        selected_label="Perfil",
        is_admin=not e_vendedor,
        callbacks={
            "on_home": on_home,
            "on_vendas": on_vendas,
            "on_stock": on_stock,
            "on_users": on_users,
            "on_log": on_log or (lambda: None),
            "on_perfil": lambda: None,
        },
        bgcolor=cor_barra,
        indicator_color=cor_bar,
    )

    page.update()