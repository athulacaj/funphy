import flet as ft


def main(page: ft.Page):
    page.title = "Blackboard Icon"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.WHITE  # So we can see the icon clearly

    # Colors
    BOARD_COLOR = ft.Colors.BLACK87
    BOARD_FRAME_COLOR = ft.Colors.WHITE  # A slightly lighter wood-like color for the frame
    TEXT_COLOR = ft.Colors.WHITE
    LEG_COLOR = ft.Colors.GREEN_ACCENT_700
    TOP_BAR_COLOR = ft.Colors.WHITE

    # Dimensions (approximate, can be adjusted)
    BOARD_WIDTH = 200
    BOARD_HEIGHT = 120
    FRAME_THICKNESS = 10
    LEG_WIDTH = 15
    LEG_HEIGHT = 80
    TOP_BAR_WIDTH = 60
    TOP_BAR_HEIGHT = 15
    size = 100  # Size of the text

    # Chalkboard Text
    chalk_text = ft.Text(
        "E=mc",
        color=TEXT_COLOR,
        size=30,
        weight=ft.FontWeight.BOLD,
    )
    superscript_2 = ft.Text(
        "2",
        color=TEXT_COLOR,
        size=18,
        weight=ft.FontWeight.BOLD,
        offset=ft.Offset(0, -0.35),  # Adjust for superscript effect
    )

    board_content = ft.Stack(
        [
            ft.Container(  # Blackboard
                width=BOARD_WIDTH,
                height=BOARD_HEIGHT,
                bgcolor=BOARD_COLOR,
                border_radius=5,
                alignment=ft.alignment.center,
                content=ft.Row(
                    [chalk_text, superscript_2],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START,  # Align '2' with top of 'c'
                    spacing=0,
                )
            ),
        ]
    )

    # Board with Frame
    board_with_frame = ft.Container(
        content=board_content,
        width=BOARD_WIDTH,
        bgcolor=ft.Colors.TRANSPARENT, 
        border_radius=8,  # Slightly larger radius for the frame
        border=ft.border.all(
            width=FRAME_THICKNESS,
            color=BOARD_FRAME_COLOR
        ),
        alignment=ft.alignment.center,
    )

    # Top Bar
    top_bar = ft.Container(
        width=TOP_BAR_WIDTH,
        height=TOP_BAR_HEIGHT,
        bgcolor=ft.Colors.TRANSPARENT,  # Set background to transparent
        border=ft.border.only(
            left=ft.BorderSide(width=3, color=TOP_BAR_COLOR),
            right=ft.BorderSide(width=3, color=TOP_BAR_COLOR),
            top=ft.BorderSide(width=3, color=TOP_BAR_COLOR)
        ),
        border_radius=ft.border_radius.only(top_left=3, top_right=3),
    )

    # Legs
    leg_style = {
        "width": LEG_WIDTH,
        "height": LEG_HEIGHT,
        "bgcolor": LEG_COLOR,
        "border_radius": 5,
    }
    left_leg = ft.Container(**leg_style, rotate=ft.Rotate(0.2))
    middle_leg = ft.Container(**leg_style)  # Straight
    right_leg = ft.Container(**leg_style, rotate=ft.Rotate(-0.2))

    tripod_legs = ft.Row(
        [left_leg, middle_leg, right_leg],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=-5,  # Overlap legs slightly
    )

    # Assemble the icon
    icon_layout = ft.Column(
        [
            top_bar,
            board_with_frame,
            ft.Container(height=2),  # Small spacer
            tripod_legs,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,  # No space between top_bar and board
    )

    page.add(
        ft.Container(
            content=icon_layout,
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.Colors.BLACK,  # Background color for the page
        ),
    )


ft.app(target=main)