import flet as ft
import random
import threading
from .db import AppDatabase
import flet_audio as fa


# Define theme colors
# BG_COLOR = "#0F111A"  # Deep Twilight
BG_COLOR = "#120C6E"  # Deep Twilight
PRIMARY_COLOR = "#7B68EE"  # Medium Slate Blue
ACCENT_COLOR = "#36F1CD"  # Aqua Mint
SNACK_COLOR = "#04332A"  # Aqua Mint
TEXT_COLOR = ft.Colors.WHITE
BUTTON_PADDING = ft.padding.symmetric(vertical=12, horizontal=24)
# Path to background image
# BG_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png")

# Define reusable components
def get_background_image(showImage=True):
    # return ft.Container(
    #     expand=True,
    #     alignment=ft.alignment.bottom_right,
    #     content=ft.Image(
    #         src="icon.png",  # Ensure this path is correct
    #         fit=ft.ImageFit.COVER,
    #         opacity=0.2,
    #     ),
    # )

    return ft.Container(
            content=ft.Image(
                src="icon.png",  # Ensure this path is correct
                fit=ft.ImageFit.COVER,
                opacity=0.2,
            ) if showImage else None,  # Show image only if showImage is True
            alignment=ft.alignment.center,  # Center content within container
            expand=True,
            margin=0,
            padding=0,  # Remove inbuilt padding
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.Colors.with_opacity(1,BG_COLOR),  # hsla(244, 80%, 24%, 1)
                    ft.Colors.with_opacity(1,"#400576"),  # hsla(271, 94%, 49%, 1)
                    ft.Colors.with_opacity(1,BG_COLOR),
                ],
                stops=[0.0, 0.5, 1.0],
            ),
        )

click1_audio = fa.Audio(
    src="audio/click1.wav",
    autoplay=False,
)
error_audio = fa.Audio(
    src="audio/error1.wav",
    autoplay=False,
)
audio1 = fa.Audio(
    src="audio/win1.wav",
    autoplay=False,
)
def ConfettiWidget(width=None, height=600, dot_count=300, distance=1300):
    play_sound=AppDatabase.get_self_user_2().get("play_sound", True) if AppDatabase.get_self_user_2() else True
    def play_click_sound():
        if play_sound:
            try:
                click1_audio.seek(0)
                click1_audio.play()
            except Exception as e:
                pass
    def play_error_sound():       
        if play_sound: 
            try:
                error_audio.seek(0)
                error_audio.play()
            except Exception as e:
                pass

    def create_confetti_piece():
        return ft.Container(
            width=6,
            height=6,
            bgcolor=random.choice([
                ft.Colors.RED_400,
                ft.Colors.BLUE_500,
                ft.Colors.GREEN_400,
                ft.Colors.AMBER_ACCENT,
                ft.Colors.PURPLE_400,
                ft.Colors.PINK_400
            ]),
            border_radius=3,
            left=random.randint(0, distance),
            top=random.randint(0, distance),
            margin=2,
            animate_position=ft.Animation(
                random.randint(800, 1400),
                curve=random.choice([
                    ft.AnimationCurve.BOUNCE_OUT,
                    ft.AnimationCurve.EASE_IN_OUT,
                    ft.AnimationCurve.ELASTIC_OUT,
                    ft.AnimationCurve.EASE_OUT_BACK
                ])
            ),
        )

    confetti_pieces = [create_confetti_piece() for _ in range(dot_count)]
    confetti_stack = ft.Stack(controls=confetti_pieces, expand=True if width is None else False, width=width, height=height, visible=False)

    def clearview():
        confetti_stack.visible=False
        confetti_stack.update()
        column.update()

    def animate_confetti(e=None):
        if(confetti_stack.visible is False):
            threading.Timer(0.1, animate_confetti).start()
            if play_sound:
                try:
                    audio1.seek(0)
                    audio1.play()
                except Exception as e:
                    pass
            threading.Timer(1.5,clearview).start()
        
        confetti_stack.visible = True
        for piece in confetti_pieces:
            piece.left = random.randint(0, distance)
            piece.top = random.randint(0, distance)
            piece.animate_position = ft.Animation(
                random.randint(1500, 2200),
                curve=random.choice([
                    ft.AnimationCurve.BOUNCE_OUT,
                    ft.AnimationCurve.EASE_IN_OUT,
                    ft.AnimationCurve.ELASTIC_OUT,
                    ft.AnimationCurve.EASE_OUT_BACK
                ])
            )
        confetti_stack.update()
        column.update()

    confetti_button = ft.ElevatedButton("Confetti!", on_click=animate_confetti, bgcolor=ft.Colors.BLUE_500, color=ft.Colors.WHITE)

    column = ft.Column([
        audio1,
        click1_audio,
        error_audio,
        confetti_stack,
        # confetti_button
    ])
    column.animate_confetti = animate_confetti  # Expose animate_confetti as an attribute
    column.play_click_sound = play_click_sound  # Expose play_click_sound as an attribute
    column.play_error_sound = play_error_sound  # Expose play_error_sound as an attribute
    return column


