import flet as ft
from database import validar_recuperacao_db, resetar_senha_db

def tela_recuperacao(page: ft.Page, on_login):
    page.controls.clear()
    
    # Forçamos o tema dark para garantir o visual "Pae"
    page.theme_mode = ft.ThemeMode.DARK
    
    # --- PALETA DE CORES DARK PROFISSIONAL ---
    cor_fundo_tela = "#000000"        # Preto Absoluto
    cor_card_principal = "#0b1445"    # Azul Marinho Profundo
    cor_texto_high = "#FFFFFF"        # Branco Puro
    cor_texto_low = "#94A3B8"         # Cinza Azulado (subtexto)
    cor_borda = "#1E2B4E"             # Azul de destaque para bordas
    cor_input_bg = "#070D1F"          # Fundo do Input (mais escuro que o card)
    cor_destaque_verde = "#08D345"    # Verde Neon (Home Style)
    cor_botao_azul = "#1B4F9C"        # Azul Royal

    page.bgcolor = cor_fundo_tela

    # --- ESTADO ---
    id_usuario_validado = [None] 

    # --- HELPER PARA INPUTS ESTILIZADOS ---
    def estilo_field(label, password=False, visible=True):
        return ft.TextField(
            label=label,
            password=password,
            can_reveal_password=password,
            visible=visible,
            border_radius=15,
            bgcolor=cor_input_bg,
            border_color=cor_borda,
            focused_border_color=cor_destaque_verde, # Brilha verde ao clicar
            label_style=ft.TextStyle(color=cor_texto_low),
            color=cor_texto_high,
            cursor_color=cor_destaque_verde,
            selection_color=ft.Colors.with_opacity(0.3, cor_destaque_verde)
        )

    nome_in = estilo_field("Nome Completo")
    email_in = estilo_field("E-mail Cadastrado")
    cpf_in = estilo_field("CPF (Somente números)")
    nova_senha_in = estilo_field("Nova Senha", password=True, visible=False)
    confirmar_senha_in = estilo_field("Confirmar Nova Senha", password=True, visible=False)

    btn_acao = ft.ElevatedButton(
        "Verificar Dados",
        bgcolor=cor_botao_azul, 
        color="white",
        width=300, height=55,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=15),
            overlay_color=ft.Colors.WHITE10
        ),
        on_click=lambda e: processar_recuperacao(e)
    )

    def processar_recuperacao(e):
        if id_usuario_validado[0] is None:
            user = validar_recuperacao_db(nome_in.value, email_in.value, cpf_in.value)
            
            if user:
                id_usuario_validado[0] = user['id_user']
                nome_in.visible = email_in.visible = cpf_in.visible = False
                nova_senha_in.visible = confirmar_senha_in.visible = True
                btn_acao.text = "Alterar Senha"
                page.snack_bar = ft.SnackBar(
                    ft.Text("Dados confirmados! Digite a nova senha.", color="white"), 
                    bgcolor=cor_destaque_verde
                )
                page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Dados não conferem!"), bgcolor="#B91C1C")
                page.snack_bar.open = True
        
        else:
            if nova_senha_in.value == confirmar_senha_in.value and len(nova_senha_in.value) >= 4:
                sucesso = resetar_senha_db(id_usuario_validado[0], nova_senha_in.value)
                if sucesso:
                    page.snack_bar = ft.SnackBar(ft.Text("Senha alterada com sucesso!"), bgcolor=cor_destaque_verde)
                    page.snack_bar.open = True
                    on_login()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Erro no banco de dados."), bgcolor="red")
                    page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Senhas incompatíveis ou curtas!"), bgcolor="orange")
                page.snack_bar.open = True
        
        page.update()

    # --- LAYOUT COM CORREÇÃO DE ALINHAMENTO ---
    page.add(
        ft.Container(
            expand=True,
            content=ft.Container(
                bgcolor=cor_card_principal,
                padding=40,
                border_radius=30,
                border=ft.border.all(1, cor_borda),
                width=420,
                content=ft.Column([
                    ft.Icon(ft.Icons.LOCK_RESET, size=80, color=cor_destaque_verde),
                    ft.Text("RECUPERAR ACESSO", size=24, weight="bold", color=cor_texto_high),
                    ft.Text("Validação de identidade", size=14, color=cor_texto_low),
                    ft.Divider(height=20, color="transparent"),
                    nome_in, 
                    email_in, 
                    cpf_in,
                    nova_senha_in, 
                    confirmar_senha_in,
                    ft.Divider(height=10, color="transparent"),
                    btn_acao,
                    ft.TextButton(
                        "Voltar ao Login", 
                        on_click=lambda _: on_login(), 
                        style=ft.ButtonStyle(color=cor_texto_low)
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
            )
        )
    )
    page.update()