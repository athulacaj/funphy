import flet as ft

def main(page: ft.Page):
    page.title = "Physics Journey"
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400  # Set a reasonable width for a mobile-like app
    page.window_height = 700 # Set a reasonable height
    page.window_resizable = False # Prevent resizing for a consistent look

    # Define a common theme for the app
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.GREEN_700,
        use_material3=True,
        # You can further customize typography, shapes, etc. here
    )

    # Green gradient background
    page.bgcolor = ft.colors.TRANSPARENT # Make page background transparent to show gradient
    page.add(
        ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.GREEN_800, ft.colors.GREEN_400, ft.colors.WHITE],
                stops=[0.0, 0.5, 1.0]
            ),
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Hello!", size=48, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                ft.Text("Let's start your Physics Journey", size=20, color=ft.colors.WHITE70),
                                ft.Divider(height=40, color=ft.colors.TRANSPARENT), # Spacer
                                ft.ElevatedButton(
                                    content=ft.Text("Log In", size=18, weight=ft.FontWeight.BOLD),
                                    on_click=lambda e: page.go("/login"),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        padding=ft.padding.symmetric(vertical=15, horizontal=40),
                                        bgcolor=ft.colors.WHITE,
                                        color=ft.colors.GREEN_700,
                                        elevation=5
                                    )
                                ),
                                ft.Divider(height=20, color=ft.colors.TRANSPARENT), # Spacer
                                ft.OutlinedButton(
                                    content=ft.Text("Sign Up", size=18, weight=ft.FontWeight.BOLD),
                                    on_click=lambda e: page.go("/signup"),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        padding=ft.padding.symmetric(vertical=15, horizontal=40),
                                        side=ft.BorderSide(2, ft.colors.WHITE),
                                        color=ft.colors.WHITE,
                                        elevation=0
                                    )
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15
                        ),
                        alignment=ft.alignment.center,
                        expand=True
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        )
    )

    # Login Screen
    login_view = ft.View(
        "/login",
        [
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.colors.GREEN_800, ft.colors.GREEN_400, ft.colors.WHITE],
                    stops=[0.0, 0.5, 1.0]
                ),
                content=ft.Column(
                    [
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            icon_color=ft.colors.WHITE,
                            on_click=lambda e: page.go("/"),
                            tooltip="Go back"
                        ),
                        ft.Text("Welcome back! User", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.TextField(
                                        label="Username",
                                        border_radius=ft.border_radius.all(10),
                                        filled=True,
                                        bgcolor=ft.colors.WHITE,
                                        color=ft.colors.BLACK,
                                        label_style=ft.TextStyle(color=ft.colors.GREY_600),
                                        border_color=ft.colors.TRANSPARENT,
                                    ),
                                    ft.TextField(
                                        label="Password",
                                        password=True,
                                        can_reveal_password=True,
                                        border_radius=ft.border_radius.all(10),
                                        filled=True,
                                        bgcolor=ft.colors.WHITE,
                                        color=ft.colors.BLACK,
                                        label_style=ft.TextStyle(color=ft.colors.GREY_600),
                                        border_color=ft.colors.TRANSPARENT,
                                    ),
                                    ft.TextButton(
                                        "Forgot Password?",
                                        on_click=lambda e: print("Forgot Password clicked"),
                                        style=ft.ButtonStyle(color=ft.colors.WHITE70)
                                    ),
                                    ft.ElevatedButton(
                                        content=ft.Text("Log In", size=18, weight=ft.FontWeight.BOLD),
                                        on_click=lambda e: print("Login button clicked"),
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(vertical=15, horizontal=40),
                                            bgcolor=ft.colors.GREEN_700,
                                            color=ft.colors.WHITE,
                                            elevation=5
                                        )
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15
                            ),
                            padding=ft.padding.all(20),
                            border_radius=ft.border_radius.all(15),
                            bgcolor=ft.colors.BLACK26, # Semi-transparent background for the form
                            width=300
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.START, # Align content to start to make space for back button
                    spacing=20,
                    padding=ft.padding.only(top=20) # Add padding for the back button
                ),
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        padding=0 # Remove default padding for full gradient coverage
    )

    # Sign Up Screen
    signup_view = ft.View(
        "/signup",
        [
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.colors.GREEN_800, ft.colors.GREEN_400, ft.colors.WHITE],
                    stops=[0.0, 0.5, 1.0]
                ),
                content=ft.Column(
                    [
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            icon_color=ft.colors.WHITE,
                            on_click=lambda e: page.go("/"),
                            tooltip="Go back"
                        ),
                        ft.Text("Create an Account", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.TextField(
                                        label="Email",
                                        border_radius=ft.border_radius.all(10),
                                        filled=True,
                                        bgcolor=ft.colors.WHITE,
                                        color=ft.colors.BLACK,
                                        label_style=ft.TextStyle(color=ft.colors.GREY_600),
                                        border_color=ft.colors.TRANSPARENT,
                                    ),
                                    ft.TextField(
                                        label="Username",
                                        border_radius=ft.border_radius.all(10),
                                        filled=True,
                                        bgcolor=ft.colors.WHITE,
                                        color=ft.colors.BLACK,
                                        label_style=ft.TextStyle(color=ft.colors.GREY_600),
                                        border_color=ft.colors.TRANSPARENT,
                                    ),
                                    ft.TextField(
                                        label="Password",
                                        password=True,
                                        can_reveal_password=True,
                                        border_radius=ft.border_radius.all(10),
                                        filled=True,
                                        bgcolor=ft.colors.WHITE,
                                        color=ft.colors.BLACK,
                                        label_style=ft.TextStyle(color=ft.colors.GREY_600),
                                        border_color=ft.colors.TRANSPARENT,
                                    ),
                                    ft.TextField(
                                        label="Re-enter Password",
                                        password=True,
                                        can_reveal_password=True,
                                        border_radius=ft.border_radius.all(10),
                                        filled=True,
                                        bgcolor=ft.colors.WHITE,
                                        color=ft.colors.BLACK,
                                        label_style=ft.TextStyle(color=ft.colors.GREY_600),
                                        border_color=ft.colors.TRANSPARENT,
                                    ),
                                    ft.ElevatedButton(
                                        content=ft.Text("Sign Up", size=18, weight=ft.FontWeight.BOLD),
                                        on_click=lambda e: print("Sign Up button clicked"),
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(vertical=15, horizontal=40),
                                            bgcolor=ft.colors.GREEN_700,
                                            color=ft.colors.WHITE,
                                            elevation=5
                                        )
                                    ),
                                    ft.TextButton(
                                        "Already have an account? Sign In",
                                        on_click=lambda e: page.go("/login"),
                                        style=ft.ButtonStyle(color=ft.colors.WHITE70)
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15
                            ),
                            padding=ft.padding.all(20),
                            border_radius=ft.border_radius.all(15),
                            bgcolor=ft.colors.BLACK26, # Semi-transparent background for the form
                            width=300
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.START,
                    spacing=20,
                    padding=ft.padding.only(top=20)
                ),
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        padding=0
    )

    # Route change handler
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            # Welcome screen is the initial content of the page, not a separate view
            pass
        elif page.route == "/login":
            page.views.append(login_view)
        elif page.route == "/signup":
            page.views.append(signup_view)
        page.update()

    page.on_route_change = route_change
    page.go(page.route) # Go to the initial route

ft.app(target=main)
