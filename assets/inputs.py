import flet as ft
from assets.client_card import create_client_card
from db import search_client

def create_search_bar(page: ft.Page, lv: ft.ListView, lvc: ft.Container, home_button: ft.FloatingActionButton) -> ft.TextField:
    def on_change(e):
        search_results = search_client(search.value)
        lv.controls.clear()
        for client in search_results:
            lv.controls.append(
                create_client_card(client['nom'], client['prenom'], client['mail'], page, lv, lvc, home_button)
            )
        page.update()
    search = ft.TextField(
        label="Rechercher un client",
        on_change=on_change,
        expand=True,
    )
    return search