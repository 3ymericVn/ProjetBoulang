import flet as ft 
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet import ControlEvent
import sqlite3

def main(page: ft.Page) -> None:
    with sqlite3.connect('oui.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test (
                oui TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO test (oui) VALUES ('oui zizi')
        ''')
        conn.commit()
    page.title = 'SignUp'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_with = 400
    page.window_height = 400
    page.windows_resizable = False
    
    text_username: TextField = TextField(label='username', text_align=ft.TextAlign.LEFT, width=200)
    text_password: TextField = TextField(label='password', text_align=ft.TextAlign.LEFT, width=200, password=True)
    checkbox_signup : Checkbox = Checkbox(label='Jaccpete connard', value=False)
    button_submit : ElevatedButton = ElevatedButton(text='Sign up', width=200,disabled=True)

    def validate(e: ControlEvent) -> None:
        if all([text_username.value , text_password.value, checkbox_signup.value]):
            button_submit.disabled = False
        else:
            button_submit.disabled = True
        page.update()

    def submit(e: ControlEvent) -> None:
        print('Username', text_username.value)
        print('Username', text_username.value)
        with sqlite3.connect('oui.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM test
            ''')
            text = [i for i in cursor.fetchall()]
            conn.commit()
        text = text[0][0]
        page.clean()
        page.add(
            Row(
                controls=[Text(value=f'Welcome : {text_username.value} {text}',size=20)],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
    checkbox_signup.on_change = validate
    text_username.on_change = validate
    text_password.on_change = validate
    button_submit.on_click = submit

    page.add(
        Row(
            controls=[
                Column(
                    [text_username,
                     text_password,
                     checkbox_signup,
                     button_submit]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


if __name__ == '__main__':
    ft.app(target=main)

