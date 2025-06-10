import flet as ft
from assets import create_add_button, create_client_card, create_search_bar
from db import init_db, get_clients

def main(page: ft.Page):
    page.title = "Accueil"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0

    init_db()
    page.floating_action_button = create_add_button(page)
    clients = get_clients()
    
    lv = ft.ListView(spacing=10)
    lvc = ft.Container(
        content=lv
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
            create_client_card(client['nom'], client['prenom'], client['mail'])
        )
    page.add(lvc)

ft.app(main)