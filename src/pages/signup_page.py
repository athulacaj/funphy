import flet as ft
# import sys
# import os
from .utils import get_background_image, BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING
from .db import AppDatabase

# Find the root directory of the project and add it to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

def signup_page(page: ft.Page):
    # Create loading indicator
    progress_ring = ft.ProgressRing(width=16, height=16, stroke_width=2, color=ACCENT_COLOR, visible=False)
    
    # Create form fields
    name = ft.TextField(label="Name", color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
    email = ft.TextField(label="Email", color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
    confirm = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
      # Create error text
    error_text = ft.Text("", color=ft.Colors.RED_400, size=12, visible=False)
    
    
    async def submit_signup(e):
        # Show loading indicator
        progress_ring.visible = True
        error_text.visible = False
        page.update()
        
        # Basic validation
        if not name.value or not email.value or not password.value or not confirm.value:
            error_text.value = "Please fill in all fields"
            error_text.visible = True
            progress_ring.visible = False
            page.update()
            return
            
        if password.value != confirm.value:
            error_text.value = "Passwords do not match"
            error_text.visible = True
            progress_ring.visible = False
            page.update()
            return
        
        # Save user to database
        success, message = await AppDatabase.save_user(name.value, email.value, password.value)
        
        if success:
            page.snack_bar = ft.SnackBar(ft.Text("Account created successfully!"), bgcolor=ACCENT_COLOR)
            page.snack_bar.open = True
            page.go("/login")
        else:
            error_text.value = message
            error_text.visible = True
            
        progress_ring.visible = False
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
                            ft.Text("Sign Up", size=30, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
                            name,
                            email,
                            password,
                            confirm,
                            error_text,
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Sign Up", 
                                        on_click=submit_signup, 
                                        style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=TEXT_COLOR, padding=BUTTON_PADDING)
                                    ),
                                    progress_ring,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.TextButton("Login", on_click=lambda e: page.go("/login"), style=ft.ButtonStyle(color=ACCENT_COLOR, padding=BUTTON_PADDING)),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        expand=True,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20)
                ),
            ],expand=True)
        ],
        bgcolor=BG_COLOR,
        padding=0
    )
