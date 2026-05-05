import flet as ft
import flet_charts as fch
from database import buscar_dados_home

def home_page(page: ft.Page, on_logout, on_stock, on_users, on_perfil, on_venda, on_vendas):
    try:
        dados = buscar_dados_home()
    except Exception:
        dados = {"receita": 0.0, "ranking": [], "vendas_semanais": [], "vendedores": []}

    receita_atual = float(dados.get('receita', 0.0))
    meta_valor = receita_atual * 1.08 

    def formatar_moeda(valor):
        try:
            val = float(valor) if valor is not None else 0.0
            return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except:
            return "R$ 0,00"

    page.controls.clear()
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    page.bgcolor = "#000000" if is_dark else "#F0F4FF" 
    cor_fundo_container = "#0b1445" if is_dark else "#E1E8FA" 
    cor_texto_principal = ft.Colors.WHITE if is_dark else "#0b1445"
    cor_texto_secundario = ft.Colors.WHITE_70 if is_dark else ft.Colors.GREY_700
    cor_borda = "#1E2B4E" if is_dark else "#BCCAE3"

    # --- LÓGICA DE QUANTIDADE DE PRODUTOS ---
    qtd_produtos = [0] * 5
    dias_semana = ["S", "T", "Q", "Q", "S"]
    
    for v in dados.get('vendas_semanais', []):
        idx = v.get('dia_num')
        if idx is not None and 0 <= idx <= 4:
            qtd_produtos[idx] = v.get('qtd') or 0

    # --- ESCALA DO GRÁFICO ---
    max_venda_atual = max(qtd_produtos) if max(qtd_produtos) > 0 else 10
    limite_y = max_venda_atual + (max_venda_atual * 0.2)
    
    if limite_y <= 100:
        passo_y = 20
    elif limite_y <= 500:
        passo_y = 100
    else:
        passo_y = 500

    # --- GRÁFICO ---
    card_vendas_qtd = ft.Container(
        bgcolor=cor_fundo_container, padding=25, border_radius=25, border=ft.border.all(1, cor_borda),
        content=ft.Column([
            ft.Text("QUANTIDADE DE PRODUTOS VENDIDOS", size=11, color=cor_texto_secundario, weight="bold"),
            ft.Container(
                height=180,
                content=fch.BarChart(
                    max_y=limite_y,
                    interactive=True,
                    horizontal_grid_lines=fch.ChartGridLines(
                        color=ft.Colors.with_opacity(0.1, cor_texto_principal), width=1
                    ),
                    left_axis=fch.ChartAxis(
                        labels=[fch.ChartAxisLabel(value=i, label=ft.Text(str(i), size=10, color=cor_texto_secundario)) 
                               for i in range(0, int(limite_y) + 1, int(passo_y))]
                    ),
                    bottom_axis=fch.ChartAxis(
                        labels=[fch.ChartAxisLabel(value=i, label=ft.Text(dias_semana[i], color=cor_texto_principal, weight="bold")) 
                               for i in range(5)]
                    ),
                    groups=[
                        fch.BarChartGroup(
                            x=i, 
                            rods=[fch.BarChartRod(from_y=0, to_y=v, width=38, color="#08D345", border_radius=5)]
                        ) for i, v in enumerate(qtd_produtos)
                    ]
                )
            )
        ])
    )

    # --- FUNÇÃO AUXILIAR DE ITEM (RESOLVE O NameError) ---
    def item_ranking(nome, subtexto, valor_direita):
        return ft.Container(
            padding=15, border_radius=15, bgcolor=cor_fundo_container if is_dark else "#FFFFFF",
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, cor_texto_principal)),
            content=ft.Row([
                ft.Column([
                    ft.Text(nome, weight="bold", color=cor_texto_principal), 
                    ft.Text(subtexto, size=10, color=cor_texto_secundario)
                ], spacing=2, expand=True),
                ft.Text(valor_direita, weight="bold", color="#08D345"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        )

    # --- MONTAGEM DOS RANKINGS ---
    coluna_produtos = ft.Column(spacing=10)
    for v in dados.get('ranking', []):
        # Aqui usamos o nome correto da função
        coluna_produtos.controls.append(
            item_ranking(v['nome_user'], f"{v['qtd_venda']} UNIDADES", formatar_moeda(v['valor_total']))
        )

    coluna_vendedores = ft.Column(spacing=10)
    for vend in dados.get('vendedores', []): 
        coluna_vendedores.controls.append(
            item_ranking(vend['nome'], "VENDEDOR ATIVO", f"{vend['total_vendas']} vendas")
        )

    # --- CONTEÚDO ---
    conteudo = ft.ListView(
        expand=True, padding=20,
        controls=[
            ft.Text("Consolidação", size=28, weight="bold", color=cor_texto_principal),
            ft.Container(height=10),
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.ADD_SHOPPING_CART, color="white"), ft.Text("REGISTRAR NOVA VENDA", color="white", weight="bold")], alignment="center"),
                bgcolor="#1B4F9C", padding=15, border_radius=15, on_click=lambda _: on_venda()
            ),
            ft.Container(height=20),
            
            # Card Receita
            ft.Container(
                padding=25, border_radius=20, bgcolor=cor_fundo_container, border=ft.border.all(1, cor_borda),
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text("RECEITA ATUAL", size=11, color=cor_texto_secundario, weight="bold"),
                            ft.Text(formatar_moeda(receita_atual), size=28, weight="bold", color="#08D345"),
                        ], expand=True),
                        ft.Container(content=ft.Icon(ft.Icons.TRENDING_UP, color="#08D345", size=30), padding=10)
                    ]),
                    ft.Divider(color=ft.Colors.WHITE10, height=20),
                    ft.Row([ft.Icon(ft.Icons.TRACK_CHANGES, color="red", size=16), ft.Text(f"META (+8%): {formatar_moeda(meta_valor)}", size=12, color=cor_texto_secundario)])
                ])
            ),
            ft.Container(height=20),
            card_vendas_qtd,
            ft.Container(height=25),
            
            ft.Text("PRODUTOS MAIS VENDIDOS", size=12, color=cor_texto_secundario, weight="bold"),
            coluna_produtos,
            
            ft.Container(height=25),
            
            ft.Text("RANKING DE VENDEDORES", size=12, color=cor_texto_secundario, weight="bold"),
            coluna_vendedores,
            
            ft.Container(height=100)
        ]
    )

    page.appbar = ft.AppBar(
        bgcolor="#0b1445", title=ft.Text("Vende de Tudo", color="white", weight="bold"), center_title=True,
        actions=[ft.IconButton(icon=ft.Icons.EXIT_TO_APP, icon_color="white", on_click=lambda _: on_logout())]
    )

    page.add(conteudo)



    def trocar_aba(e):

        idx = e.control.selected_index

        if idx == 1: on_vendas()

        elif idx == 2: on_stock()

        elif idx == 3: on_users()

        elif idx == 4: on_perfil()



    page.navigation_bar = ft.Container(

        content=ft.NavigationBar(

            bgcolor="#0b1445", selected_index=0, on_change=trocar_aba,

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

    page.update() 