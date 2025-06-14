import flet as ft
from assets import create_add_button, create_client_card, create_search_bar
from db import init_db, get_clients, get_transactions


def main(page: ft.Page):

    def affichage_transac(lvc):
        transacs = get_transactions()
        lv2 = ft.ListView(spacing=10)
        for transac in transacs:
            lv2.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{transac['date']} - {transac['operation']}"),
                    subtitle=ft.Text(f"{transac['mail']} - {transac['montant']} €"),
                    leading=ft.Icon(ft.Icons.TRANSACTION_OUTLINED),
                    trailing=ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINED),
                )
            )
        lvc.content = lv2
        page.add(lvc)

    page.title = "Accueil"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0

    init_db()
    lv = ft.ListView(spacing=10)
    boutton_ajout = create_add_button(page, lv)
    boutton_li_transac = ft.FloatingActionButton(
        icon=ft.Icons.ASSESSMENT_OUTLINED, on_click=lambda x : affichage_transac(lvc), bgcolor=ft.Colors.LIME_300
    )

    page.overlay.append(
        ft.Container(
            boutton_ajout,
            alignment=ft.alignment.bottom_right,
            margin=20,
        )
    )

    page.overlay.append(
        ft.Container(
            boutton_li_transac,
            alignment=ft.alignment.bottom_left,
            margin=20,
        )
    )


    clients = get_clients()
    
    
    lvc = ft.Container(
        content=lv,
        expand=True,
    )
    search = create_search_bar(page, lv)

    page.add(
        ft.Container(
            ft.Row(
                [
                    search
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLUE,
            padding=ft.padding.all(20),
        ),
    )
    for client in clients:
        lv.controls.append(
            create_client_card(client['nom'], client['prenom'], client['mail'], page, lv)
        )
    page.add(lvc)




ft.app(main)