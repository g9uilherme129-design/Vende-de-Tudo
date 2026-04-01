import flet as ft

def editar_produto(page: ft.Page, on_stock):
    page.controls.clear()
    page.title = "Editar Produto"
    
    # REMOVIDO: page.theme_mode e page.bgcolor fixos para respeitar o global
    page.window_width = 400
    page.window_height = 800
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Lógica de cores adaptáveis
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    cor_texto = ft.Colors.WHITE if is_dark else ft.Colors.BLACK
    cor_input_fundo = "#0A122A" if is_dark else "#F0F2F5"
    cor_borda = "#1E2B4E" if is_dark else "#D1D5DB"

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color="white", # Mantido branco pois a AppBar é escura fixa
            on_click=lambda _: on_stock()
        ),
        title=ft.Text("Editar Produto", size=20, weight="bold", color="white"),
        bgcolor="#0b1445",
        center_title=True,
    )

    def estilo_input(label, hint="", value="", read_only=False, col=None):
        input_field = ft.TextField(
            value=value,
            hint_text=hint,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color=cor_texto), # Dinâmico
            expand=True,
        )
        
        container = ft.Column(
            [
                ft.Text(label, size=11, color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=input_field,
                    bgcolor=cor_input_fundo, # Dinâmico
                    border=ft.border.all(1, cor_borda), # Dinâmico
                    border_radius=10,
                    padding=ft.padding.only(right=10),
                )
            ],
            spacing=5,
            col=col 
        )
        return container, input_field

    # Criando os campos
    nome_container, nome_input = estilo_input("EDITAR PRODUTO", hint="Nome do produto", col=12)
    fornecedor_container, fornecedor_input = estilo_input("FORNECEDOR", hint="Fornecedor", col=12)
    codigo_container, codigo_input = estilo_input("ID / CÓDIGO", value="CL-263", read_only=True, col=6)
    categoria_container, categoria_input = estilo_input("CATEGORIA", value="Moda", col=6)

    def salvar(e):
        print("Alterações do produto salvas com sucesso!")

    layout_campos = ft.ResponsiveRow(
        controls=[
            nome_container,
            fornecedor_container,
            codigo_container, 
            categoria_container, 
        ],
        spacing=15,
        run_spacing=15,
    )

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Divider(height=10, color="transparent"),
                layout_campos,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Salvar Alterações", 
                    on_click=salvar, 
                    width=200,
                    style=ft.ButtonStyle(
                        bgcolor="#1B4F9C",
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=10),
                    )
                ),
            ],
            spacing=10
        )
    )
    page.update()