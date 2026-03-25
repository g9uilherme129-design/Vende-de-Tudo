# Importa a biblioteca Flet, que serve para criar interfaces
import flet as ft 

# Essa é a função principal, onde tudo acontece
def main(page: ft.Page):
    page.title = "Registrar Vendas" # Define o título da janela do aplicativo
    page.bgcolor = "black" # Define a cor de fundo da página como preto
    page.theme_mode = ft.ThemeMode.DARK # Ativa o modo escuro do aplicativo
    page.padding = 20 # Cria um espaço interno (margem) de pixels em volta do conteúdo
    
    # Função que será chamada quando algum evento acontecer (ex: clicar em botão)
    def salvar_venda(e):
        # Mostra uma mensagem no console (terminal) dizendo que a venda foi registrada
        print("Venda registrada com sucesso!")

    # Cria uma "caixa" (container) que vai guardar todo o formulário
    formulario = ft.Container(
        bgcolor="#0F1C3F",  # Cor de fundo da caixa (azul escuro)
        border_radius=15,  # Deixa as bordas arredondadas
        padding=20,  # Espaço interno dentro da caixa

        # Dentro da caixa, usamos uma Coluna para os itens ficarem um embaixo do outro
        content=ft.Column(
            spacing=15,   # Espaço entre os itens da coluna
            controls=[   # Lista de elementos que vão aparecer na tela
                ft.Text("Registrar Venda", size=22, weight="bold"),      # Título do formulário
                ft.Text("PRODUTO", size=12, color="grey"),  # Texto pequeno indicando o campo de produto
                ft.TextField(     # Campo onde o usuário vai digitar o produto
                    hint_text="BUSCAR...",     # Texto que some quando você começa a digitar
                    prefix_icon=ft.Icons.SEARCH,     # Ícone de lupa dentro do campo
                    border_radius=20,      # Bordas arredondadas do campo
                    bgcolor="#162447",      # Cor de fundo do campo
                    border_color="transparent",      # Remove a borda visível
                ),
                ft.Text("QUANTIDADE", size=12, color="grey"),  # Texto indicando o campo de quantidade
                ft.TextField(   # Campo para digitar a quantidade do produto
                    hint_text="1",   # Valor padrão sugerido
                    prefix_icon=ft.Icons.NUMBERS,    # Ícone de números
                    border_radius=20,   # Bordas arredondadas
                    bgcolor="#162447",     # Cor de fundo do campo
                    border_color="transparent",    # Remove a borda visível
                    keyboard_type=ft.KeyboardType.NUMBER,
                ),
                ft.Text("SUBTOTAL ESTIMADO", size=12, color="grey"),  # Etiqueta para o valor total
                ft.TextField(  # Campo para o valor em dinheiro
                    hint_text="R$ 0,00",   # Texto inicial mostrando valor zerado
                    prefix_icon=ft.Icons.ATTACH_MONEY,   # Ícone de dinheiro
                    border_radius=20, # Bordas arredondadas
                    bgcolor="#162447",  # Cor de fundo
                    border_color="transparent", # Remove a borda visível
                ),
                ft.Text("FORMA DE PAGAMENTO", size=12, color="grey"),  # Texto indicando a forma de pagamento
                ft.Dropdown(  # O Dropdown é aquela listinha que "abre" quando você clica
                    border_radius=20,  # Bordas arredondadas
                    bgcolor="#162447", # Cor de fundo
                    border_color="transparent",  # Remove a borda visível
                    options=[  # Opções que o usuário pode escolher
                        ft.dropdown.Option("PIX"),
                        ft.dropdown.Option("CARTÃO DE CRÉDITO"),
                        ft.dropdown.Option("CARTÃO DE DÉBITO"),
                        ft.dropdown.Option("DINHEIRO"),
                    ],
                ),
                ft.Container(height=10),  # Espaço vazio só para dar um respiro no layout
                ft.ElevatedButton( 
                    "Registrar Venda", # Texto do botão
                    icon=ft.Icons.SAVE, # Ícone de salvar
                    on_click=salvar_venda,   # Quando clicar, chama a função salvar_venda
                    style=ft.ButtonStyle(  # Estilo do botões
                        bgcolor="#0867F5",  # Cor azuç do botões
                        shape=ft.RoundedRectangleBorder(radius=20), # Bordas arredondadas
                        padding=20,   # Espaço interno do botão
                    ),
                    width=250,    # Largura do botão
                ),
            ],
        ),
    )
    page.add(  # Adiciona conteúdo na página
        ft.Column(
            expand=True,  # Faz a coluna ocupar todo o espaço da tela
            horizontal_alignment="center",   # Centraliza os itens na horizontal (no meio da tela)
            # Lista de elementos dentro da coluna
            controls=[formulario],  # Aqui estamos colocando o formulário que você criou
        )
    )
    page.navigation_bar = ft.NavigationBar(  # Cria a barra de navegação na parte de baixo do app
        selected_index=0, # Começa com o primeiro ícone selecionado
        bgcolor="#0F1C3F", # Mesma cor azul do formulário para combinar

    # Botões da barra de navegação
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY, label="Estoque"),
            ft.NavigationBarDestination(icon=ft.Icons.GROUP, label="Usuários"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Perfil"),
        ],
    )
# Inicia o aplicativo chamando a função main
ft.app(target=main)