import flet as ft

def main(page: ft.Page):
    page.title = "Cadastro de Novo Produto"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"  # Um preto quase puro(v junior)
    page.window_width = 400
    page.window_height = 800
    page.padding = 20
    # Agora vai centralizar!
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # inputs no grau ta estilizado (CONTAINER)
    def estilo_input(label, hint="", value="", width=None, read_only=False, on_change=None):
        return ft.Column([
            ft.Text(label, size=11, color=ft.colors.TEAL_700, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.TextField(
                    value=value,
                    hint_text=hint,
                    hint_style=ft.TextStyle(color=ft.colors.GREY_700),
                    border=ft.InputBorder.NONE, # Remove a borda normalmente tem
                    content_padding=15,
                    read_only=read_only,
                    on_change=on_change,
                    text_style=ft.TextStyle(color="white"),
                ),
                bgcolor="#0A122A",
                border=ft.border.all(1, "#1E2B4E"),
                border_radius=10,
                width=width if width else 360, # Vai garantir a largura se não for especifica certo jão
            )
        ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.START) # a label vai ficar alinhada á esquerda do input (agora vai dar certo menzinhoo)

    # depois de tudo dando errado mudei para hooks porque vi no GE que rodaria melhor 
    def editar_produto():
        
        produto_inicial = {
            "nome": "Moletom thundercats",
            "fornecedor": "He-Man Modas LTDA",
            "codigo": "SW-099",
            "categoria": "Roupa de Héroi"
        }

        nome, set_nome = ft.use_state(produto_inicial["nome"])
        fornecedor, set_fornecedor = ft.use_state(produto_inicial["fornecedor"])
        codigo, set_codigo = ft.use_state(produto_inicial["codigo"])
        categoria, set_categoria = ft.use_state(produto_inicial["categoria"])


        return ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row([
                    ft.Text("Editar Produto", size=28, weight="bold", color="white"),
            ]), 
            ft.Divider(height=10, color="transparent"),   
                # inputs grandes 
                estilo_input("NOME DO PRODUTO", value=nome, on_change=lambda e: set_nome(e.control.value)),
                estilo_input("FORNECEDOR / DISTRIBUIDOR", value=fornecedor, on_change=lambda e: set_fornecedor(e.control.value)),

                # inputs oequenos
                ft.Row([
                    estilo_input("ID / CÓDIGO", value=codigo, width=170, read_only=True),
                    estilo_input("CATEGORIA", value=categoria, width=170, on_change=lambda e: set_categoria(e.control.value)),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),

                ft.Divider(height=20, color="transparent"),

                # Botão salva edição
                ft.Container(
                    content=ft.ElevatedButton(
                        "Salvar Alterações",
                        style=ft.ButtonStyle(
                            color="white",
                            bgcolor=ft.colors.BLUE_800,
                            shape=ft.RoundedRectangleBorder(radius=25),
                        ),
                        on_click=lambda _: print(f"Salvando: {nome}, {fornecedor}, {categoria}"),
                    ),
                    alignment=ft.alignment.center,
                    height=50,
                ),
                ft.TextButton(
                    "Cancelar",
                    style=ft.ButtonStyle(color=ft.colors.GREY_500),
                    on_click=lambda _: print("Editar cancelada"),
                ),

                ft.Divider(height=10, color="transparente"),
                ft.Text(f"Editar ID: {codigo}", size=10, color="grey")
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    page.add(editar_produto())

ft.app(target=main)