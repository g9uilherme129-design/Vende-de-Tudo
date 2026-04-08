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
from gerenciar_vendas import vendas

def main(page: ft.Page):
    page.title = "Vende de Tudo"
    page.padding = 20
    
    # --- CONFIGURAÇÃO INICIAL DE TEMA ---
    try:
        if hasattr(page, "client_storage") and page.client_storage:
            tema_salvo = page.client_storage.get("app_theme")
        else:
            tema_salvo = None
    except Exception:
        tema_salvo = None

    page.theme_mode = tema_salvo if tema_salvo else ft.ThemeMode.DARK
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- FUNÇÃO GLOBAL PARA ALTERAR TEMA ---
    def alterar_tema(modo):
        if modo == "dark":
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = "#000000"  # Fundo escuro global
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = "#F0F4FF"  # Fundo claro global (o branco azulado)
        
        try:
            if hasattr(page, "client_storage") and page.client_storage:
                page.client_storage.set("app_theme", modo)
        except:
            pass
        

        page.update()
        
        # Recarrega a tela de configurações para atualizar os ícones e textos nela
        carregar_config()

    # ---------------------------
    # Funções de Navegação
    # ---------------------------

    def carregar_home():
        home_page(
            page,
            on_logout=fazer_logout,
            on_stock=carregar_stock,
            on_users=carregar_usuarios,
            on_perfil=carregar_perfil,
            on_venda=carregar_registrar_venda,
            on_vendas=carregar_vendas,
        )

    def carregar_registrar_venda():
        tela_registrar_venda(
            page,
            on_voltar=carregar_home
        )

    def carregar_stock():
        estoque(
            page,
            on_logout=fazer_logout,
            on_home=carregar_home,
            on_vendas=carregar_vendas,
            on_users=carregar_usuarios,
            on_perfil=carregar_perfil,
            on_adicionar_produto=carregar_novo_produto,
            on_editar_produto=carregar_editar_produto
        )

    def carregar_vendas():
        vendas(
            page,
            on_logout=fazer_logout,
            on_home=carregar_home,
            on_users=carregar_usuarios,
            on_stock=carregar_stock,
            on_perfil=carregar_perfil,
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
            on_editar_usuario=carregar_editar_usuario
        )
        
    def carregar_perfil():
        perfil_page(
            page, 
            on_home=carregar_home,
            on_stock=carregar_stock,
            on_vendas=carregar_vendas,
            on_users=carregar_usuarios,
            on_logout=fazer_logout,
            on_config=carregar_config
        )

    def carregar_config():
        configuracoes_page(
            page,
            on_back=carregar_perfil,
            on_change_theme=alterar_tema
        )

    def fazer_logout():
        page.navigation_bar = None
        page.controls.clear()
        carregar_login()
        page.update()
        
    def carregar_novo_produto():
        produto(page, on_stock=carregar_stock)

    def carregar_editar_produto():
        editar_produto(page, on_stock=carregar_stock)

    def carregar_novo_usuario():
        novo_usuario(page, on_users=carregar_usuarios)

    def carregar_editar_usuario():
        editar_usuario(page, on_users=carregar_usuarios)

    def carregar_login():
        page.appbar = None
        page.navigation_bar = None
        page.controls.clear()
        page.add(login_view(page, on_login_sucesso=carregar_home))
        page.update()

    # Configurações de janela
    page.window_width = 400
    page.window_height = 800
    
    carregar_login()

ft.app(main)
