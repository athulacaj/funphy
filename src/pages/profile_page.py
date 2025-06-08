import flet as ft
from .utils import get_background_image, BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING
from .db import AppDatabase
def profile_page(page: ft.Page):
    user = AppDatabase.get_self_user_2()
    if not user:
        page.go("/login")
        return

    user_name = user.get("name", "User")
    user_email = user.get("email", "email")
    user_avatar = user.get("avatar", None)

    beginner_feedback = user.get("beginner_feedback", None)
    intermediate_feedback = user.get("intermediate_feedback", None)
    advanced_feedback = user.get("advanced_feedback", None)
    assessment_feedback= user.get("assessment_feedback", [])
    assment_reslt= assessment_feedback[0] if len(assessment_feedback) > 0 else "N/A"
    level="N/A"
    score=0
    if advanced_feedback:
        level = "Advanced"
        score = advanced_feedback.get("score", 0)
    elif intermediate_feedback:
        level = "Intermediate"
        score = intermediate_feedback.get("score", 0)
    elif beginner_feedback:
        level = "Beginner"
        score = beginner_feedback.get("score", 0)

    def edit_username(e):
        # Placeholder for edit username logic
        page.snack_bar = ft.SnackBar(ft.Text("Edit username not implemented"), bgcolor=ACCENT_COLOR)
        page.snack_bar.open = True
        page.update()

    def change_avatar(e):
        # Placeholder for change avatar logic
        page.snack_bar = ft.SnackBar(ft.Text("Change avatar not implemented"), bgcolor=ACCENT_COLOR)
        page.snack_bar.open = True
        page.update()

    return ft.View(
        "/profile",
        [
            ft.AppBar(
                leading=ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    on_click=lambda _: page.go("/dashboard"),
                    icon_color=TEXT_COLOR,
                    icon_size=30
                ),
                title=ft.Text("Profile", size=25, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                center_title=True,
                bgcolor=BG_COLOR,
                elevation=0,
            ),
            ft.Container(
                ft.Column(
                    [
                        ft.Container(height=10),
                        ft.Container(
                            ft.Column([
                                ft.Text("Player username:", size=16, color=TEXT_COLOR, italic=True),
                                ft.Row([
                                    ft.Text(user_name, size=20, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                                    # ft.IconButton(ft.Icons.EDIT, icon_color=ACCENT_COLOR, on_click=edit_username, icon_size=18),
                                ], alignment=ft.MainAxisAlignment.START),
                                ft.Divider(),
                            ]),
                            padding=15,
                            border=ft.border.all(2, ACCENT_COLOR),
                            border_radius=10,
                            width=300,
                        ),
                        ft.Container(height=10),
                        ft.Container(
                            ft.Column([
                                ft.Text("User Email", size=16, color=TEXT_COLOR),
                                ft.Text(user_email, size=20, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                            ]),
                            padding=10,
                            border=ft.border.all(2, ACCENT_COLOR),
                            border_radius=10,
                            width=300,
                        ),
                        
                        # ft.Container(height=10),
                        # ft.Container(
                        #     ft.Column([
                        #         ft.Text("Change Avatar", size=16, color=TEXT_COLOR),
                        #         ft.Row([
                        #             ft.IconButton(ft.Icons.FEMALE, icon_color=ft.Colors.PINK_400, on_click=change_avatar),
                        #             ft.IconButton(ft.Icons.MALE, icon_color=ft.Colors.BLUE_400, on_click=change_avatar),
                        #             ft.IconButton(ft.Icons.PALETTE, icon_color=ft.Colors.GREEN_400, on_click=change_avatar),
                        #         ], alignment=ft.MainAxisAlignment.START, spacing=10),
                        #     ]),
                        #     padding=10,
                        #     border=ft.border.all(2, ACCENT_COLOR),
                        #     border_radius=10,
                        #     width=300,
                        # ),
                        
                        ft.Container(height=10),
                        ft.Container(
                            ft.Column([
                                ft.Text("Level and Progress", size=16, weight=ft.FontWeight.W_600, color=ACCENT_COLOR),
                                ft.Divider(),
                                ft.Text(level, size=18, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                                ft.Text(score, size=14, color=TEXT_COLOR),
                                ft.Text(f"Assment Feedback: {assment_reslt}", size=16, weight=ft.FontWeight.W_600, color=ACCENT_COLOR),
                            ]),
                            padding=15,
                            border=ft.border.all(2, ACCENT_COLOR),
                            border_radius=10,
                            width=300,
                        ),
                        ft.Container(height=10),
                        ft.Row([
                            ft.IconButton(ft.Icons.CHEVRON_LEFT, on_click=lambda e: page.go("/dashboard"), icon_color=ACCENT_COLOR),
                        ], alignment=ft.MainAxisAlignment.END, width=300),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                alignment=ft.alignment.center,
                expand=True,
            ),
        ],
        bgcolor=BG_COLOR,
        scroll=ft.ScrollMode.AUTO,
    )
