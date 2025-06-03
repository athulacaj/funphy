import flet as ft
from .utils import get_background_image, BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING
from .db import AppDatabase

# Define colors from the image for better accuracy
BEGINNER_BG_COLOR = ft.Colors.with_opacity(0.8, ft.Colors.GREEN_ACCENT_700)
INTERMEDIATE_BG_COLOR = ft.Colors.with_opacity(0.8, ft.Colors.ORANGE_ACCENT_700)
ADVANCED_BG_COLOR = ft.Colors.with_opacity(0.8, ft.Colors.BLUE_ACCENT_700)
CARD_TEXT_COLOR = ft.Colors.WHITE
STAR_FILLED_COLOR = ft.Colors.AMBER
STAR_EMPTY_COLOR = ft.Colors.with_opacity(0.5, ft.Colors.WHITE)
PROGRESS_BAR_COLOR = ft.Colors.GREEN_ACCENT_400 # General progress bar color, can be customized per level
LOCK_ICON_COLOR = ft.Colors.WHITE70


def settings_page(page: ft.Page):
    play_sound=AppDatabase.get_self_user_2().get("play_sound", True) if AppDatabase.get_self_user_2() else True
    def on_toggle_appearance(e):
        # Handle appearance toggle
        pass

    def on_toggle_notifications(e):
        # Handle notifications toggle
        pass

    def on_toggle_sounds(e):
        # Handle sounds toggle
        play_sound= e.control.value
        AppDatabase.save_self_user_data_2({"play_sound": play_sound})
        pass

    def on_credits(e):
        # Handle credits button
        pass

    def on_switch_account(e):
        # Handle switch account button
        on_logout(e)
        # pass

    def on_delete_account(e):
        AppDatabase.delete_self_user()
        on_logout(e)


    def on_logout(e):
        # Clear user data from session
        page.session.remove("user")
        page.snack_bar = ft.SnackBar(ft.Text("Logged out successfully"), bgcolor=ACCENT_COLOR)
        page.snack_bar.open = True
        page.go("/welcome")
        page.update()

    return ft.View(
        "/settings",
        [
            ft.AppBar(
                title=ft.Text("Settings", size=30, weight=ft.FontWeight.W_600, color=ACCENT_COLOR),
                center_title=True,
                bgcolor=BG_COLOR,
                elevation=0,
                leading=ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    on_click=lambda _: page.go("/dashboard"),
                    icon_color=TEXT_COLOR,
                    icon_size=30
                ),
            ),
            ft.Container(
                ft.Column([
                    ft.Container(
                        ft.Column([
                            ft.Text("Menu Settings", size=26, weight=ft.FontWeight.W_600, color=TEXT_COLOR, italic=True, text_align=ft.TextAlign.CENTER),
                            ft.Container(height=15),
                            # ft.Row([
                            #     ft.Text("Appearance", size=18, color=TEXT_COLOR),
                            #     ft.Switch(value=False, on_change=on_toggle_appearance, active_color=PRIMARY_COLOR, thumb_color=PRIMARY_COLOR),
                            # ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            # ft.Row([
                            #     ft.Text("Notifications", size=18, color=TEXT_COLOR),
                            #     ft.Switch(value=False, on_change=on_toggle_notifications, active_color=PRIMARY_COLOR, thumb_color=PRIMARY_COLOR),
                            # ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([
                                ft.Text("Sounds", size=18, color=TEXT_COLOR, italic=True),
                                ft.Switch(value=play_sound, on_change=on_toggle_sounds, active_color=PRIMARY_COLOR, thumb_color=PRIMARY_COLOR),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Container(height=20),
                            # ft.ElevatedButton("Credits", on_click=on_credits, style=ft.ButtonStyle(bgcolor=BG_COLOR, color=TEXT_COLOR, side=ft.BorderSide(1, TEXT_COLOR))),
                            ft.ElevatedButton("Switch Account", on_click=on_switch_account, style=ft.ButtonStyle(bgcolor=BG_COLOR, color=TEXT_COLOR, side=ft.BorderSide(1, TEXT_COLOR))),
                            ft.ElevatedButton("Delete Account", on_click=on_delete_account, style=ft.ButtonStyle(bgcolor=BG_COLOR, color=TEXT_COLOR, side=ft.BorderSide(1, TEXT_COLOR))),
                            ft.ElevatedButton("Log Out", on_click=on_logout, style=ft.ButtonStyle(bgcolor=BG_COLOR, color=TEXT_COLOR, side=ft.BorderSide(1, TEXT_COLOR))),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        ),
                        padding=20,
                        border=ft.border.all(2, TEXT_COLOR),
                        border_radius=20,
                        bgcolor=BG_COLOR,
                        width=350,
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                ),
                alignment=ft.alignment.center,
                expand=True,
                padding=ft.padding.symmetric(vertical=30, horizontal=0),
                bgcolor=BG_COLOR
            )
        ],
        bgcolor=BG_COLOR
    )