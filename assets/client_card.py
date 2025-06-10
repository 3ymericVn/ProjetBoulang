import flet as ft

def create_client_card(nom: str, prenom: str, mail: str) -> ft.Container:
    return ft.Container(
        content=ft.ListTile(
            leading=ft.CircleAvatar(
                content=ft.Text(nom[0].upper()),
                bgcolor=ft.Colors.DEEP_ORANGE_300,
                radius=20,
            ),
            title=ft.Text(f"{nom} {prenom}", size=18, weight=ft.FontWeight.BOLD),
            subtitle=ft.Text(mail, size=14, italic=True),
            on_click=lambda x: print(f"{prenom} {nom} clicked!"),
        ),
        bgcolor=ft.Colors.TEAL_100,
        border_radius=12,
        padding=10,
        margin=5
    )