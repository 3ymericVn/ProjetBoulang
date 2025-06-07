import flet as ft
from assets import create_add_button
from db.utils import init_db, search_client, get_clients

def main(page: ft.Page):
    page.title = "Accueil"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0

    init_db()
    page.floating_action_button = create_add_button(page)
    clients = get_clients()

    def on_change(e):
        search_results = search_client(e.control.value)
        print(len(search_results))
        lv.controls.clear()
        for client in search_results:
            lv.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{client['nom']} {client['prenom']}"),
                    subtitle=ft.Text(client["mail"]),
                    on_click=lambda x: print(f"{client['nom']} {client['prenom']} clicked!")
                )
            )
        page.update()

    def on_tap(e):
        search.open_view()
    
    lv = ft.ListView(
        ft.ListTile(
            title=ft.Text(f"{client['nom']} {client['prenom']}"),
            subtitle=ft.Text(client["mail"]),
            on_click=lambda x: print(f"{client['nom']} {client['prenom']} clicked!")
        )
        for client in clients
    )
    search = ft.SearchBar(
        bar_hint_text="Rechercher un client",
        on_change=on_change,
        on_tap=on_tap,
        expand=True,
        view_elevation=4,
        controls=[
            lv
        ]
    )
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


ft.app(main)