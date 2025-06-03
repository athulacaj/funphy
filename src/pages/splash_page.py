import flet as ft
from .utils import get_background_image, BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING

def get_view(page: ft.Page):
    return ft.View(
        "/",
        [
            ft.Stack([
                # Background image container
                get_background_image(),
                # Content
                ft.Container(
                    ft.Column(
                        [
                            ft.Container(
                                ft.Icon(ft.Icons.VIDEOGAME_ASSET, size=100, color=ACCENT_COLOR),
                                width=140, height=140,
                                bgcolor=PRIMARY_COLOR,
                                border_radius=70,
                            ),
                            ft.Text("FunPhy", size=30, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    "Get Started", 
                                    on_click=lambda e: page.go("/welcome"), 
                                    style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=TEXT_COLOR, padding=BUTTON_PADDING),
                                    width=200,
                                ),
                                alignment=ft.alignment.center,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    expand=True,
                    alignment=ft.alignment.center
                ),
            ],expand=True,)
        ],
        # bgcolor=BG_COLOR  # Added background color
    )
