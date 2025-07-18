import re
import flet as ft
from .client_card import create_client_card
from .views import affichage_transac, affichage_clients, create_transaction_table
from db import add_client, get_transactions, get_client_solde

EMAIL_REGEX = r"^\S+@\S+\.\S+$"

def affichage_transac(page: ft.Page, lvc: ft.Container, lv: ft.ListView, boutton_li_transac: ft.FloatingActionButton):
    transacs = get_transactions()
    lv2 = ft.ListView(spacing=10)
    datatable = create_transaction_table(transacs, boutton_li_transac)
    lv2.controls.append(datatable)
    lvc.content = lv2
    page.add(lvc)
    boutton_li_transac.icon = ft.Icons.HOME_FILLED
    boutton_li_transac.on_click = lambda x : affichage_clients(lvc, lv, boutton_li_transac)
    page.update()

def affichage_clients(page: ft.Page, lvc: ft.Container, lv: ft.ListView, boutton_li_transac: ft.FloatingActionButton):
    lvc.content = lv
    boutton_li_transac.icon = ft.Icons.ASSESSMENT_OUTLINED
    boutton_li_transac.on_click = lambda x : affichage_transac(page, lvc, lv, boutton_li_transac)
    page.update()

async def fab_pressed(page: ft.Page, lv: ft.ListView, lvc: ft.Container, home_button: ft.FloatingActionButton):
    def validate_input(e):
        if all([nom.value, prenom.value, mail.value]) and re.match(EMAIL_REGEX, mail.value):
            submit.disabled = False
        else:
            submit.disabled = True
        page.update()

    async def add_list_tile(e):
        page.close(dlg)
        if not await add_client(nom.value, prenom.value, mail.value):
            return page.open(ft.SnackBar(ft.Text("Ce mail est déjà enregistré !")))
        
        lv.controls.append(
            create_client_card(nom.value, prenom.value, mail.value, 0.0, page, lv, lvc, home_button)
        )
        page.update()

        page.open(ft.SnackBar(ft.Text("Client ajouté !")))
        return None

    nom = ft.TextField(label="Nom", on_change=validate_input)
    prenom = ft.TextField(label="Prenom", on_change=validate_input)
    mail = ft.TextField(label="Mail", on_change=validate_input)
    submit = ft.ElevatedButton(text="Ajouter", on_click=add_list_tile, disabled=True)

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

async def create_add_button(page: ft.Page, lv: ft.ListView, lvc: ft.Container, boutton_li_transac: ft.FloatingActionButton):
    async def on_click(x):
        await fab_pressed(page, lv, lvc, boutton_li_transac)
    return ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        bgcolor=ft.Colors.LIME_300,
        on_click=on_click,
    )

def create_list_transac(page: ft.Page, lvc: ft.Container, lv: ft.ListView, boutton_li_transac: ft.FloatingActionButton) -> ft.FloatingActionButton:
    async def on_click(x):
        await affichage_transac(page, lvc, lv, boutton_li_transac)
    return ft.FloatingActionButton(
        icon=ft.Icons.ASSESSMENT_OUTLINED, on_click=on_click, bgcolor=ft.Colors.LIME_300
    )