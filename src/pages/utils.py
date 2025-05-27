import flet as ft
import os

# Define theme colors
BG_COLOR = "#0F111A"  # Deep Twilight
PRIMARY_COLOR = "#7B68EE"  # Medium Slate Blue
ACCENT_COLOR = "#36F1CD"  # Aqua Mint
TEXT_COLOR = ft.Colors.WHITE
BUTTON_PADDING = ft.padding.symmetric(vertical=12, horizontal=24)

# Path to background image
BG_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png")

# Define reusable components
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
