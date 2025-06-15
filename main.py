import flet as ft
from assets import create_add_button, create_client_card, create_search_bar, create_transaction_table
from db import init_db, get_clients, get_transactions

def main(page: ft.Page):
    def affichage_transac(lvc: ft.Container, lv: ft.ListView, boutton_li_transac: ft.FloatingActionButton):
        transacs = get_transactions()
        lv2 = ft.ListView(spacing=10)
        datatable = create_transaction_table(transacs)
        lv2.controls.append(datatable)
        lvc.content = lv2
        page.add(lvc)
        boutton_li_transac.icon = ft.Icons.HOME_FILLED
        boutton_li_transac.on_click = lambda x : affichage_clients(lvc, lv, boutton_li_transac)
        page.update()

    def affichage_clients(lvc: ft.Container, lv: ft.ListView, boutton_li_transac: ft.FloatingActionButton):
        lvc.content = lv
        boutton_li_transac.icon = ft.Icons.ASSESSMENT_OUTLINED
        boutton_li_transac.on_click = lambda x : affichage_transac(lvc, lv, boutton_li_transac)
        page.update()

    page.title = "Accueil"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.only(0, 0, 0, 0)
    page.window.frameless = False

    init_db()
    lv = ft.ListView(spacing=10)
    lvc = ft.Container(
        content=lv,
        expand=True,
    )
    boutton_ajout = create_add_button(page, lv, lvc)
    boutton_li_transac = ft.FloatingActionButton(
        icon=ft.Icons.ASSESSMENT_OUTLINED, on_click=lambda x : affichage_transac(lvc, lv, boutton_li_transac), bgcolor=ft.Colors.LIME_300
    )

    page.update()

    clients = get_clients()
    
    search = create_search_bar(page, lv, lvc)

    page.add(
        ft.Container(
            ft.Row(
                [
                    search, 
                    boutton_li_transac,
                    boutton_ajout,
                ],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLUE,
            padding=ft.padding.all(20),
        ),
    )
    for client in clients:
        lv.controls.append(
            create_client_card(client['nom'], client['prenom'], client['mail'], page, lv, lvc)
        )
    page.add(lvc)


ft.app(main)