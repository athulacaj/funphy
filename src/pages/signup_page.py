import flet as ft
from .utils import get_background_image, BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING

def signup_page(page: ft.Page):
    name = ft.TextField(label="Name", color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
    email = ft.TextField(label="Email", color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
    confirm = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
    
    def submit_signup(e):
        page.snack_bar = ft.SnackBar(ft.Text("Account created!"), bgcolor=ACCENT_COLOR)
        page.snack_bar.open = True
        page.go("/login")
        page.update()

    return ft.View(
        "/signup",
        [
            ft.Stack([
                # Background image container
                get_background_image(),
                # Content
                ft.Container(
                    ft.Column(
                        [
                            ft.Text("Create an Account", size=30, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
                            name,
                            email,
                            password,
                            confirm,
                            ft.ElevatedButton("Sign Up", on_click=submit_signup, style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=TEXT_COLOR, padding=BUTTON_PADDING)),
                            ft.TextButton("Back", on_click=lambda e: page.go("/welcome"), style=ft.ButtonStyle(color=ACCENT_COLOR, padding=BUTTON_PADDING)),
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
