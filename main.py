import flet as ft
from assets import create_add_button, add_client_tile
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
        search_results = search_client(search.value)
        lv.controls.clear()
        for client in search_results:
            prenom = client['prenom']
            nom = client['nom']
            mail = client['mail']
            lv.controls.append(
                ft.Container(   
                    content=ft.ListTile(
                        leading=ft.CircleAvatar(
                            content=ft.Text(nom[0].upper()),
                            bgcolor=ft.Colors.DEEP_ORANGE_300,
                            radius=20,
                        ),
                        title=ft.Text(f"{prenom} {nom}", size=18, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(mail, size=14, italic=True),
                        on_click=lambda x: print(f"{prenom} {nom} clicked!"),
                    ),
                    bgcolor=ft.Colors.TEAL_100,
                    border_radius=12,
                    padding=10,
                    margin=5
                )
            )
        page.update()

    
    lv = ft.ListView(spacing=10)
    lvc = ft.Container(
        content=lv
    )
    search = ft.TextField(
        label="Rechercher un client",
        on_change=on_change,
        expand=True,
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
    for client in clients:
        prenom = client['prenom']
        nom = client['nom']
        mail = client['mail']
        lv.controls.append(
            ft.Container(   
                content=ft.ListTile(
                    leading=ft.CircleAvatar(
                        content=ft.Text(nom[0].upper()),
                        bgcolor=ft.Colors.DEEP_ORANGE_300,
                        radius=20,
                    ),
                    title=ft.Text(f"{prenom} {nom}", size=18, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(mail, size=14, italic=True),
                    on_click=lambda x: print(f"{prenom} {nom} clicked!"),
                ),
                bgcolor=ft.Colors.TEAL_100,
                border_radius=12,
                padding=10,
                margin=5
            )
        )
    page.add(lvc)

ft.app(main)