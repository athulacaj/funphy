import flet as ft
# import sys
# import os
from .utils import get_background_image, BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING

# Find the root directory of the project and add it to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from .db import AppDatabase

def get_view(page: ft.Page):
    # Create loading indicator
    progress_ring = ft.ProgressRing(width=16, height=16, stroke_width=2, color=ACCENT_COLOR, visible=False)
    
    
    # Create form fields
    email = ft.TextField(label="Email", color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
    # Create error text
    error_text = ft.Text("", color=ft.Colors.RED_400, size=12, visible=False)    # Create retry button (initially hidden)
    retry_button = ft.OutlinedButton(
        "Retry Connection", 
        icon=ft.Icons.REFRESH,
        visible=False,
        on_click=lambda e: submit_login(e),
        style=ft.ButtonStyle(color=ACCENT_COLOR)    )
    
    
    async def submit_login(e):
        # Show loading indicator
        progress_ring.visible = True
        error_text.visible = False
        retry_button.visible = False
        page.update()
        
        # Basic validation
        if not email.value or not password.value:
            error_text.value = "Please enter both email and password"
            error_text.visible = True
            progress_ring.visible = False
            page.update()
            return
        
        try:
            # Initialize the database before attempting authentication

            # Authenticate user with a timeout handling
            success, result = await AppDatabase.authenticate_user(email.value, password.value)
            
            if success:
                # Store user data in session
                page.session.set("user", result)
                
                page.snack_bar = ft.SnackBar(ft.Text("Login successful!"), bgcolor=ACCENT_COLOR)
                page.snack_bar.open = True
                if(result.get("assessment_score") is None):
                    page.go("/assessment/intro")
                else:
                    page.go("/dashboard")  # Navigate to dashboard
            else:
                if "Timeout" in str(result):
                    error_text.value = "Connection timeout. Please check your network and try again."
                    retry_button.visible = True
                else:
                    error_text.value = result if isinstance(result, str) else "Invalid credentials"
                    retry_button.visible = False
                error_text.visible = True
                
        except Exception as e:
            error_text.value = f"Login error: {str(e)}"
            if "Timeout" in str(e):
                error_text.value = "Connection timeout. Please check your network and try again."
                retry_button.visible = True
            else:
                retry_button.visible = False
            error_text.visible = True
            
        progress_ring.visible = False
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
                                    email,
                                    password,
                                    error_text,
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Log In", 
                                                on_click=submit_login, 
                                                style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=TEXT_COLOR, padding=BUTTON_PADDING)
                                            ),
                                            progress_ring,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    retry_button,
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
                ),
            ],expand=True)
        ],
        bgcolor=BG_COLOR  
    )
