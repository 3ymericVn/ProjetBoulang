import flet as ft


def main(page: ft.Page):
    page.title = "Floating Action Button"
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
                ft.ListTile(
                    title=ft.Text(f"{nom.value} {prenom.value} {mail.value}"),
                    bgcolor=ft.Colors.TEAL_300,
                    leading=ft.Icon(
                        ft.Icons.CIRCLE_OUTLINED, color=ft.Colors.DEEP_ORANGE_300
                    ),
                    on_click=lambda x: print(x.control.title.value + " was clicked!"),
                )
            )
            page.open(ft.SnackBar(ft.Text("Tile was added successfully!")))
        

        dlg = ft.AlertDialog(
            title=ft.Text("Tile was added successfully!"),
            content=ft.Text("Tile was added successfully!"),
            actions_overflow_button_spacing=10,
            actions=[
                nom,
                prenom,
                mail,
                submit
            ]
        ) 
        page.open(dlg)


    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=fab_pressed, bgcolor=ft.Colors.LIME_300
    )
    page.add(
        ft.Container(
            ft.Row(
                [
                    ft.Text(
                        "Floating Action Button Example",
                        style=ft.TextStyle(size=20, weight=ft.FontWeight.W_500),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLUE,
            padding=ft.padding.all(20),
        ),
        ft.Text("Press the FAB to add a tile!"),
    )


ft.app(main)