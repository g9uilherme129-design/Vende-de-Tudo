import flet as ft

def game_page(page: ft.Page, on_back):
    page.controls.clear()
    
    # --- PADRONIZAÇÃO DE CORES (IDÊNTICA AO SEU SISTEMA) ---
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_fundo_card = "#0b1445" if is_dark else "#FFFFFF"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"
    cor_texto_p = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_texto_s = "#1679f2" if is_dark else "#DA7D7D"
    cor_barra = "#0b1445" if is_dark else "#DA7D7D" 
    cor_fundo_tela = "#050A18" if is_dark else "#F0F4FF"

    # --- FUNÇÃO AUXILIAR PARA SEÇÕES DE TEXTO ---
    def secao_texto(titulo, conteudo_texto):
        return ft.Container(
            padding=20,
            border_radius=20,
            bgcolor=cor_fundo_card,
            border=ft.border.all(1, cor_borda),
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, color=cor_texto_s, size=20),
                    ft.Text(titulo, size=16, weight="bold", color=cor_texto_p),
                ], spacing=10),
                ft.Divider(color=ft.Colors.WHITE10 if is_dark else ft.Colors.BLACK12),
                ft.Text(conteudo_texto, size=14, color=cor_texto_p, text_align=ft.TextAlign.JUSTIFY),
            ], spacing=10)
        )

    # --- CONTEÚDO LEGAL ---
    conteudo = ft.Container(
        expand=True,
        bgcolor=cor_fundo_tela,
        padding=20,
        content=ft.Column([
            ft.Text("Termos e Regras", size=28, weight="bold", color=cor_texto_p),
            ft.Text("Leia atentamente as políticas da empresa", size=14, color=cor_texto_s),
            ft.Container(height=10),

            # Seção: Termos de Uso
            secao_texto(
                "Termos de Uso", 
                "Ao utilizar o sistema Vende de Tudo, você concorda em manter a integridade dos dados "
                "e utilizar as ferramentas apenas para fins profissionais. O acesso é pessoal e intransferível."
            ),

            ft.Container(height=10),

            # Seção: Política de Privacidade
            secao_texto(
                "Política de Privacidade", 
                "Seus dados de acesso e registros de vendas são protegidos por criptografia. "
                "Não compartilhamos informações de faturamento com terceiros fora da organização."
            ),

            ft.Container(height=10),

            # Seção: Regras da Empresa
            secao_texto(
                "Regras da Empresa", 
                "1. Todos os registros de venda devem ser feitos em tempo real.\n"
                "2. É proibido o compartilhamento de senhas entre vendedores.\n"
                "3. O estoque deve ser conferido semanalmente.\n"
                "4. Manter o respeito e a ética no ambiente de trabalho digital."
            ),

            # Botão de Aceite (Estilo dos botões do seu sistema)
            ft.Container(height=20),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color="black"), 
                    ft.Text("ESTOU CIENTE E DE ACORDO", color="black", weight="bold")
                ], alignment="center"),
                bgcolor="#16a34a", 
                height=55, 
                border_radius=15, 
                on_click=lambda _: on_back()
            ),
            
            ft.Container(height=100) # Espaço para o scroll
        ], scroll=ft.ScrollMode.AUTO)
    )

    # --- APPBAR ---
    page.appbar = ft.AppBar(
        bgcolor=cor_barra,
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_back()),
        title=ft.Text("Políticas Internas", color="white", weight="bold"),
        center_title=True,
    )

    page.add(conteudo)
    page.update()