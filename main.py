import flet as ft
from login import login_view
from tela_inicial import home_page
from gerenciar_estoque import estoque
from gerenciar_usuario import usuarios
from perfil import perfil_page
from novo_produto import produto
from editar_produto import editar_produto
from novo_usuario import novo_usuario
from editar_usuario import editar_usuario   
from configuracoes import configuracoes_page
from desativar_usuario import tela_desativar_usuario
from registrar_venda import tela_registrar_venda
from gerenciar_vendas import gerenciar_vendas
from gerenciar_fornecedores import tela_fornecedores
from novo_fornecedor import novo_fornecedor
from database import buscar_tema_db
from reativar_usuario import reativar_user
from gerenciar_categoria import gerenciar_categorias
from editar_fornecedor import editar_fornecedor
from recuperar_senha import tela_recuperacao
from editar_venda import editar_venda
from termos import game_page
from database import buscar_dados_completos_perfil, buscar_dados_home
from tela_log import tela_log
from log import write_log


def main(page: ft.Page):
    page.title = "Vende de Tudo"
    page.padding = 20
    page.user_data = None
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 400
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- FUNÇÃO GLOBAL PARA ALTERAR TEMA E REFRESH ---
    def alternar_tema_global():
        from database import salvar_tema_db
        novo_tema_dark = page.theme_mode != ft.ThemeMode.DARK
        page.theme_mode = ft.ThemeMode.DARK if novo_tema_dark else ft.ThemeMode.LIGHT
        
        id_usuario = page.user_data.get("id_user") if page.user_data else None
        if id_usuario:
            salvar_tema_db(id_usuario, novo_tema_dark)
            print(f"Tema {page.theme_mode} salvo para o usuário {id_usuario}")

        aplicar_tema_visual(novo_tema_dark)
        carregar_perfil()

    def aplicar_tema_visual(eh_dark):
        if eh_dark:
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = "#050A18"
            # Criando atributos dinâmicos direto no page para suas outras telas lerem:
            page.cor_card = "#0b1445"
            page.cor_texto = ft.Colors.WHITE
            page.cor_accent = "#1679f2"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = "#F0F4FF"
            # Criando atributos dinâmicos direto no page para suas outras telas lerem:
            page.cor_card = "#D1D5DB"
            page.cor_texto = "#DA7D7D"
            page.cor_accent = "#D0D1D3"
        
        page.update()

    # ---------------------------
    # Funções de Navegação
    # ---------------------------

    def carregar_home(dados_usuario=None):
        # --- 1. PRESERVA OS DADOS E CONFIGURA O ID DO USUÁRIO ---
        if dados_usuario:
            page.user_data = dados_usuario
            
            # Garante que vai salvar como "ADMIN" ou "VENDEDOR" limpo e em maiúsculo
            cargo_bruto = dados_usuario.get('perfil') or 'VENDEDOR'
            page.tipo_usuario = str(cargo_bruto).upper().strip()
            
            # Garante o ID na propriedade certa que a Home precisa ler
            page.id_user = dados_usuario.get('id_user') or dados_usuario.get('id_usuario')
            
            # --- 2. SISTEMA DE TEMA HISTÓRICO ---
            id_atual = page.id_user
            try:
                tema_db = buscar_tema_db(id_atual)
                aplicar_tema_visual(eh_dark=(tema_db == 1))
            except Exception as e:
                print(f"Erro ao carregar tema inicial: {e}")
                aplicar_tema_visual(eh_dark=True)

        page.controls.clear()
        
        # --- 3. CHAMADA DA HOME COM OS CALLBACKS ORIGINAIS CORRETOS ---
        home_page(
            page,
            on_logout=fazer_logout,           # Nome corrigido para o seu padrão antigo
            on_stock=carregar_stock,           # Nome corrigido para o seu padrão antigo
            on_users=carregar_usuarios,
            on_perfil=carregar_perfil,
            on_log=carregar_log,
            on_venda=carregar_registrar_venda,
            on_vendas=carregar_vendas
        )
        page.update()

    def carregar_fornecedores():
        tela_fornecedores(
            page,
            on_home=carregar_home,
            on_vendas=carregar_vendas,
            on_stock=carregar_stock,
            on_usuarios=carregar_usuarios,
            on_log=carregar_log,
            on_adicionar_fornecedor=carregar_novo_fornecedor,
            on_editar_fornecedor=carregar_editar_fornecedor,
            on_perfil=carregar_perfil
        )

    def carregar_novo_fornecedor():
        novo_fornecedor(page, on_voltar=carregar_fornecedores)

    def carregar_editar_fornecedor(id_forn):
        editar_fornecedor(page, on_back=carregar_fornecedores, id_fornecedor=id_forn)

    def carregar_registrar_venda():
        tela_registrar_venda(page, on_voltar=carregar_home)

    def carregar_stock():
        estoque(
            page,
            on_logout=fazer_logout,
            on_home=carregar_home,
            on_vendas=carregar_vendas,
            on_users=carregar_usuarios,
            on_log=carregar_log,
            on_perfil=carregar_perfil,
            on_adicionar_produto=carregar_novo_produto,
            on_editar_produto=carregar_editar_produto,
            on_fornecedores=carregar_fornecedores,
            on_categorias=carregar_categoria
        )

    def carregar_categoria():
        gerenciar_categorias(page, on_back=carregar_stock)

    def carregar_vendas():
        gerenciar_vendas(
            page,
            on_logout=fazer_logout,
            on_home=carregar_home,
            on_users=carregar_usuarios,
            on_vendas=carregar_vendas,
            on_log=carregar_log,
            on_stock=carregar_stock,
            on_perfil=carregar_perfil,
            on_editar_venda=carregar_editar_venda,
            on_registrar_venda=carregar_registrar_venda
        )

    def carregar_editar_venda(id_venda):
        editar_venda(page, on_back=carregar_vendas, id_venda=id_venda)

    def carregar_usuarios():
        usuarios(
            page, 
            on_logout=fazer_logout,
            on_home=carregar_home,
            on_vendas=carregar_vendas,
            on_stock=carregar_stock,
            on_perfil=carregar_perfil,
            on_log=carregar_log,
            on_adicionar_usuario=carregar_novo_usuario,
            on_editar_usuario=carregar_editar_usuario,
            on_desativar_usuario=carregar_desativar_usuario,
            user_data=page.user_data,
            on_reativar_user=carregar_reativar_user
        )
        
    def carregar_perfil():
        page.controls.clear() 
        perfil_page(
            page, 
            on_home=lambda: carregar_home(page.user_data),
            on_stock=carregar_stock,
            on_vendas=carregar_vendas,
            on_users=carregar_usuarios,
            on_logout=fazer_logout,
            on_game=carregar_jogo,
            on_theme_change=alternar_tema_global,
            on_log=carregar_log,
            on_config=carregar_config
        )

    def carregar_jogo():
        game_page(page, on_back=carregar_perfil)

    def carregar_config():
        configuracoes_page(page, on_back=carregar_perfil, user_data=page.user_data)

    def fazer_logout():
        page.user_data = None
        page.tipo_usuario = None  # Reseta o cargo no logout
        page.navigation_bar = None
        page.appbar = None
        carregar_login()
        
    def carregar_novo_produto():
        produto(page, on_stock=carregar_stock)

    def carregar_editar_produto(id_prod):
        editar_produto(page, id_produto=id_prod, on_stock=carregar_stock)

    def carregar_novo_usuario():
        novo_usuario(page, on_users=carregar_usuarios)
        
    def tratar_clique_status(usuario_selecionado, carregar_tela_desativar, carregar_tela_reativar):
        if usuario_selecionado.get("status_user") == 1:
            carregar_tela_desativar(usuario_selecionado)
        else:
            carregar_tela_reativar(usuario_selecionado)

    def carregar_editar_usuario(id_user):
        editar_usuario(page, id_usuario=id_user, on_users=carregar_usuarios)

    def carregar_desativar_usuario(dados_do_usuario_alvo):
        def voltar_com_msg_desativado():
            carregar_usuarios()
            page.snack_bar = ft.SnackBar(ft.Text(f"Usuário {dados_do_usuario_alvo.get('nome_user','')} desativado com sucesso!"), bgcolor="green")
            page.snack_bar.open = True
            # grava confirmação no log
            try:
                admin_id = page.user_data.get('id_user') if page.user_data else None
                write_log('confirmacao_desativacao', user_id=admin_id, details=f"{dados_do_usuario_alvo.get('id_user')} - {dados_do_usuario_alvo.get('nome_user')}")
            except Exception:
                pass
            page.update()

        tela_desativar_usuario(page=page, user_data=dados_do_usuario_alvo, on_voltar=voltar_com_msg_desativado)

    def carregar_reativar_user(dados_do_usuario):
        def voltar_com_msg_reativado():
            carregar_usuarios()
            page.snack_bar = ft.SnackBar(ft.Text(f"Usuário {dados_do_usuario.get('nome_user','')} reativado com sucesso!"), bgcolor="green")
            page.snack_bar.open = True
            # grava confirmação no log
            try:
                admin_id = page.user_data.get('id_user') if page.user_data else None
                write_log('confirmacao_reativacao', user_id=admin_id, details=f"{dados_do_usuario.get('id_user')} - {dados_do_usuario.get('nome_user')}")
            except Exception:
                pass
            page.update()

        reativar_user(page, user_data=dados_do_usuario, on_gerenciar_usuario=voltar_com_msg_reativado)

    def carregar_log():
        tela_log(
            page,
            on_back=lambda: carregar_home(page.user_data),
            on_home=carregar_home,
            on_vendas=carregar_vendas,
            on_stock=carregar_stock,
            on_users=carregar_usuarios,
            on_perfil=carregar_perfil,
            on_log=carregar_log,
            is_admin=(getattr(page, 'tipo_usuario', '').upper().strip() == 'ADMIN')
        )

    def carregar_recuperar_senha():
        from recuperar_senha import tela_recuperacao
        tela_recuperacao(page=page, on_login=carregar_login)

    def carregar_login():
        page.appbar = None
        page.navigation_bar = None
        page.controls.clear()
        aplicar_tema_visual(eh_dark=False)
        # Re-renderiza a tela de login ao redimensionar para aplicar responsividade
        page.on_resize = lambda e: carregar_login()
        page.add(login_view(page, on_login_sucesso=carregar_home, on_recuperar_senha=carregar_recuperar_senha))
        page.update()
        
    carregar_login()

ft.run(main)