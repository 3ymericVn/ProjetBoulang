import asyncio
import flet as ft

async def main(page: ft.Page):
    page.title = "Test"
    page.add(await create_client_card(page))
    page.update()

async def create_client_card(page: ft.Page):
    async def on_click(e, oui: str):
        print(oui)
    async def on_click2(e):
        await on_click(e, "oui")
    return ft.Container(
        content=ft.Text("Client"),
        bgcolor=ft.Colors.TEAL_100,
        border_radius=12,
        padding=10,
        on_click=on_click2,
    )
    
asyncio.run(ft.app_async(target=main))