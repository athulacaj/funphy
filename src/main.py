import flet as ft
from pages import splash_page, welcome_page, login_page, signup_page, dashboard_page
from pages.utils import BG_COLOR

def main(page: ft.Page):
    page.title = "FunPhy - Fun with Physics"
    page.bgcolor = BG_COLOR
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

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

        page.update()

    page.on_route_change = route_change
    page.go(page.route or "/")


ft.app(main)
