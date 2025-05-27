import flet as ft
from .utils import get_background_image, BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING

def get_view(page: ft.Page):
    return ft.View(
        "/welcome",
        [
            ft.Stack([
                # Background image container
                get_background_image(),
                # Content
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Hello!", size=40, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
                            ft.Text("Let's start your epic journey.", size=20, color=TEXT_COLOR),
                            ft.Row(
                                [
                                    ft.ElevatedButton("Log In", on_click=lambda e: page.go("/login"), style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=TEXT_COLOR, padding=BUTTON_PADDING)),
                                    ft.ElevatedButton("Sign Up", on_click=lambda e: page.go("/signup"), style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=TEXT_COLOR, padding=BUTTON_PADDING)),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        expand=True,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                    height=page.window.height if page.window else 600,
                ),
            ])
        ]
    )
