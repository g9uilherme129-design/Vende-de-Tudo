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
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo = "#050A18" if is_dark else "#F0F4FF"
    cor_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_texto = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_subtitulo = ft.Colors.GREY_300 if is_dark else ft.Colors.BLUE_GREY_700
    cor_accent = "#1679f2" if is_dark else "#DA7D7D"

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

    log_items = []
    for l in reversed(linhas[-200:]):
        ts, user, action, details = parse_log_line(l)
        action_label = ft.Container(
            content=ft.Text(action.upper(), size=10, weight='bold', color='white'),
            padding=ft.padding.symmetric(horizontal=10, vertical=6),
            bgcolor=cor_accent,
            border_radius=12,
        )
        user_label = ft.Text(f'Usuário: {user}', size=11, color=cor_subtitulo)
        time_label = ft.Text(ts, size=10, color=cor_subtitulo)
        details_label = ft.Text(details, size=12, color=cor_texto)

        log_items.append(
            ft.Container(
                width=800,
                padding=20,
                bgcolor=cor_card,
                border_radius=20,
                border=ft.border.all(1, ft.Colors.WHITE10),
                content=ft.Column([
                    ft.Row([action_label, time_label], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=8),
                    ft.Row([user_label], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=10),
                    details_label
                ], spacing=6)
            )
        )

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_back() if on_back else None),
        title=ft.Text('Logs de Atividade', color='white'),
        center_title=True,
        bgcolor="#0b1445"
    )

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
        bgcolor="#0b1445",
        indicator_color="#1679f2",
    )

    page.add(
        ft.Container(
            expand=True,
            bgcolor=cor_fundo,
            padding=20,
            content=ft.Column([
                ft.Container(
                    width=850,
                    padding=24,
                    bgcolor=cor_card,
                    border_radius=24,
                    border=ft.border.all(1, ft.Colors.WHITE10),
                    content=ft.Column([
                        ft.Row([
                            ft.Text('Últimos registros', size=20, weight='bold', color=cor_texto),
                            ft.Text(f'Total: {len(linhas)}', size=12, color=cor_subtitulo)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Divider(height=1, color=ft.Colors.WHITE12),
                        ft.Column(log_items, spacing=12, scroll=ft.ScrollMode.AUTO)
                    ], spacing=18)
                )
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    )
    page.update()
