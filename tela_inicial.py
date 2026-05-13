import flet as ft
import flet_charts as fch
from database import buscar_dados_home
from database import buscar_dados_home_vendedor

def home_page(page: ft.Page, on_logout, on_stock, on_users, on_perfil, on_venda, on_vendas):
    
    # --- VERIFICAÇÃO DE CARGO ---
    tipo_usuario = getattr(page, "tipo_usuario", "VENDEDOR")
    perfil_limpo = str(tipo_usuario).upper().strip()
    e_admin = (perfil_limpo == "ADMIN")
    
    # --- RECUPERAÇÃO DO ID DO USUÁRIO ---
    # Tenta recuperar de atributos diretos ou usando a propriedade correta da session do Flet
    id_usuario_logado = getattr(page, "id_user", None) or getattr(page, "id_usuario", None)

    # --- BUSCA DE DADOS DINÂMICA ---
    try:
        if e_admin:
            dados = buscar_dados_home()
        else:
            dados = buscar_dados_home_vendedor(id_usuario_logado)
    except Exception:
        dados = {
            "receita": 0.0, 
            "receita_vendedor": 0.0, 
            "ranking": [], 
            "vendas_semanais": [], 
            "vendedores": [],
            "produtos_scrum": []
        }

    receita_exibir = 0.0
    meta_valor = 0.0 

    if e_admin:
        titulo_receita = "RECEITA TOTAL DA EMPRESA"
        receita_exibir = float(dados.get('receita', 0.0))
        meta_valor = receita_exibir * 1.08 
    else:
        titulo_receita = "MINHAS VENDAS REALIZADAS"
        receita_exibir = float(dados.get('receita_vendedor', 0.0))
    
    def formatar_moeda(valor):
        try:
            val = float(valor) if valor is not None else 0.0
            return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except:
            return "R$ 0,00"

    page.controls.clear()
    
    # --- LÓGICA DE CORES IDENTICA À PERFIL_PAGE ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#050f44" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"
    cort_3 = "#36D900" if is_dark else "#FF6C03"
    cor_bar = "#1679f2" if is_dark else "#BA7272"

    # --- FUNÇÃO AUXILIAR DE ITEM ---
    def item_ranking(nome, subtexto, valor_direita):
        return ft.Container(
            padding=15, border_radius=15, bgcolor=cor_fundo_card,
            border=ft.border.all(1, cor_borda),
            content=ft.Row([
                ft.Column([
                    ft.Text(nome, weight="bold", color=cor_texto_p), 
                    ft.Text(subtexto, size=10, color=cor_texto_s)
                ], spacing=2, expand=True),
                ft.Text(valor_direita, weight="bold", color=cort_3),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        )

    # --- MONTAGEM DOS RANKINGS ---
    coluna_produtos = ft.Column(spacing=10)
    for v in dados.get('ranking', []):
        coluna_produtos.controls.append(item_ranking(v['nome_user'], f"{v['qtd_venda']} UNIDADES", formatar_moeda(v['valor_total'])))

    coluna_vendedores = ft.Column(spacing=10)
    for vend in dados.get('vendedores', []): 
        coluna_vendedores.controls.append(item_ranking(vend['nome'], "VENDEDOR ATIVO", f"{vend['total_vendas']} vendas"))


    # --- COMPONENTE DE ESTOQUE COMPACTO (VENDEDOR) ---
    grid_produtos = ft.GridView(expand=True, runs_count=3, max_extent=120, spacing=8, run_spacing=8)
    lista_produtos_original = dados.get('produtos_scrum', [])

    def popular_grid(texto_busca=""):
        grid_produtos.controls.clear()
        termo = texto_busca.lower().strip()
        
        for p in lista_produtos_original:
            nome_prod = p.get('nome', '')
            qtd_atual = p.get('quantidade', 0)
            
            # Filtro da barra de pesquisa e validação de quantidade positiva
            if termo in nome_prod.lower() and qtd_atual > 0:
                grid_produtos.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.SHOPPING_BAG_OUTLINED, color=cor_texto_s, size=20),
                            ft.Text(nome_prod, size=10, weight="bold", text_align="center", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Text(formatar_moeda(p.get('preco', 0)), size=10, color=cort_3, weight="bold"),
                            ft.Container(
                                content=ft.Text(f"{qtd_atual} UN", size=8, weight="bold", color="white"),
                                bgcolor="#51e833" if qtd_atual > 10 else "#ff4444",
                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                border_radius=5
                            )
                        ], alignment="center", horizontal_alignment="center", spacing=2),
                        bgcolor=cor_fundo_card, 
                        padding=6, 
                        border_radius=12, 
                        border=ft.border.all(1, cor_borda),
                    )
                )
        page.update()

    def filtrar_estoque(e):
        popular_grid(e.control.value)

    # Inicializa a renderização dos cards do GridView
    popular_grid()


    # --- ÁREA DINÂMICA: GRÁFICO (ADMIN) OU GRID COM PESQUISA (VENDEDOR) ---
    if e_admin:
        qtd_produtos = [0] * 5
        dias_semana = ["S", "T", "Q", "Q", "S"]
        for v in dados.get('vendas_semanais', []):
            idx = v.get('dia_num')
            if idx is not None and 0 <= idx <= 4:
                qtd_produtos[idx] = v.get('qtd') or 0

        max_venda_atual = max(qtd_produtos) if max(qtd_produtos) > 0 else 10
        limite_y = max_venda_atual + (max_venda_atual * 0.2)
        passo_y = 20 if limite_y <= 100 else 100 if limite_y <= 500 else 500

        area_visual_desempenho = ft.Column([
            ft.Text("PRODUTOS VENDIDOS NA SEMANA", size=11, color=cor_texto_s, weight="bold"),
            ft.Container(
                height=180,
                content=fch.BarChart(
                    max_y=limite_y,
                    interactive=True,
                    horizontal_grid_lines=fch.ChartGridLines(color=ft.Colors.with_opacity(0.1, cor_texto_p), width=1),
                    left_axis=fch.ChartAxis(
                        labels=[fch.ChartAxisLabel(value=i, label=ft.Text(str(i), size=10, color=cor_texto_s)) 
                               for i in range(0, int(limite_y) + 1, int(passo_y))]
                    ),
                    bottom_axis=fch.ChartAxis(
                        labels=[fch.ChartAxisLabel(value=i, label=ft.Text(dias_semana[i], color=cor_texto_p, weight="bold")) 
                               for i in range(5)]
                    ),
                    groups=[fch.BarChartGroup(x=i, rods=[fch.BarChartRod(from_y=0, to_y=v, width=38, color=cort_3, border_radius=5)]) 
                            for i, v in enumerate(qtd_produtos)]
                )
            )
        ])
    else:
        # Container compacto contendo a Barra de Pesquisa e o GridView com rolagem
        area_visual_desempenho = ft.Column([
            ft.Text("CONSULTA RÁPIDA DE ESTOQUE", size=11, color=cor_texto_s, weight="bold"),
            ft.TextField(
                hint_text="Pesquisar produto...",
                text_size=12,       
                height=40,
                border_radius=10,
                border_color=cor_borda,
                color=cor_texto_p,
                prefix_icon=ft.Icons.SEARCH,
                on_change=filtrar_estoque,
                content_padding=10
            ),
            ft.Container(
                height=200, # Define a altura fixa do scroll da listagem rápida
                content=grid_produtos
            )
        ], spacing=10)

    # --- CONTEÚDO PRINCIPAL ---
    conteudo = ft.Container(
        expand=True, bgcolor=cor_fundo_tela, padding=20,
        content=ft.Column([
            ft.Text("Consolidação", size=28, weight="bold", color=cor_texto_p),
            ft.Container(height=10),
            
            # Botão Registrar Venda
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ADD_SHOPPING_CART, color="white"), 
                    ft.Text("REGISTRAR NOVA VENDA", color="white", weight="bold")
                ], alignment="center"),
                bgcolor=cor_texto_s, 
                height=55, 
                border_radius=15, 
                on_click=lambda _: on_venda()
            ),
            
            ft.Container(height=20),
            
            # Card Receita Dinâmico (Admin vs Vendedor)
            ft.Container(
                padding=25, border_radius=20, bgcolor=cor_fundo_card, border=ft.border.all(1, cor_borda),
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(titulo_receita, size=11, color=cor_texto_s, weight="bold"),
                            ft.Text(formatar_moeda(receita_exibir), size=28, weight="bold", color=cort_3),
                        ], expand=True),
                        ft.Icon(ft.Icons.TRENDING_UP, color=cort_3, size=30)
                    ]),
                    ft.Column([
                        ft.Divider(color=ft.Colors.WHITE10 if is_dark else ft.Colors.BLACK12, height=20),
                        ft.Row([ft.Icon(ft.Icons.TRACK_CHANGES, color="#B71C1C", size=16), ft.Text(f"META (+8%): {formatar_moeda(meta_valor)}", size=12, color=cor_texto_s)])
                    ], visible=e_admin)
                ])
            ),
            
            ft.Container(height=20),
            
            # Injeta o Gráfico (Admin) ou o Mini-Grid com scroll interno (Vendedor)
            ft.Container(
                bgcolor=cor_fundo_card, padding=20, border_radius=25, border=ft.border.all(1, cor_borda),
                content=area_visual_desempenho
            ),
            
            ft.Container(height=25),
            ft.Text("PRODUTOS MAIS VENDIDOS", size=12, color=cor_texto_s, weight="bold"),
            coluna_produtos,
            
            # --- BLINDAGEM VISUAL ---
            ft.Column([
                ft.Container(height=25),
                ft.Text("RANKING DE VENDEDORES", size=12, color=cor_texto_s, weight="bold"),
                coluna_vendedores,
            ], visible=e_admin),
            
            ft.Container(height=100)
        ], scroll=ft.ScrollMode.AUTO)
    )

    # --- APPBAR E NAVBAR ---
    page.appbar = ft.AppBar(
        bgcolor=cor_barra, title=ft.Text("Vende de Tudo", color="white", weight="bold"), center_title=True,
        actions=[ft.IconButton(icon=ft.Icons.EXIT_TO_APP, icon_color="white", on_click=lambda _: on_logout())]
    )

    destinos_navegacao = [
        ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicial"),
    ]

    if e_admin:
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_OUTLINED, label="Vendas"))
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"))
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.GROUP_OUTLINED, label="Usuários"))
    else:
        destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, label="Estoque"))

    destinos_navegacao.append(ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Perfil"))

    def trocar_aba(e):
        aba_selecionada = destinos_navegacao[e.control.selected_index].label
        if aba_selecionada == "Inicial":
            pass
        elif aba_selecionada == "Vendas":
            on_vendas()
        elif aba_selecionada == "Estoque":
            on_stock()
        elif aba_selecionada == "Usuários":
            on_users()
        elif aba_selecionada == "Perfil":
            on_perfil()

    page.navigation_bar = ft.Container(
        content=ft.NavigationBar(
            bgcolor=cor_barra, 
            selected_index=0, 
            on_change=trocar_aba,
            indicator_color=cor_bar,
            destinations=destinos_navegacao
        ),
        margin=ft.margin.only(left=25, right=25, bottom=20),
        border_radius=40, 
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS
    )

    page.add(conteudo)