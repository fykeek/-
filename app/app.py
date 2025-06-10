import flet as ft


async def main(page: ft.Page) -> None:
    page.title = "FyKeek combat"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = '#141221'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {""}


if __name__ == "__main__":
    ft.app(target=main,view=ft.WEB_BROWSER)