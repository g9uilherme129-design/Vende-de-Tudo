import flet as ft

def produto(page: ft.Page, on_stock):

    page.controls.clear()

    page.title = "Cadastro de Novo Produto"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.window_width = 400
    page.window_height = 800
    page.padding = 20

    # INPUT ESTILIZADO
    def estilo_input(label, hint="", value="", width=None, read_only=False):
        campo = ft.TextField(
            value=value,
            hint_text=hint,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color="white"),
        )

        return ft.Column(
            [
                ft.Text(
                    label,
                    size=11,
                    color=ft.Colors.TEAL_700,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(
                    content=campo,
                    bgcolor="#0A122A",
                    border=ft.border.all(1, "#1E2B4E"),
                    border_radius=10,
                    width=width,
                ),
            ],
            spacing=5,
        ), campo  # 👈 retornamos também o campo

    # Criando campos
    nome_container, nome = estilo_input("NOME DO PRODUTO", "Ex: Moletom")
    fornecedor_container, fornecedor = estilo_input("FORNECEDOR / DISTRIBUIDOR", "He-Man Modas")
    codigo_container, codigo = estilo_input("ID / CÓDIGO", value="SW-001", width=170, read_only=True)
    categoria_container, categoria = estilo_input("CATEGORIA", value="Moda", width=170)

    def salvar(e):
        print(
            f"Salvando: {nome.value}, {fornecedor.value}, {categoria.value}"
        )

    page.add(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Novo Produto", size=28, weight=ft.FontWeight.BOLD, color="white"),
                ft.Divider(height=10, color="transparent"),

                nome_container,
                fornecedor_container,

                ft.Row(
                    [
                        codigo_container,
                        categoria_container,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                ft.Divider(height=20, color="transparent"),

                ft.Container(
                    content=ft.ElevatedButton(
                        "Adicionar",
                        style=ft.ButtonStyle(
                            color="white",
                            bgcolor=ft.Colors.BLUE_800,
                            shape=ft.RoundedRectangleBorder(radius=25),
                        ),
                        on_click=lambda _: print(f"Salvando: {nome}, {fornecedor}, {categoria}"),
                    ),
                    alignment=ft.Alignment(0, 0),
                    height=50,
                ),

                ft.TextButton("Voltar", on_click=lambda e: on_stock())
            ],
            spacing=15,
        )
    )

    page.update()