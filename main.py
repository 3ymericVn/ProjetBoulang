import flet as ft
from assets import create_add_button, create_client_card, create_search_bar, create_transaction_table, affichage_transac, affichage_clients, create_list_transac
from db import init_db, get_clients, get_transactions
from mail import send_mail

def main(page: ft.Page):

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
    
    boutton_li_transac = create_list_transac(page, lvc, lv, None)
    boutton_ajout = create_add_button(page, lv, lvc, boutton_li_transac)
    
    boutton_li_transac.on_click = lambda x: affichage_transac(page, lvc, lv, boutton_li_transac)

    page.update()

    clients = get_clients()
    
    search = create_search_bar(page, lv, lvc, boutton_li_transac)

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
            create_client_card(client['nom'], client['prenom'], client['mail'], page, lv, lvc, boutton_li_transac)
        )
    page.add(lvc)


ft.app(main)