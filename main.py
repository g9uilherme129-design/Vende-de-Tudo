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
            # Sincroniza o user_data global da página
            page.user_data = dados_usuario
            
            # Salvamos no page.data para compatibilidade
            page.data = {
                "user_id": dados_usuario.get('id_user') or dados_usuario.get('id_use'),
                "user_nome": dados_usuario.get('nome_user')
            }
            
            # Aplicação do tema
            id_atual = page.data["user_id"]
            try:
                tema_db = buscar_tema_db(id_atual)
                aplicar_tema_visual(eh_dark=(tema_db == 1))
            except:
                aplicar_tema_visual(eh_dark=True)

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
            on_adicionar_fornecedor=carregar_novo_fornecedor,
            on_editar_fornecedor=carregar_editar_fornecedor,
            on_perfil=carregar_perfil
        )

    def carregar_novo_fornecedor():
        novo_fornecedor(page, on_voltar=carregar_fornecedores)

    def carregar_editar_fornecedor(id_forn):
        editar_fornecedor(
            page, 
            on_back=carregar_fornecedores,
            id_fornecedor=id_forn
        )

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
            on_fornecedores=carregar_fornecedores,
            on_categorias=carregar_categoria
        )

    def carregar_categoria():
        gerenciar_categorias(
            page,
            on_back=carregar_stock
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
            user_data=page.user_data,
            on_reativar_user=carregar_reativar_user
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
            user_data=page.user_data
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
        

    def tratar_clique_status(usuario_selecionado, carregar_tela_desativar, carregar_tela_reativar):
        if usuario_selecionado.get("status_user") == 1:
            carregar_tela_desativar(usuario_selecionado)
        else:
            carregar_tela_reativar(usuario_selecionado)

    def carregar_editar_usuario(id_user):
        editar_usuario(page, id_usuario=id_user, on_users=carregar_usuarios)

    # --- AJUSTE NA FUNÇÃO DE DESATIVAR/REATIVAR ---
    def carregar_desativar_usuario(dados_do_usuario_alvo):
        # Essa função agora é inteligente:
        # No 'usuarios.py', se o cara estiver INATIVO, ela abre o modal de reativação direto.
        # Se estiver ATIVO, ela abre a tela de desativar normal.
        tela_desativar_usuario(
            page=page, 
            user_data=dados_do_usuario_alvo, 
            on_voltar=carregar_usuarios
        )

    def carregar_reativar_user(dados_do_usuario):
        reativar_user(
            page,
            user_data=dados_do_usuario,
            on_gerenciar_usuario=carregar_usuarios
        )

    def carregar_recuperar_senha():
        from recuperar_senha import tela_recuperacao # Import local para evitar erro de circularidade
        tela_recuperacao(
            page=page, 
            on_login=carregar_login # Passa a volta para o login como callback
        )

    def carregar_login():
        page.appbar = None
        page.navigation_bar = None
        page.controls.clear()
        aplicar_tema_visual(eh_dark=False)
        page.add(login_view(page, on_login_sucesso=carregar_home, on_recuperar_senha=carregar_recuperar_senha))
        page.update()

    carregar_login()

ft.app(target=main)