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

def main(page: ft.Page):
    page.title = "Vende de Tudo"
    page.padding = 20
    page.user_data = None
    
    page.window_width = 400
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- FUNÇÃO GLOBAL PARA ALTERAR TEMA ---
    def aplicar_tema_visual(eh_dark):
        """Aplica o tema visualmente na página"""
        if eh_dark:
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = "#000000"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = "#F0F4FF"
        page.update()

    # ---------------------------
    # Funções de Navegação
    # ---------------------------

    def carregar_home(dados_usuario=None):
        if dados_usuario:
            page.user_data = dados_usuario
            
            # --- NOVO: Ao entrar na home (pós-login), aplica o tema do banco ---
            id_atual = dados_usuario.get('id_user') or dados_usuario.get('id_use')
            try:
                # O banco retorna 1 para Dark, 0 para Light
                tema_db = buscar_tema_db(id_atual)
                aplicar_tema_visual(eh_dark=(tema_db == 1))
            except:
                aplicar_tema_visual(eh_dark=True) # Fallback

        page.controls.clear()
        home_page(
            page,
            on_logout=fazer_logout,
            on_stock=carregar_stock,
            on_users=carregar_usuarios,
            on_perfil=carregar_perfil,
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
            on_adicionar_fornecedor=carregar_novo_fornecedor
        )

    def carregar_novo_fornecedor():
        novo_fornecedor(page, on_voltar=carregar_fornecedores)

    def carregar_registrar_venda():
        tela_registrar_venda(page, on_voltar=carregar_home)

    def carregar_stock():
        estoque(
            page,
            on_logout=fazer_logout,
            on_home=carregar_home,
            on_vendas=carregar_vendas,
            on_users=carregar_usuarios,
            on_perfil=carregar_perfil,
            on_adicionar_produto=carregar_novo_produto,
            on_editar_produto=carregar_editar_produto,
            on_fornecedores=carregar_fornecedores
        )

    def carregar_vendas():
        gerenciar_vendas(
            page,
            on_logout=fazer_logout,
            on_home=carregar_home,
            on_users=carregar_usuarios,
            on_stock=carregar_stock,
            on_perfil=carregar_perfil,
            on_registrar_venda=carregar_registrar_venda
        )

    def carregar_usuarios():
        usuarios(
            page, 
            on_logout=fazer_logout,
            on_home=carregar_home,
            on_vendas=carregar_vendas,
            on_stock=carregar_stock,
            on_perfil=carregar_perfil,
            on_adicionar_usuario=carregar_novo_usuario,
            on_editar_usuario=carregar_editar_usuario,
            on_desativar_usuario=carregar_desativar_usuario,
            user_data=page.user_data
        )
        
    def carregar_perfil():
        perfil_page(
            page, 
            on_home=lambda: carregar_home(page.user_data),
            on_stock=carregar_stock,
            on_vendas=carregar_vendas,
            on_users=carregar_usuarios,
            on_logout=fazer_logout,
            on_config=carregar_config,
        )

    def carregar_config():
        configuracoes_page(
            page,
            on_back=carregar_perfil,
            user_data=page.user_data # Passando os dados para salvar o tema
        )

    def fazer_logout():
        page.user_data = None
        page.navigation_bar = None
        page.appbar = None
        carregar_login()
        
    def carregar_novo_produto():
        produto(page, on_stock=carregar_stock)

    def carregar_editar_produto(id_prod):
        editar_produto(page, id_produto=id_prod, on_stock=carregar_stock)

    def carregar_novo_usuario():
        novo_usuario(page, on_users=carregar_usuarios)

    def carregar_editar_usuario(id_user):
        editar_usuario(page, id_usuario=id_user, on_users=carregar_usuarios)

    def carregar_desativar_usuario(dados_do_usuario_alvo):
        tela_desativar_usuario(
            page=page, 
            user_data=dados_do_usuario_alvo, 
            on_voltar=carregar_usuarios
        )

    def carregar_login():
        page.appbar = None
        page.navigation_bar = None
        page.controls.clear()
        # Reset para tema claro no login para melhor leitura
        aplicar_tema_visual(eh_dark=False)
        page.add(login_view(page, on_login_sucesso=carregar_home))
        page.update()

    carregar_login()

ft.app(target=main)