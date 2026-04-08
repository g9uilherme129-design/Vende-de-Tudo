import flet as ft
from database import Database

db = Database()

def produto(page: ft.Page, on_stock):
    page.controls.clear()
    
    # REMOVIDO: page.bgcolor e page.theme_mode fixos para seguir o sistema global
    page.padding = 20


    def estilo_input(label, hint="", value="", read_only=False, col=None):
        input_field = ft.TextField(
            value=value,
            hint_text=hint,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
            border=ft.InputBorder.NONE,
            content_padding=15,
            read_only=read_only,
            text_style=ft.TextStyle(color=cor_texto_input),
            expand=True,
        )
        
        container = ft.Column(
            [
                ft.Text(label, size=11, color=cor_label, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=input_field,
                    bgcolor=cor_fundo_input,
                    border=ft.border.all(1, cor_borda_input),
                    border_radius=10,
                    padding=ft.padding.only(right=10),
                )
            ],
            spacing=5,
            col=col 
        )
        return container, input_field

    # Campos Responsivos
    nome_container, nome_input = estilo_input("NOME DO PRODUTO", col={"sm": 12, "md": 12})
    fornecedor_container, fornecedor_input = estilo_input("FORNECEDOR", col=12)
    codigo_container, codigo_input = estilo_input("ID / CÓDIGO", value="SW-001", read_only=True, col=6)
    categoria_container, categoria_input = estilo_input("CATEGORIA", value="Moda", col=6)
    quantidade_container, quantidade_input = estilo_input("QUANTIDADE", value="1", col=12)
    venda_container, venda_input = estilo_input("VENDA(R$)", value="0,00", col=6)
    custo_container, custo_input = estilo_input("CUSTO(R$)", value="0,00", col=6)

    def salvar_clique(e):
        nome = nome_input.value
        fornecedor_id = 1
        categoria_id =1
        codigo = codigo_input.value
        validade = "2026-12-31"
        custo = custo_input.value.replace("R$", "").replace(",", ".")
        venda = venda_input.value.replace("R$", "").replace(",", ".")
        embalagem = "unidade"
        try:  
            qtd = int(quantidade_input.value)
        except:
            qdt = 0
            
        lote = "L-001"

        if not nome:
            nome_input.error_text = "Digite o nome do produto"
            page.update()
            return

        sucesso = db.inserir_estoque(
            fornecedor_id,
            categoria_id,
            codigo,
            validade,
            custo,
            venda,
            embalagem,
            qtd,
            lote,
        )

        if sucesso:
            nome_input.value = ""
            page.snack_bar = ft.SnackBar(ft.Text("produto salvo com susseso"), bgcolor="green")
            page.snack_bar.open = True

        else:
            page.snack_bar = ft.SnackBar(ft.Text("erro ao conectar ao Banco"), bgcolor="red")
            page.snack_bar.open = True
       
        page.update()

    page.add(
        ft.Colunm(
            scroll=ft.ScrollMode.AUTO,
            horizontal_aligment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("novo produto", size=28, weight=ft.FontWeight.BOLD, color="white"),
                nome_container,
                fornecedor_container,
                ft.Row([codigo_container, categoria_container], alignment=ft.MainAxisAlignment.CENTER),
                ft.ElevatedButton("Adicionar", on_click=salvar_clique, width=200),
                ft.TextButton("voltar", on_click=lambda _: on_stock()),
            ],
            spacing=10
        )
    )
    page.update()