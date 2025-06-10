import flet as ft

def create_client_card(nom: str, prenom: str, mail: str, page: ft.Page) -> ft.Container:
    cg = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value="add", label="Créditer"),
                ft.Radio(value="sub", label="Débiter"),
            ]
        )
    )
    number_input = ft.TextField(
        label="Montant",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    popup = ft.AlertDialog(
        action_button_padding=ft.padding.all(0),
        title=ft.Text("Créditer ou débiter ?"),
        content=ft.Column(
            [
                cg,
                number_input,
            ]
        ),
        actions=[
            ft.ElevatedButton(text="Créditer", on_click=lambda x: print("Créditer")),
        ]
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
            on_click=lambda x: page.open(popup),
        ),
        bgcolor=ft.Colors.TEAL_100,
        border_radius=12,
        padding=10,
        margin=5
    )