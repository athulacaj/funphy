import flet as ft
from .utils import get_background_image, BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING
from .db import AppDatabase
import random
import asyncio

# Define colors from the image for better accuracy
BEGINNER_BG_COLOR = ft.Colors.with_opacity(0.8, ft.Colors.GREEN_ACCENT_700)
INTERMEDIATE_BG_COLOR = ft.Colors.with_opacity(0.8, ft.Colors.ORANGE_ACCENT_700)
ADVANCED_BG_COLOR = ft.Colors.with_opacity(0.8, ft.Colors.BLUE_ACCENT_700)
CARD_TEXT_COLOR = ft.Colors.WHITE
STAR_FILLED_COLOR = ft.Colors.AMBER
STAR_EMPTY_COLOR = ft.Colors.with_opacity(0.5, ft.Colors.WHITE)
PROGRESS_BAR_COLOR = ft.Colors.GREEN_ACCENT_400 # General progress bar color, can be customized per level
LOCK_ICON_COLOR = ft.Colors.WHITE70

def create_level_card(icon: ft.Icon, title: str, subtitle: str, progress_value: float, score: str, stars: int, total_stars: int, unlocked: bool, bgcolor: str, on_click=None):
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
                        ft.Icon(ft.Icons.GAMEPAD, color=ft.Colors.AMBER_ACCENT_200, size=16),  # Changed to a points icon
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
        ),
        on_click=on_click
    )


