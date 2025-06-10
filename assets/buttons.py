import re
import flet as ft
from .client_card import create_client_card
from db import add_client

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
        if not add_client(nom.value, prenom.value, mail.value):
            return page.open(ft.SnackBar(ft.Text("Ce mail est déjà enregistré !")))
        page.add(
            create_client_card(nom.value, prenom.value, mail.value, page)
        )

        page.open(ft.SnackBar(ft.Text("Client ajouté !")))
        return None

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