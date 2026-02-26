import flet as ft
import flet_charts as fch
from datetime import datetime
from db import conectar


def home_page(page: ft.Page, on_logout, on_stock, on_users, on_perfil):

    # =============================
    # FUNÇÕES DO BANCO
    # =============================

    def buscar_receita_mes():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        mes = datetime.now().month
        ano = datetime.now().year

        cursor.execute("""
            SELECT SUM(total) as total
            FROM vendas
            WHERE MONTH(data_venda) = %s 
            AND YEAR(data_venda) = %s
        """, (mes, ano))

        resultado = cursor.fetchone()
        cursor.close()
        conn.close()

        return resultado["total"] or 0


    def buscar_ranking():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT u.nome,
                COUNT(v.id) as total_vendas,
                SUM(v.total) as total_valor
            FROM vendas v
            JOIN usuarios u ON v.usuario_id = u.id
            WHERE MONTH(v.data_venda) = MONTH(CURDATE())
            GROUP BY u.nome
            ORDER BY total_valor DESC
            LIMIT 3
        """)

        ranking = cursor.fetchall()
        cursor.close()
        conn.close()

        return ranking


    # =============================
    # BUSCAR DADOS
    # =============================

    receita_atual = buscar_receita_mes()
    ranking_db = buscar_ranking()

    # =============================
    # UI
    # =============================

    page.controls.clear()
    page.bgcolor = "#000000"

    page.appbar = ft.AppBar(
        title=ft.Text("Vende de Tudo"),
        bgcolor="#0b1445"
    )

    # RECEITA
    card_receita = ft.Container(
        padding=15,
        border_radius=20,
        bgcolor="#0b1445",
        content=ft.Column(
            [
                ft.Text("RECEITA DO MÊS", size=12, color=ft.Colors.WHITE_70),
                ft.Text(
                    f"R$ {receita_atual:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREEN
                ),
            ]
        )
    )

    # RANKING
    ranking_itens = []

    for r in ranking_db:
        ranking_itens.append(
            ft.Text(
                f"{r['nome']} - R$ {r['total_valor']:,.2f}",
                color=ft.Colors.WHITE
            )
        )

    ranking = ft.Container(
        padding=15,
        border_radius=20,
        bgcolor="#0b1445",
        content=ft.Column(ranking_itens)
    )

    conteudo = ft.Column(
        [
            ft.Text("Consolidação",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE),
            ft.Container(height=15),
            card_receita,
            ft.Container(height=15),
            ranking,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    page.add(conteudo)
    page.update()