import flet as ft
from .utils import get_background_image, BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING

# Define colors from the image for better accuracy
BEGINNER_BG_COLOR = ft.Colors.with_opacity(0.8, ft.Colors.GREEN_ACCENT_700)
INTERMEDIATE_BG_COLOR = ft.Colors.with_opacity(0.8, ft.Colors.ORANGE_ACCENT_700)
ADVANCED_BG_COLOR = ft.Colors.with_opacity(0.8, ft.Colors.BLUE_ACCENT_700)
CARD_TEXT_COLOR = ft.Colors.WHITE
STAR_FILLED_COLOR = ft.Colors.AMBER
STAR_EMPTY_COLOR = ft.Colors.with_opacity(0.5, ft.Colors.WHITE)
PROGRESS_BAR_COLOR = ft.Colors.GREEN_ACCENT_400 # General progress bar color, can be customized per level
LOCK_ICON_COLOR = ft.Colors.WHITE70

def create_level_card(icon: ft.Icon, title: str, subtitle: str, progress_value: float, score: str, stars: int, total_stars: int, unlocked: bool, bgcolor: str):
    """Helper function to create a level card."""
    star_icons = [ft.Icon(ft.Icons.STAR, color=STAR_FILLED_COLOR if i < stars else STAR_EMPTY_COLOR) for i in range(total_stars)]
    
    lock_status_content = [
        ft.Icon(ft.Icons.LOCK_OPEN if unlocked else ft.Icons.LOCK, color=LOCK_ICON_COLOR, size=18),
        ft.Text("Unlocked" if unlocked else "Locked", color=LOCK_ICON_COLOR, size=12, weight=ft.FontWeight.W_500)
    ]

    return ft.Container(
        content=ft.Column(
            [
                ft.Row([icon, ft.Text(title, weight=ft.FontWeight.BOLD, size=12, color=CARD_TEXT_COLOR)], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                ft.Container(height=5),
                ft.Text(subtitle, weight=ft.FontWeight.BOLD, size=18, color=CARD_TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.MONETIZATION_ON_OUTLINED, color=ft.Colors.AMBER_ACCENT_200, size=16),
                        ft.Text(score, color=CARD_TEXT_COLOR, size=12),
                        ft.ProgressBar(value=progress_value, width=60, color=PROGRESS_BAR_COLOR, bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                        ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER_ACCENT_200, size=16),
                        ft.Text("Maxed", color=CARD_TEXT_COLOR, size=12, weight=ft.FontWeight.BOLD) # Assuming "Macined" means Maxed
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=10),
                ft.Row(star_icons, alignment=ft.MainAxisAlignment.CENTER, spacing=2),
                ft.Container(height=10),
                ft.Row(lock_status_content, alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        ),
        bgcolor=bgcolor,
        padding=ft.padding.symmetric(vertical=15, horizontal=20),
        border_radius=10,
        width=220, # Adjusted width for better fit
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(2, 2),
        )
    )

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
    assessment_score = user.get("assessment_score", None)
    
    def logout(e):
        # Clear user data from session
        page.session.remove("user")
        
        # Show logout message
        page.snack_bar = ft.SnackBar(ft.Text("Logged out successfully"), bgcolor=ACCENT_COLOR)
        page.snack_bar.open = True
        
        # Redirect to welcome page
        page.go("/welcome")
        page.update()
        
    # Game Map Section
    game_map_section = ft.Container(
        ft.Column(
            [
                ft.Text("Game Levels", size=28, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR, text_align=ft.TextAlign.CENTER),
                ft.Container(height=15),
                ft.Row(
                    [
                        # create_level_card(
                        #     icon=ft.Icon(ft.Icons.GRASS, color=ft.Colors.GREEN_ACCENT_400, size=30),
                        #     title="BEGINNER",
                        #     subtitle="BEGINNER",
                        #     progress_value=0.8, # Example: 80%
                        #     score="32,00",
                        #     stars=4,
                        #     total_stars=5,
                        #     unlocked=True,
                        #     bgcolor=BEGINNER_BG_COLOR
                        # ),
                        create_level_card(
                            icon=ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color=ft.Colors.ORANGE_ACCENT_400, size=30),
                            title="INTERMEDIATE", # Corrected spelling
                            subtitle="INTERMEDIATE", # Corrected spelling
                            progress_value=0.5, # Example: 50%
                            score="10,00",
                            stars=3,
                            total_stars=5,
                            unlocked=True, # Assuming intermediate is also unlocked for now
                            bgcolor=INTERMEDIATE_BG_COLOR
                        ),
                        create_level_card(
                            icon=ft.Icon(ft.Icons.DIAMOND, color=ft.Colors.BLUE_ACCENT_200, size=30), # Using diamond as a proxy for crystal
                            title="ADVANCED",
                            subtitle="ADVANCED",
                            progress_value=0.2, # Example: 20%
                            score="22,00",
                            stars=2,
                            total_stars=5,
                            unlocked=False, # Assuming advanced is locked
                            bgcolor=ADVANCED_BG_COLOR
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=25, # Increased spacing between cards
                    wrap=True, # Allow wrapping on smaller screens
                    vertical_alignment=ft.CrossAxisAlignment.START,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.padding.symmetric(vertical=30, horizontal=20), # Added padding around the section
        # margin=ft.margin.only(top=20) # Add some top margin
    )

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
                            
                            # Game Map Section added here
                            game_map_section,
                            
                            ft.Container(height=20), # Spacer

                            ft.Container(
                                ft.Column(
                                    [
                                        ft.Text("Dashboard Actions", size=24, weight=ft.FontWeight.W_500, color=PRIMARY_COLOR), # Changed title
                                        ft.Text("Your personal dashboard content will appear here.", size=14, color=TEXT_COLOR),
                                        
                                        ft.Container(height=20),  # Spacer
                                        
                                        # Conditionally show the button
                                        *([
                                            ft.ElevatedButton(
                                                "Start Physics Assessment", 
                                                on_click=lambda e: page.go("/assessment/intro"),
                                                style=ft.ButtonStyle(
                                                    bgcolor=ACCENT_COLOR, 
                                                    color=BG_COLOR, 
                                                    padding=BUTTON_PADDING
                                                )
                                            )
                                        ] if assessment_score is None else []),
                                    ],
                                    spacing=10,
                                ),
                                padding=20,
                                border_radius=10,
                                bgcolor=ft.Colors.BLACK12, # Kept original bgcolor for this specific container
                                width=400, # Kept original width
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
                    height=page.window.height if page.window else 600, # Adjusted to use page.window.height
                ),
            ])
        ],
        bgcolor=BG_COLOR,
        scroll=ft.ScrollMode.AUTO # Added scroll for potentially long content
    )
