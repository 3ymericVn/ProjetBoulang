import re
import flet as ft
from db import operate_solde, delete_client, edit_client, get_client_solde, get_transactions_by_mail
from .views import affichage_clients, create_transaction_table
EMAIL_REGEX = r"^\S+@\S+\.\S+$"

def create_transaction_table(transac_cli: list[dict], home_button: ft.FloatingActionButton) -> ft.DataTable:
    datatable = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Client")),
            ft.DataColumn(ft.Text("Mail")),
            ft.DataColumn(ft.Text("Montant")),
        ],
        rows=[]
    )

    if len(transac_cli) == 0:
        datatable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Aucune transaction trouvée")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ]
            )
        )
        return datatable

    for transac in transac_cli:
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
    return datatable

async def create_client_card(nom: str, prenom: str, mail: str, page: ft.Page, lv: ft.ListView, lvc: ft.Container, home_button: ft.FloatingActionButton) -> ft.Container:
    async def on_click(e):
        await valider_click(e, radio.value, number_input.value)
    
    async def valider_click(e, radio_value, number_value):
        print(radio_value, number_value)
        if await operate_solde(mail, number_value, radio_value):
            page.close(popup)
            solde_text.value = f"{await get_client_solde(mail):.2f}€"
            page.open(ft.SnackBar(ft.Text(f"Le solde de {nom} {prenom} a été modifié.")))
            page.update()
        else:
            page.open(ft.SnackBar(ft.Text("Solde insuffisant !")))

    show_quick_amounts = False

    def on_radio_change(_):
        nonlocal show_quick_amounts
        show_quick_amounts = radio.value == "add"
        quick_amounts_container.visible = show_quick_amounts
        page.update()

    radio = ft.RadioGroup(
        value="sub",
        on_change=on_radio_change,
        content=ft.Row(
            [
                ft.Radio(
                    value="sub",
                    label="Débiter",
                    width=120,
                    height=50,
                    label_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                ),
                ft.Radio(
                    value="add",
                    label="Créditer",
                    width=120,
                    height=50,
                    label_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30,
        ),
    )

    number_input = ft.TextField(
        label="Montant personnalisé",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=8,
        border_color=ft.Colors.BLUE_200,
        bgcolor=ft.Colors.BLUE_50,
        text_style=ft.TextStyle(size=18),
        width=220,
        prefix_icon=ft.Icons.EURO_SYMBOL,
        visible=True,
    )

    radio2 = ft.RadioGroup(
        value="sub",
        content=ft.Row(
            [
                ft.Radio(
                    value="vingt",
                    label="20€ + 1€",
                    width=120,
                    height=50,
                    label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_900),
                ),
                ft.Radio(
                    value="cinquante",
                    label="50€ + 4€",
                    width=120,
                    height=50,
                    label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_900),
                ),
                ft.Radio(
                    value="cent",
                    label="100€ + 10€",
                    width=130,
                    height=50,
                    label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_900),
                ),
                ft.Radio(
                    value="cent_trente",
                    label="130€ + 15€",
                    width=130,
                    height=50,
                    label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_900),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
    )

    quick_amounts_container = ft.Column(
        [
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            ft.Text("Ou choisissez un montant rapide :", size=16, color=ft.Colors.GREY_700),
            radio2,
        ],
        visible=show_quick_amounts,
    )

    popup = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=12),
        content=ft.Column(
            [
                radio,
                ft.Row(
                    [number_input],
                    alignment=ft.MainAxisAlignment.CENTER, 
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                quick_amounts_container,
            ],
            width=600,
            height=320,
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER, 
        ),
        actions=[
            ft.FilledButton(
                text="Valider",
                on_click=on_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.Padding(16, 10, 16, 10),
                    text_style=ft.TextStyle(size=22, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.GREEN_400,
                    color=ft.Colors.WHITE,
                ),
                icon=ft.Icons.CHECK_CIRCLE_OUTLINED,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        inset_padding=ft.padding.only(top=24, bottom=24, left=24, right=24),
        bgcolor=ft.Colors.WHITE,
        elevation=8,
    )


    def delete_client_confirm(mail):
        async def delete_client2_click(e):
            await delete_client2(mail)
            page.close(dlg)

        dlg = ft.AlertDialog(
            title=ft.Text("Supprimer le client :"),
            content=ft.Text(f"Êtes-vous sûr de vouloir supprimer le client {nom} {prenom} ?"),
            actions=[
                ft.TextButton(text="Annuler", on_click=lambda x: page.close(dlg)),
                ft.TextButton(text="Supprimer", on_click=delete_client2_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg)


    async def delete_client2(mail):
        solde = await get_client_solde(mail)
        if solde > 0:
            page.open(ft.SnackBar(
                ft.Text(f"Le client {nom} {prenom} a un solde positif de {solde:.2f}€. Veuillez le débiter avant de le supprimer.")
            ))
            return
        else:
            page.open(ft.SnackBar(
                ft.Text(f"Le client {nom} {prenom} a été supprimé.")
            ))
            await delete_client(mail)
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

        async def on_edit_client_submit(e):
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

            if await edit_client(t_mail.value, t_nom.value, t_prenom.value):
                nom, prenom, mail = t_nom.value, t_prenom.value, t_mail.value
                page.open(ft.SnackBar(ft.Text("Client modifié !")))
            else:
                page.open(ft.SnackBar(ft.Text("Erreur lors de la modification du client !")))
        
        t_nom = ft.TextField(label="Nom", value=e_nom, on_change=validate_input)
        t_prenom = ft.TextField(label="Prenom", value=e_prenom, on_change=validate_input)
        t_mail = ft.TextField(label="Mail", value=e_mail, on_change=validate_input)
        submit = ft.ElevatedButton(text="Modifier", on_click=on_edit_client_submit, disabled=True)

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

    solde_text = ft.Text(f"{await get_client_solde(mail):.2f}€", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)

    def reset_value(e):
        radio.value = "sub"      
        number_input.value = ""     
        page.open(popup)

    async def affichage_transac_client(mail, lvc: ft.Container, home_button: ft.FloatingActionButton):
        transac_cli = await get_transactions_by_mail(mail)
        lv3 = ft.ListView(spacing=10)
        datatable = create_transaction_table(transac_cli, home_button)
        lv3.controls.append(datatable)
        lvc.content = lv3
        home_button.icon = ft.Icons.HOME_FILLED
        home_button.on_click = lambda x : affichage_clients(page, lvc, lv, home_button)
        page.update()

    async def affichage_transac_client_click(x):
        await affichage_transac_client(mail, lvc, home_button)

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
                            ft.PopupMenuItem(text="Supprimer le client", on_click=lambda x: delete_client_confirm(mail)),
                            ft.PopupMenuItem(text="Modifier le client", on_click=lambda x: on_edit_client(x, nom, prenom, mail)),
                            ft.PopupMenuItem(text="Liste des transactions du client", on_click=affichage_transac_client_click)
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