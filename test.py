import flet as ft


def main(page: ft.Page):
    page.title = "Accueil"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0


    def fab_pressed(e):
        def validate_input(e):
            if all([nom.value, prenom.value, mail.value]):
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


    ajouter_btn = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        bgcolor=ft.Colors.LIME_300,
        on_click=fab_pressed,
        right=16,
        bottom=16
    )

    rechercher_btn = ft.FloatingActionButton(
        icon=ft.Icons.SEARCH,
        bgcolor=ft.Colors.BLUE_300,
        left=16,
        bottom=16
    )

    page.overlay.append(
        ft.Stack(
            controls=[ajouter_btn, rechercher_btn],
            expand=True
        )
    )

    page.add(
        ft.Container(
            ft.Row(
                [
                    ft.Text(
                        "Liste des clients",
                        style=ft.TextStyle(size=20, weight=ft.FontWeight.W_500),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLUE,
            padding=ft.padding.all(20),
        ),
    )


ft.app(main)