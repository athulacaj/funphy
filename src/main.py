import flet as ft
from pages import splash_page, welcome_page, login_page, signup_page, dashboard_page,get_assessment_pages
from pages.utils import BG_COLOR, ACCENT_COLOR
from pages.db import AppDatabase
from pages.path_game import path_game 
from pages.emoji_game import build_emoj_game 


async def main(page: ft.Page):
    page.title = "FunPhy - Fun with Physics"
    page.bgcolor = BG_COLOR
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Set Snackbar theme to BG_COLOR with opacity
    page.theme = ft.Theme(
        snackbar_theme=ft.SnackBarTheme(
            bgcolor=ft.Colors.with_opacity(0.95, ACCENT_COLOR)
        )
    )

    # page.route="/signup"

    def route_change(route):
        page.views.clear()

        if page.route == "/":
            # Splash Screen
            page.views.append(splash_page(page))
        elif page.route == "/welcome":
            # Welcome Screen
            page.views.append(welcome_page(page))        
        elif page.route == "/login":
            # Login Screen
            page.views.append(login_page(page))
        elif page.route == "/signup":
            # Signup Screen
            page.views.append(signup_page(page))
        elif page.route == "/dashboard":
            # Dashboard Screen
            page.views.append(dashboard_page(page))
        elif page.route.startswith("/assessment/"):
            assessment_view = get_assessment_pages(page)
            if assessment_view:
                page.views.append(assessment_view)
        # Add path game route
        elif page.route == "/path_game":
            page.views.append(path_game(page))
        elif page.route == "/emoji_game":
            page.views.append(build_emoj_game(page))
        
        page.update()

    await AppDatabase.initialize()  # Ensure database is initialized before any page loads
    self_user = await AppDatabase.get_self_user()  # Get the currently logged-in user
    if self_user  is not None:
        # If user is already logged in, redirect to dashboard
        page.route = "/dashboard"
        page.session.set("user", self_user) # Store user data in session
        
    page.on_route_change = route_change
    page.go(page.route or "/")


ft.app(main)
