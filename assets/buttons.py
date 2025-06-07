import re
import flet as ft
from db.utils import add_client

EMAIL_REGEX = r"^\S+@\S+\.\S+$"

def fab_pressed(page: ft.Page):
    def validate_input(e):
        if all([nom.value, prenom.value, mail.value]) and re.match(EMAIL_REGEX, mail.value):
            submit.disabled = False
        else:
            submit.disabled = True
        page.update()

    nom = ft.TextField(label="Nom", on_change=validate_input)
    prenom = ft.TextField(label="Prenom", on_change=validate_input)
    mail = ft.TextField(label="Mail", on_change=validate_input)
    submit = ft.ElevatedButton(text="Ajouter", on_click=lambda x: add_list_tile(x), disabled=True)

    def add_list_tile(e):
        page.close(dlg)
        page.add(
            ft.Container(
                content=ft.ListTile(
                    leading=ft.CircleAvatar(
                        content=ft.Text(nom.value[0].upper()),
                        bgcolor=ft.Colors.DEEP_ORANGE_300,
                        radius=20,
                    ),
                    title=ft.Text(f"{prenom.value} {nom.value}", size=18, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(mail.value, size=14, italic=True),
                    on_click=lambda x: print(f"{prenom.value} {nom.value} clicked!"),
                ),
                bgcolor=ft.Colors.TEAL_100,
                border_radius=12,
                padding=10,
                margin=5
            )
        )
        add_client(nom.value, prenom.value, mail.value)
        page.open(ft.SnackBar(ft.Text("Client ajouté !")))
    
    dlg = ft.AlertDialog(
        title=ft.Text("Ajouter un nouveau client :"),
        actions_overflow_button_spacing=10,
        actions=[
            nom,
            prenom,
            mail,
            submit
        ]
    ) 
    page.open(dlg)

def create_add_button(page: ft.Page):
    return ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        bgcolor=ft.Colors.LIME_300,
        on_click=lambda x: fab_pressed(page)
    )