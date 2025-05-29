import flet as ft
from .utils import get_background_image, BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING

def dashboard_page(page: ft.Page):
    # Check if user is logged in
    user = page.session.get("user")
    
    if not user:
        # If not logged in, redirect to login page
        page.go("/login")
        return
        
    # User information from session
    user_name = user.get("name", "User")
    user_email = user.get("email", "")
    assement_score = user.get("assessment_score", None)
    
    def logout(e):
        # Clear user data from session
        page.session.remove("user")
        
        # Show logout message
        page.snack_bar = ft.SnackBar(ft.Text("Logged out successfully"), bgcolor=ACCENT_COLOR)
        page.snack_bar.open = True
        
        # Redirect to welcome page
        page.go("/welcome")
        page.update()
    
    # Dashboard content
    return ft.View(
        "/dashboard",
        [
            ft.Stack([
                # Background image container
                get_background_image(),
                
                # Content
                ft.Container(
                    ft.Column(
                        [   
                            ft.Text(f"Welcome, {user_name}!", size=30, weight=ft.FontWeight.W_600, color=ACCENT_COLOR),
                            ft.Text(f"Email: {user_email}", size=16, color=TEXT_COLOR),
                            
                            ft.Container(height=20),  # Spacer
                            ft.Container(
                                ft.Column(
                                    [
                                        ft.Text("Dashboard", size=24, weight=ft.FontWeight.W_500, color=PRIMARY_COLOR),
                                        ft.Text("Your personal dashboard content will appear here.", size=14, color=TEXT_COLOR),
                                        
                                        ft.Container(height=20),  # Spacer
                                        
                                        ft.ElevatedButton(
                                            "Start Physics Assessment", 
                                            on_click=lambda e: page.go("/assessment/intro"),
                                            style=ft.ButtonStyle(
                                                bgcolor=ACCENT_COLOR, 
                                                color=BG_COLOR, 
                                                padding=BUTTON_PADDING
                                            )
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                padding=20,
                                border_radius=10,
                                bgcolor=ft.Colors.BLACK12,
                                width=400,
                            ),
                            
                            ft.Container(height=20),  # Spacer
                            
                            ft.ElevatedButton(
                                "Logout", 
                                on_click=logout, 
                                style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=TEXT_COLOR, padding=BUTTON_PADDING)
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
        ],
        bgcolor=BG_COLOR  
    )
