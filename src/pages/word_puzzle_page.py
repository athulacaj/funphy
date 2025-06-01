import flet as ft
from .utils import BG_COLOR, get_background_image

def word_puzzle_page(page: ft.Page):
    # TODO: Implement the word puzzle UI based on the image provided

    content = ft.Column(
        controls=[
            ft.Text("Word Puzzle Page", size=30, weight=ft.FontWeight.BOLD),
            # Add word puzzle elements here
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.View(
        "/word_puzzle",
        [
            get_background_image(),
            ft.Container(
                content=content,
                expand=True,
                padding=ft.padding.all(20),
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.with_opacity(0.5, BG_COLOR), # Semi-transparent background
            )
        ],
        bgcolor=BG_COLOR,
        padding=0
    )