def dashboard_page(page: ft.Page):
    # Check if user is logged in
    user = AppDatabase.get_self_user_2()  # Get the currently logged-in user from the database
    
    if not user:
        # If not logged in, redirect to login page
        page.go("/login")
        return
        
    # User information from session
    user_name = user.get("name", "User")
    user_email = user.get("email", "")
    assessment_score = user.get("assessment_score", None)
    assessment_feedback_list = user.get("assessment_feedback", [])
    assessment_feedback = None
    if(len(assessment_feedback_list) and len(assessment_feedback_list[0])>0):
        assessment_feedback=assessment_feedback_list[0]

    beginner_feedback = user.get("beginner_feedback", None)
    beginner_score = None
    beginner_score_max = 300
    beginner_score_star = 0
    beginner_progress_value = 0
    if beginner_feedback:
        beginner_score = beginner_feedback.get("score", None)
        beginner_score_star = round((beginner_score / beginner_score_max) * 5, 2) if beginner_score is not None else 0
        beginner_progress_value = beginner_score / beginner_score_max if beginner_score is not None else 0
    is_beginner_unlocked = beginner_score is not None
    
    intermediate_feedback = user.get("intermediate_feedback", None)
    intermediate_score = None
    intermediate_score_max = 500
    intermediate_score_star = 0
    intermediate_progress_value = 0
    if intermediate_feedback:
        intermediate_score = intermediate_feedback.get("score", None)
        intermediate_score_star = round((intermediate_score / intermediate_score_max) * 5, 2) if intermediate_score is not None else 0
        intermediate_progress_value = intermediate_score / intermediate_score_max if intermediate_score is not None else 0

    advanced_feedback = user.get("advanced_feedback", None)
    advanced_score = None
    advanced_score_max = 1000
    advanced_score_star = 0
    advanced_progress_value = 0
    is_advanced_unlocked=intermediate_score is not None
    if advanced_feedback:
        advanced_score = advanced_feedback.get("score", None)
        advanced_score_star = round((advanced_score / advanced_score_max) * 5, 2) if advanced_score is not None else 0
        advanced_progress_value = advanced_score / advanced_score_max if advanced_score is not None else 0
    
    def logout(e):
        # Clear user data from session
        page.session.remove("user")
        
        # Show logout message
        page.snack_bar = ft.SnackBar(ft.Text("Logged out successfully"), bgcolor=ACCENT_COLOR)
        page.snack_bar.open = True
        
        # Redirect to welcome page
        page.go("/welcome")
        page.update()
        
    # Game Map Section - Horizontal Levels Layout
    def planet_level(icon, label, unlocked, on_click, bgcolor, border_color, star_color, score, stars, total_stars):
        return ft.Column(
            [
                ft.Icon(ft.Icons.STAR, color=star_color if unlocked else ft.Colors.GREY_400, size=32),
                ft.Container(
                    content=ft.Icon(icon, color=ft.Colors.WHITE, size=36),
                    width=64,
                    height=64,
                    bgcolor=bgcolor,
                    border=ft.border.all(3, border_color if unlocked else ft.Colors.GREY_400),
                    border_radius=32,
                    alignment=ft.alignment.center,
                    on_click=on_click if unlocked else None,
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.25, border_color),
                        offset=ft.Offset(2, 4),
                    ),
                
                ),
                ft.Container(height=6),
                ft.Text(label, size=14, weight=ft.FontWeight.BOLD, color=border_color if unlocked else ft.Colors.GREY_400),
                ft.Text(f"Score: {score if score is not None else 'N/A'}", size=12, color=ft.Colors.WHITE70),
                ft.Row(
                    [ft.Icon(ft.Icons.STAR, color=star_color if i < stars else ft.Colors.GREY_400, size=16) for i in range(total_stars)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        )

    # Horizontal layout for game map section
    game_map_section = ft.Container(
        ft.Column(
            [
                ft.Container(
                    content=ft.Stack(
                        [
                            # White path connector with box shadow
                            ft.Container(
                                width=4,
                                height=70,
                                left=100,
                                bottom=120,
                                rotate=ft.Rotate(45),
                                bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
                                border_radius=6,
                                
                                shadow=ft.BoxShadow(
                                    spread_radius=10,
                                    blur_radius=24,
                                    color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE),
                                    offset=ft.Offset(0, 0),
                                ),
                            ),
                            
                            ft.Container(
                                width=4,
                                height=80,
                                left=125,
                                top=65,
                                rotate=ft.Rotate(-.8),
                                bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
                                border_radius=6,
                                
                                shadow=ft.BoxShadow(
                                    spread_radius=10,
                                    blur_radius=24,
                                    color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE),
                                    offset=ft.Offset(0, 0),
                                ),
                            ),
                            
                            ft.Container(
                                planet_level(
                                    icon=ft.Icons.PUBLIC,
                                    label="INTERMEDIATE",
                                    unlocked=is_beginner_unlocked,
                                    on_click=lambda e: page.go("/path_game") if is_beginner_unlocked else None,
                                    bgcolor=ft.Colors.ORANGE_ACCENT_700,
                                    border_color=ft.Colors.ORANGE_ACCENT_400,
                                    star_color=ft.Colors.AMBER,
                                    score=f"{intermediate_score} / {intermediate_score_max}",
                                    stars=intermediate_score_star,
                                    total_stars=5,
                                ),
                                
                                right=0,  # Zigzag: align right
                                top=115,
                            ),
                            ft.Container(height=30),  # Spacer between levels
                            ft.Container(
                                planet_level(
                                    icon=ft.Icons.PUBLIC,
                                    label="ADVANCED",
                                    unlocked=is_advanced_unlocked,
                                    on_click=lambda e: page.go("/emoji_game") if is_advanced_unlocked else None,
                                    bgcolor=ft.Colors.BLUE_ACCENT_700,
                                    border_color=ft.Colors.BLUE_500,
                                    star_color=ft.Colors.AMBER,
                                    score=f"{advanced_score} / {advanced_score_max}",
                                    stars=advanced_score_star,
                                    total_stars=5,
                                ),
                                left=0,  # Zigzag: align left
                                top=0,
                            ),
                            ft.Container(height=30),  # Spacer between levels
                            ft.Container(
                                planet_level(
                                    icon=ft.Icons.PUBLIC,
                                    label="BEGINNER",
                                    unlocked=True,
                                    on_click=lambda e: page.go("/word_puzzle"),
                                    bgcolor=ft.Colors.GREEN_ACCENT_700,
                                    border_color=ft.Colors.GREEN_ACCENT_400,
                                    star_color=ft.Colors.AMBER,
                                    score=f"{beginner_score} / {intermediate_score_max}",
                                    stars=beginner_score_star,
                                    total_stars=5,
                                ),
                                left=0,
                                bottom=0  # Zigzag: align left at bottom
                            ),
                        ],
                        height=400,
                        width=250,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            spacing=10,
        ),
        padding=ft.padding.symmetric(vertical=30, horizontal=20),
    )

    # --- Animated White Stars Logic ---
    num_stars = 16
    star_states = [dict(left=0, top=0, size=16, visible=False) for _ in range(num_stars)]
    star_controls = [ft.Container() for _ in range(num_stars)]

    def update_stars():
        for i, state in enumerate(star_states):
            star_controls[i].content = ft.AnimatedSwitcher(
                content=ft.Icon(ft.Icons.STAR, color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE), size=state['size']) if state['visible'] else ft.Container(),
                duration=300,
            )
            star_controls[i].left = state['left']
            star_controls[i].top = state['top']
            star_controls[i].width = 32
            star_controls[i].height = 32
        page.update()

    async def star_pop_loop(i):
        while True:
            if(page.route != "/dashboard"):
                break
            await asyncio.sleep(random.uniform(0.8, 2.5))
            star_states[i]['left'] = random.randint(0, 220)
            star_states[i]['top'] = random.randint(0, 350)
            star_states[i]['size'] = random.randint(12, 28)
            star_states[i]['visible'] = True
            update_stars()
            await asyncio.sleep(random.uniform(0.5, 1.2))
            star_states[i]['visible'] = False
            update_stars()

    async def start_star_animation():
        await asyncio.sleep(0.5)
        for i in range(num_stars):
            asyncio.create_task(star_pop_loop(i))

    # Schedule the animation to start after the page is loaded
    page.run_task(start_star_animation)

    # Dashboard content
    # Create user avatar with first letter of user name
    user_initial = user_name[0].upper() if user_name else "U"
    user_avatar = ft.Container(
        content=ft.Text(user_initial, color=ft.Colors.WHITE, size=28, weight=ft.FontWeight.W_600),
        width=50,
        height=50,
        margin=ft.margin.all(6),
        bgcolor=ft.Colors.TRANSPARENT,
        border_radius=25,
        border=ft.border.all(1, ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
        alignment=ft.alignment.center,
        on_click=lambda _:page.go("/profile")
    )
    return ft.View(
        "/dashboard",
        [
            ft.AppBar(
                
                leading=user_avatar,
                title=ft.Text(f"Welcome, {user_name}!", size=20, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                center_title=True,
                bgcolor=BG_COLOR,
                elevation=0,
                actions=[
                    # ft.IconButton(
                    #     icon=ft.Icons.SEARCH,
                    #     icon_color=TEXT_COLOR,
                    #     on_click=on_search
                    # ),
                    ft.PopupMenuButton(items=[
                        # ft.PopupMenuItem(
                        #     text="Profile",
                        #     icon=ft.Icons.PERSON,
                        #     on_click=lambda e: page.go("/profile")
                        # ),
                         ft.PopupMenuItem(
                            text="Logout",
                            icon=ft.Icons.LOGOUT,
                            on_click=logout
                        ),
                        ft.PopupMenuItem(
                            text="Settings",
                            icon=ft.Icons.SETTINGS,
                            on_click=lambda e: page.go("/settings")
                        ),
                    ]),
                ],
            ),
            ft.Stack([
                # Background image container
                get_background_image(),
                # Animated white stars (no custom control)
                ft.Stack(star_controls, width=250, height=380),
                # Content
                ft.Container(
                    ft.Column(
                        [   
                            
                            # ft.Container(height=20),  # Spacer
                            
                            *([
                                # Game Map Section added here
                                game_map_section,
                                
                                ft.Container(height=20) # Spacer
                            ] if True else []),


                              ft.Row([
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.MENU_BOOK, color=ACCENT_COLOR, size=26),
                                            ft.ElevatedButton(
                                                "Learning Modules",
                                                on_click=lambda e: page.go("/learning_modules"),
                                                style=ft.ButtonStyle(
                                                    bgcolor=PRIMARY_COLOR,
                                                    color=TEXT_COLOR,
                                                    padding=BUTTON_PADDING
                                                )
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=8
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.12, PRIMARY_COLOR),
                                    border_radius=16,
                                    padding=ft.padding.symmetric(vertical=8, horizontal=18),
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=6,
                                        color=ft.Colors.with_opacity(0.18, PRIMARY_COLOR),
                                        offset=ft.Offset(1, 2),
                                    ),
                                )
                            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                            
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        expand=True,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                ),
            ],expand=True),
        ],
        bgcolor=BG_COLOR,
        padding=0
        # scroll=ft.ScrollMode.AUTO # Added scroll for potentially long content
    )

