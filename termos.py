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

    # --- ESTADO DO BOTÃO ---
    botao_clicado = {"state": False}

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
                "Ao utilizar o sistema Vende de Tudo, você concorda em manter a integridade dos dados e utilizar as ferramentas apenas para fins profissionais e comerciais legítimos. O acesso ao sistema é pessoal, intransferível e sob responsabilidade exclusiva do usuário. Qualquer tentativa de compartilhar credenciais ou conceder acesso a terceiros não autorizados resultará em sanções disciplinares. O usuário se compromete a seguir todas as políticas da empresa, manter a confidencialidade das informações sensíveis e informar imediatamente qualquer atividade suspeita ou comprometimento de segurança ao administrador do sistema."
            ),

            ft.Container(height=10),

            # Seção: Política de Privacidade
            secao_texto(
                "Política de Privacidade", 
                "Seus dados de acesso, registros de vendas, informações pessoais e histórico de transações são protegidos por criptografia de ponta a ponta e armazenados em servidores seguros. Não compartilhamos informações de faturamento, comissões ou dados sensíveis com terceiros fora da organização. Apenas administradores autorizados têm acesso aos dados completos. Os dados são retidos conforme legislação aplicável (LGPD) e podem ser excluídos mediante solicitação formal. Qualquer acessodesautorizado será imediatamente investigado e reportado."
            ),

            ft.Container(height=10),

            # Seção: Regras da Empresa
            secao_texto(
                "Regras da Empresa", 
                "1. Todos os registros de venda devem ser feitos em tempo real e com dados precisos.\n"
                "2. É proibido o compartilhamento de senhas, tokens ou credenciais entre vendedores e funcionários.\n"
                "3. O estoque deve ser conferido semanalmente e discrepâncias devem ser reportadas imediatamente.\n"
                "4. Manter o respeito, ética e profissionalismo no ambiente de trabalho digital.\n"
                "5. Não é permitido fazer alterações nos registros históricos de vendas sem autorização do administrador.\n"
                "6. Reembolsos e cancelamentos devem ser solicitados e aprovados por um administrador.\n"
                "7. O usuário é responsável por manter sua senha segura e mudar regularmente.\n"
                "8. Violações das políticas podem resultar em desativação da conta e ações legais."
            ),

            ft.Container(height=20),

            # Botão de Aceite com feedback dinâmico
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color="black" if not botao_clicado["state"] else "white"), 
                    ft.Text("ESTOU CIENTE E DE ACORDO", color="black" if not botao_clicado["state"] else "white", weight="bold")
                ], alignment="center"),
                bgcolor="#e8e8e8" if not botao_clicado["state"] else "#16a34a", 
                height=55, 
                border_radius=15,
                on_click=lambda _: _atualizar_botao()
            ),
            
            ft.Container(height=100) # Espaço para o scroll
        ], scroll=ft.ScrollMode.AUTO)
    )

    def _atualizar_botao():
        botao_clicado["state"] = True
        page.snack_bar = ft.SnackBar(ft.Text("✅ Você marcou que está ciente das políticas!"), bgcolor="#00b40d")
        page.snack_bar.open = True
        import time
        time.sleep(1.5)
        on_back()

    # --- APPBAR ---
    page.appbar = ft.AppBar(
        bgcolor=cor_barra,
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_back()),
        title=ft.Text("Políticas Internas", color="white", weight="bold"),
        center_title=True,
    )

    page.add(conteudo)
    page.update()