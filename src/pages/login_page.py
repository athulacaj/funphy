import flet as ft
from .utils import get_background_image, BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING

def get_view(page: ft.Page):
    username = ft.TextField(label="Username", color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
    
    def submit_login(e):
        page.snack_bar = ft.SnackBar(ft.Text("Logged in!"), bgcolor=ACCENT_COLOR)
        page.snack_bar.open = True
        page.go("/")
        page.update()

    return ft.View(
        "/login",
        [
            ft.Stack([
                # Background image container
                get_background_image(),
                ft.Column(
                    [
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text("Welcome back!", size=30, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
                                    username,
                                    password,
                                    ft.ElevatedButton("Log In", on_click=submit_login, style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=TEXT_COLOR, padding=BUTTON_PADDING)),
                                    ft.TextButton("Back", on_click=lambda e: page.go("/welcome"), style=ft.ButtonStyle(color=ACCENT_COLOR, padding=BUTTON_PADDING)),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                                expand=True,
                            ),
                            expand=True,
                            alignment=ft.alignment.center,
                            height=300,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    height=page.window.height if page.window else 600,
                ),
            ])
        ]
    )
