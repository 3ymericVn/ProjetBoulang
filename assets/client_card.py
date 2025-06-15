import re
import flet as ft
from db import operate_solde, delete_client, edit_client, get_client_solde, get_transactions_by_mail
EMAIL_REGEX = r"^\S+@\S+\.\S+$"

def create_client_card(nom: str, prenom: str, mail: str, page: ft.Page, lv: ft.ListView) -> ft.Container:
    def on_click(e, radio_value, number_value):
        if operate_solde(mail, number_value, radio_value):
            page.close(popup)
            solde_text.value = f"{get_client_solde(mail):.2f}€"
            page.open(ft.SnackBar(ft.Text(f"Le solde de {nom} {prenom} a été modifié.")))
            page.update()
        else:
            page.open(ft.SnackBar(ft.Text("Solde insuffisant !")))

    radio = ft.RadioGroup(
        value="sub", 
        content=ft.Column([
            ft.Radio(value="sub", label="Débiter", width=100, height=50, label_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)),
            ft.Radio(value="add", label="Créditer", width=100, height=50, label_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)),
        ])
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
    
    def on_delete_client(e):
        page.open(ft.SnackBar(
            ft.Text(f"Le client {nom} {prenom} a été supprimé." if delete_client(mail) else f"Erreur lors de la suppression du client {nom} {prenom}.")
        ))
        for i, c in enumerate(lv.controls):
            l: ft.ListTile = c.content
            if l.subtitle.value == mail:
                lv.controls.pop(i)
                page.update()
                break

    def on_edit_client(e, e_nom: str, e_prenom: str, e_mail: str):
        original_mail = e_mail
        def validate_input(e):
            if all([t_nom.value, t_prenom.value, t_mail.value]) and re.match(EMAIL_REGEX, t_mail.value):
                submit.disabled = False
            else:
                submit.disabled = True
            page.update()

        def on_edit_client_submit(e):
            nonlocal nom, prenom, mail
            for c in lv.controls:
                l: ft.ListTile = c.content
                if l.subtitle.value == original_mail:
                    l.title.value = f"{t_nom.value} {t_prenom.value}"
                    l.subtitle.value = t_mail.value
                    page.update()
                    break
            else:
                page.open(ft.SnackBar(ft.Text("Erreur lors de la modification du client !")))

            page.close(dlg)

            if edit_client(t_mail.value, t_nom.value, t_prenom.value):
                nom, prenom, mail = t_nom.value, t_prenom.value, t_mail.value
                page.open(ft.SnackBar(ft.Text("Client modifié !")))
            else:
                page.open(ft.SnackBar(ft.Text("Erreur lors de la modification du client !")))
        
        t_nom = ft.TextField(label="Nom", value=e_nom, on_change=validate_input)
        t_prenom = ft.TextField(label="Prenom", value=e_prenom, on_change=validate_input)
        t_mail = ft.TextField(label="Mail", value=e_mail, on_change=validate_input)
        submit = ft.ElevatedButton(text="Modifier", on_click=on_edit_client_submit, disabled=True)

        # Valider les champs initialement
        validate_input(None)

        dlg = ft.AlertDialog(
            title=ft.Text("Modifier le client :"),
            actions_overflow_button_spacing=10,
            actions=[
                t_nom,
                t_prenom,
                t_mail,
                submit
            ]
        )
        page.open(dlg)

    solde_text = ft.Text(f"{get_client_solde(mail):.2f}€", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)

    def reset_value(e):
        radio.value = "sub"      
        number_input.value = ""     
        page.open(popup)

    def affichage_transac_client(mail,page):

        transac_cli = get_transactions_by_mail(mail)
        lv3 = ft.ListView(spacing=10)
        lvc = ft.Container(
            content=lv3,
            expand=True,
        )
        datatable = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Montant")),
                ft.DataColumn(ft.Text("Opération")),
            ],
            rows=[]
        )
        for i in range(len(transac_cli)-1,-1,-1):
            transac = transac_cli[i]
            datatable.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(transac['date'])),
                        ft.DataCell(ft.Text(f"{transac['nom']} {transac['prenom']}")),
                        ft.DataCell(ft.Text(transac['mail'])),
                        ft.DataCell(ft.Text(("+" if transac['operation'] == 'add' else "-") + str(transac['montant']))),
                    ]
                )
            )
        lv3.controls.append(datatable)
        lvc.content = lv3
        lvc.update()
        # boutton_li_transac.icon = ft.Icons.HOME_FILLED
        # boutton_li_transac.on_click = lambda x : affichage_clients(lvc, lv, boutton_li_transac)
        page.update()
       

    return ft.Container(
        content=ft.ListTile(
            leading_and_trailing_text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            leading=solde_text,
            title=ft.Text(f"{nom} {prenom}", size=18, weight=ft.FontWeight.BOLD),
            subtitle=ft.Text(f"{mail}", size=14, italic=True),
            trailing=ft.Column(
                [
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Supprimer le client", on_click=on_delete_client),
                            ft.PopupMenuItem(text="Modifier le client", on_click=lambda x: on_edit_client(x, nom, prenom, mail)),
                            ft.PopupMenuItem(text="Liste des transactions du client", on_click=lambda x: affichage_transac_client(mail,page))
                        ],
                        expand=True,
                    )
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.END,
            ),
            on_click=reset_value, 
        ),
        bgcolor=ft.Colors.TEAL_100,
        border_radius=12,
        padding=10,
        margin=5
    )