# FunPhy - Fun with Physics App Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Theme and Utilities](#theme-and-utilities)
3. [Application Flow](#application-flow)
4. [Pages](#pages)
   - [Splash Page](#splash-page)
   - [Welcome Page](#welcome-page)
   - [Login Page](#login-page)
   - [Signup Page](#signup-page)
   - [Dashboard Page](#dashboard-page)
5. [Main Application File](#main-application-file)

---

## Introduction

FunPhy is a Fun with Physics application built with Flet, a framework for building interactive multi-user web, desktop, and mobile applications in Python.

The application features a complete user authentication flow with splash screen, welcome page, login, signup, and dashboard functionality.

## Theme and Utilities

The application uses a consistent color scheme and reusable components defined in `utils.py`:

```python
# Define theme colors
BG_COLOR = "#0F111A"           # Deep Twilight - Background color
PRIMARY_COLOR = "#7B68EE"      # Medium Slate Blue - Primary accent color
ACCENT_COLOR = "#36F1CD"       # Aqua Mint - Secondary accent color
TEXT_COLOR = ft.Colors.WHITE   # White text
BUTTON_PADDING = ft.padding.symmetric(vertical=12, horizontal=24)  # Consistent button padding
```

Reusable function for background image:

```python
def get_background_image():
    return ft.Container(
        expand=True,
        alignment=ft.alignment.bottom_right,
        content=ft.Image(
            src=BG_IMAGE_PATH,
            fit=ft.ImageFit.COVER,
            opacity=0.2,
        ),
    )
```

## Application Flow

The application follows a linear navigation flow:

1. Splash Page (`/`) → 
2. Welcome Page (`/welcome`) → 
3. Login Page (`/login`) or Signup Page (`/signup`) → 
4. Dashboard Page (`/dashboard`)

## Pages

### Splash Page

**File:** `splash_page.py`

The splash page serves as the entry point to the application, displaying the application icon and name with a "Get Started" button.

**Key Components:**
- Game icon
- Application name
- "Get Started" button to navigate to the welcome page

**Code Sample:**
```python
def get_view(page: ft.Page):
    return ft.View(
        "/",
        [
            ft.Stack([
                # Background image container
                get_background_image(),
                # Content
                ft.Container(
                    ft.Column(
                        [
                            ft.Container(
                                ft.Icon(ft.Icons.VIDEOGAME_ASSET, size=100, color=ACCENT_COLOR),
                                width=140, height=140,
                                bgcolor=PRIMARY_COLOR,
                                border_radius=70,
                            ),
                            ft.Text("Game App Name", size=30, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    "Get Started", 
                                    on_click=lambda e: page.go("/welcome"), 
                                    style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=TEXT_COLOR, padding=BUTTON_PADDING),
                                    width=200,
                                ),
                                alignment=ft.alignment.center,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                )
            ])
        ]
    )
```

### Welcome Page

**File:** `welcome_page.py`

The welcome page presents users with options to log in or sign up.

**Key Components:**
- Greeting message
- "Log In" button to navigate to the login page
- "Sign Up" button to navigate to the signup page

**Code Sample:**
```python
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
                                    ft.ElevatedButton("Log In", on_click=lambda e: page.go("/login"), 
                                                    style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=TEXT_COLOR, padding=BUTTON_PADDING)),
                                    ft.ElevatedButton("Sign Up", on_click=lambda e: page.go("/signup"), 
                                                    style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=TEXT_COLOR, padding=BUTTON_PADDING)),
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
                )
            ])
        ]
    )
```

### Login Page

**File:** `login_page.py`

The login page allows users to authenticate with their email and password.

**Key Components:**
- Email input field
- Password input field (with reveal option)
- Error message display
- Login button with loading indicator
- Retry connection button (displayed on connection errors)
- Back button to return to welcome page

**Key Functionality:**
- Form validation
- User authentication via UserDatabase
- Error handling for database connection issues
- Session management for storing user data

**Code Sample (Form Section):**
```python
# Create form fields
email = ft.TextField(label="Email", color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
password = ft.TextField(label="Password", password=True, can_reveal_password=True, color=TEXT_COLOR, border_color=ACCENT_COLOR, focused_border_color=ACCENT_COLOR)
# Create error text
error_text = ft.Text("", color=ft.Colors.RED_400, size=12, visible=False)
```

### Signup Page

**File:** `signup_page.py`

The signup page allows users to create a new account.

**Key Components:**
- Name input field
- Email input field
- Password input field (with reveal option)
- Confirm password input field (with reveal option)
- Error message display
- Sign Up button with loading indicator
- Back button to return to welcome page

**Key Functionality:**
- Form validation including password matching
- User creation via UserDatabase
- Error handling for database operations

**Code Sample (Form Validation):**
```python
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
```

### Dashboard Page

**File:** `dashboard_page.py`

The dashboard page displays user information and provides application functionality after successful authentication.

**Key Components:**
- User greeting with name
- User email display
- Dashboard content area (placeholder)
- Logout button

**Key Functionality:**
- Session verification to ensure user is logged in
- Session management for user logout
- Redirect to login page if not authenticated

**Code Sample:**
```python
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
    
    def logout(e):
        # Clear user data from session
        page.session.remove("user")
        
        # Show logout message
        page.snack_bar = ft.SnackBar(ft.Text("Logged out successfully"), bgcolor=ACCENT_COLOR)
        page.snack_bar.open = True
        
        # Redirect to welcome page
        page.go("/welcome")
        page.update()
```

## Main Application File

**File:** `main.py`

The main application file initializes the Flet application and sets up the routing system.

**Key Functionality:**
- Application initialization
- Page title and theme setup
- Route configuration for all pages
- Default route handling

**Code Sample:**
```python
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
```

---
