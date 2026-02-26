import flet as ft

def produto(page: ft.Page, on_stock):
    page.controls.clear()
    page.title = "Cadastro de Novo Produto"
    page.theme_mode = ft.ThemeMode.DARK # Preto 
    page.bgcolor = "#050505"
    page.window_width = 400
    page.window_height = 800
    page.padding = 20

    def estilo_input(label, hint="", value="", width=None, read_only=False, on_change=None):
        return ft.Column([
            ft.Text(label, size=11, color=ft.colors.TEAL_700, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.TextField(
                    value=value,
                    hint_text=hint,
                    hint_style=ft.TextStyle(color=ft.colors.GREY_700),
                    border=ft.InputBorder.NONE,
                    content_padding=15,
                    read_only=read_only,
                    on_change=on_change,
                    text_style=ft.TextStyle(color="white"),
                ),
                bgcolor="#0A122A",
                border=ft.border.all(1, "#1E2B4E"),
                border_radius=10,
                width=width if width else 360,
            )
        ], spacing=5)

    def novo_produto():
        # Estados para o formulário
        nome, set_nome = ft.use_state("")
        fornecedor, set_fornecedor = ft.use_state("")
        codigo, set_codigo = ft.use_state("SW-001")
        categoria, set_categoria = ft.use_state("Moda")

        return ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Novo Produto", size=28, weight=ft.FontWeight.BOLD, color="white"),
                ft.Divider(height=10, color="transparent"),

                # Chamadas da função estilo_input com os parênteses fechados corretamente
                estilo_input("NOME DO PRODUTO", value=nome, on_change=lambda e: set_nome(e.control.value)),
                estilo_input("FORNECEDOR", value=fornecedor, on_change=lambda e: set_fornecedor(e.control.value)),

                ft.Row(
                    controls=[
                        estilo_input("ID / CÓDIGO", value=codigo, width=170, read_only=True),
                        estilo_input("CATEGORIA", value=categoria, width=170, on_change=lambda e: set_categoria(e.control.value)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),

                ft.Divider(height=20, color="transparent"),

                ft.Container(
                    content=ft.ElevatedButton(
                        "Adicionar",
                        style=ft.ButtonStyle(
                            color="white",
                            bgcolor=ft.colors.BLUE_800,
                            shape=ft.RoundedRectangleBorder(radius=25),
                        ),
                        on_click=lambda _: print(f"Salvando: {nome}, {fornecedor}, {categoria}"),
                        width=200,
                    ),
                ),

                ft.TextButton("Voltar", on_click=lambda _: on_stock(), style=ft.ButtonStyle(color="grey")),
            ],
            spacing=15
        )

    # Importante: para usar Hooks, o Flet precisa renderizar o componente funcional
    page.add(novo_produto())
    page.update()

if __name__ == "__main__":
    def mock_stock():
        print("Voltando para o estoque...")
    
    ft.app(target=lambda page: produto(page, mock_stock))