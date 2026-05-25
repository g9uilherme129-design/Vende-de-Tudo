import flet as ft
import os
from navigation import build_navigation_bar


def parse_log_line(line: str):
    ts = ''
    user = ''
    action = ''
    details = ''
    try:
        if line.startswith('['):
            end = line.find(']')
            ts = line[1:end] if end != -1 else ''
            rest = line[end + 1:].strip()
        else:
            rest = line
        user_part, action_part = rest.split('action:', 1)
        action, details_part = action_part.split('details:', 1)
        user = user_part.replace('user:', '').strip()
        action = action.strip()
        details = details_part.strip()
    except Exception:
        details = line
    return ts, user, action, details


def tela_log(page: ft.Page, on_back=None, on_home=None, on_vendas=None, on_stock=None, on_users=None, on_perfil=None, on_log=None, is_admin=False):
    page.controls.clear()
    page.padding = 0  # Preenchimento zero para o container de fundo ocupar toda a tela

    # --- PADRONIZAÇÃO DE CORES (IDÊNTICO À TELA DE ESTOQUE) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#050f44" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cor_secundaria = "#1679f2" if is_dark else "#DA7D7D"
    cor_bar = "#1679f2" if is_dark else "#BA7272"

    page.bgcolor = cor_fundo_tela

    # --- LEITURA DO LOG ---
    log_path = os.path.join(os.path.dirname(__file__), 'app.log')
    linhas = []
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                linhas = f.read().splitlines()
        except Exception as e:
            linhas = [f'Erro ao ler log: {e}']
    else:
        linhas = ['Nenhum registro encontrado.']

    # --- COMPONENTES DOS LOGS ---
    log_items = []
    for l in reversed(linhas[-200:]):
        ts, user, action, details = parse_log_line(l)
        
        action_label = ft.Container(
            content=ft.Text(action.upper(), size=10, weight='bold', color=ft.Colors.WHITE),
            padding=ft.padding.symmetric(horizontal=10, vertical=6),
            bgcolor=cor_secundaria,
            border_radius=12,
        )
        user_label = ft.Text(f'Usuário: {user}', size=11, color=cor_texto_s)
        time_label = ft.Text(ts, size=10, color=cor_texto_s)
        details_label = ft.Text(details, size=12, color=cor_texto_p)

        log_items.append(
            ft.Container(
                padding=15,
                border_radius=15,
                bgcolor=cor_fundo_card,
                border=ft.border.all(1, cor_borda),
                content=ft.Column([
                    ft.Row([action_label, time_label], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([user_label], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(height=1, color=ft.Colors.WHITE10),
                    details_label
                ], spacing=6)
            )
        )

    # --- CONTROL DE ROLAGEM DOS LOGS ---
    lista_logs_ui = ft.Column(log_items, spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)

    # --- APPBAR ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color=ft.Colors.WHITE, on_click=lambda _: on_back() if on_back else None),
        title=ft.Text('Logs de Atividade', color=ft.Colors.WHITE, weight="bold"),
        center_title=True,
        bgcolor=cor_barra
    )

    # --- NAVIGATION BAR ---
    build_navigation_bar(
        page=page,
        selected_label="Logs",
        is_admin=is_admin,
        callbacks={
            "on_home": on_home or (lambda: None),
            "on_vendas": on_vendas or (lambda: None),
            "on_stock": on_stock or (lambda: None),
            "on_users": on_users or (lambda: None),
            "on_log": on_log or (lambda: None),
            "on_perfil": on_perfil or (lambda: None),
        },
        bgcolor=cor_barra,
        indicator_color=cor_bar,
    )

    # --- ESTRUTURA PRINCIPAL DA TELA ---
    page.add(
        ft.Container(
            expand=True,
            bgcolor=cor_fundo_tela,
            padding=20,
            content=ft.Column(
                expand=True,
                spacing=15,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text('Histórico de Logs', size=24, weight='bold', color=cor_texto_p),
                            ft.Text(f'Total: {len(linhas)}', size=12, color=cor_texto_s)
                        ]
                    ),
                    lista_logs_ui
                ]
            )
        )
    )
    page.update()