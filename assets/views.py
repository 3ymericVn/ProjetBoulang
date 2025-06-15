import flet as ft
from db import get_transactions

def create_transaction_table(transac_cli: list[dict]) -> ft.DataTable:
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
    return datatable

def affichage_transac(page: ft.Page, lvc: ft.Container, lv: ft.ListView, boutton_li_transac: ft.FloatingActionButton):
    transacs = get_transactions()
    lv2 = ft.ListView(spacing=10)
    datatable = create_transaction_table(transacs)
    lv2.controls.append(datatable)
    lvc.content = lv2
    page.add(lvc)
    boutton_li_transac.icon = ft.Icons.HOME_FILLED
    boutton_li_transac.on_click = lambda x : affichage_clients(page, lvc, lv, boutton_li_transac)
    page.update()

def affichage_clients(page: ft.Page, lvc: ft.Container, lv: ft.ListView, boutton_li_transac: ft.FloatingActionButton):
    lvc.content = lv
    boutton_li_transac.icon = ft.Icons.ASSESSMENT_OUTLINED
    boutton_li_transac.on_click = lambda x : affichage_transac(page, lvc, lv, boutton_li_transac)
    page.update() 