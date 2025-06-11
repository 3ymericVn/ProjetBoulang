import flet as ft
from db import operate_solde, delete_client

def on_delete_client(page: ft.Page, nom: str, prenom: str, mail: str):
    if delete_client(mail):
        page.snack_bar = ft.SnackBar(ft.Text(f"Le client {nom} {prenom} a été supprimé."))
        page.update()
    else:
        page.snack_bar = ft.SnackBar(ft.Text(f"Erreur lors de la suppression du client {nom} {prenom}."))
        page.update()


def create_client_card(nom: str, prenom: str, mail: str, page: ft.Page) -> ft.Container:
    def on_click(e, radio_value, number_value):
        if operate_solde(mail, number_value, radio_value):
            page.close(popup)
            page.open(ft.SnackBar(ft.Text(f"Le solde de {nom} {prenom} a été modifié.")))
            page.update()
        else:
            page.open(ft.SnackBar(ft.Text("Solde insuffisant !")))

    radio = ft.RadioGroup(
        value="sub",
        content=ft.Column(
            [
                ft.Radio(value="sub", label="Débiter", width=100, height=50, label_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)),
                ft.Radio(value="add", label="Créditer", width=100, height=50, label_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)),
            ]
        )
    )
    number_input = ft.TextField(
        label="Montant",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    popup = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("Créditer ou débiter ?"),
        content=ft.Column(
            [
                radio,
                number_input,
            ],
            width=400,
            height=200,
            spacing=20,
        ),
        actions=[
            ft.FilledButton(
                text="Valider", 
                on_click=lambda x: on_click(x, radio.value, number_input.value), 
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=5),
                    padding=ft.Padding(10, 10, 10, 10),
                    text_style=ft.TextStyle(size=30, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.GREEN_300,
                    color=ft.Colors.BLACK,
                )
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        inset_padding=ft.padding.only(top=20, bottom=20, left=20, right=20)
    )
    
    return ft.Container(
        content=ft.ListTile(
            leading=ft.CircleAvatar(
                content=ft.Text(nom[0].upper()),
                bgcolor=ft.Colors.DEEP_ORANGE_300,
                radius=20,
            ),
            title=ft.Text(f"{nom} {prenom}", size=18, weight=ft.FontWeight.BOLD),
            subtitle=ft.Text(mail, size=14, italic=True),
            trailing=ft.Column(
                [
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Supprimer le client", on_click=on_delete_client(page, nom, prenom, mail)),
                            ft.PopupMenuItem(text="Liste des transactions du client"),
                            ft.PopupMenuItem(text="Modifier le client")
                        ]
                    )
                ]
            ),
            on_click=lambda x: page.open(popup),
        ),
        bgcolor=ft.Colors.TEAL_100,
        border_radius=12,
        padding=10,
        margin=5
    )