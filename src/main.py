import flet as ft
from pages import splash_page, welcome_page, login_page, signup_page, dashboard_page,settings_page,get_assessment_pages
from pages.learning_module_pages import learning_modules_view, modules_details_view,lessons_view,notes_page,references_page,videos_view # Added import
from pages.utils import BG_COLOR, SNACK_COLOR
from pages.db import AppDatabase
from pages.path_game import path_game 
from pages.emoji_game import build_emoj_game 
from pages.word_puzzle_page import word_puzzle_page


async def main(page: ft.Page):
    page.title = "FunPhy - Fun with Physics"
    page.bgcolor = BG_COLOR
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Set Snackbar theme to BG_COLOR with opacity
    page.theme = ft.Theme(
        snackbar_theme=ft.SnackBarTheme(
            bgcolor=ft.Colors.with_opacity(1, SNACK_COLOR)
        )
    )

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
        elif page.route == "/settings":
            page.views.append(settings_page(page))
        elif page.route.startswith("/assessment/"):
            assessment_view = get_assessment_pages(page)
            if assessment_view:
                page.views.append(assessment_view)
        # Add path game route
        elif page.route == "/path_game":
            page.views.append(path_game(page))
        elif page.route == "/emoji_game":
            page.views.append(build_emoj_game(page))
        elif page.route == "/word_puzzle":
            page.views.append(word_puzzle_page(page))
        elif page.route == "/learning_modules": # Added route
            page.views.append(learning_modules_view(page))
        elif page.route == "/modules_details": # Added route
            page.views.append(modules_details_view(page))
        elif page.route == "/lessons": # Added route
            page.views.append(lessons_view(page))
        elif page.route == "/notes": # Added route
            page.views.append(notes_page(page))
        elif page.route == "/references": # Added route
            page.views.append(references_page(page))
        elif page.route == "/videos": # Added route
            page.views.append(videos_view(page))
        page.update()

    await AppDatabase.initialize()  # Ensure database is initialized before any page loads
    self_user = await AppDatabase.get_self_user()  # Get the currently logged-in user
    # self_user=None
    if self_user  is not None:
        # If user is already logged in, redirect to dashboard
        page.route = "/dashboard"

        page.session.set("user", self_user) # Store user data in session
        
    page.on_route_change = route_change
    page.session.set("play_sound", True)  # Store user data in session
    page.go(page.route or "/")


ft.app(main)
# ft.app(target=main, port=8550)
