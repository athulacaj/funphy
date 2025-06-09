import flet as ft
import random
import asyncio
from .utils import BG_COLOR,get_background_image, PRIMARY_COLOR,ConfettiWidget, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING
from .db import AppDatabase

WORDS = [
    # Unit 1: Reference Frames, Displacement, and Velocity
    "A reference frame is a perspective from which motion is observed.",
    "Displacement is the shortest distance from the initial to the final position.",
    # "Velocity is the rate of change of displacement with time.",
    # "Relative motion depends on the observer's reference frame.",
    # "A position vector points from the origin to the object's location.",
    # # Unit 2: Acceleration
    "Acceleration is the rate of change of velocity.",
    "Uniform acceleration means velocity changes at a constant rate.",
    # "Instantaneous acceleration is acceleration at a specific moment.",
    # "Deceleration is negative acceleration, slowing an object down.",
    # # Unit 3: Momentum and Inertia
    "Momentum is the product of mass and velocity.",
    "Inertia is an object's resistance to changes in motion.",
    # "Impulse is the change in momentum caused by a force.",
    # "Momentum is conserved in a closed system.",
    # "Mass is a measure of an object's inertia.",
    # # Unit 4: Kinetic Energy
    # "Kinetic energy is energy due to motion.",
    # "Work is done when a force moves an object.",
    # "The joule is the SI unit of energy.",
    # "Energy transfer occurs when work is done.",
    # "Kinetic energy depends on the square of speed.",
    # # Unit 5: Interactions I - Energy
    # "Potential energy is stored energy due to position.",
    # "Mechanical energy is the sum of kinetic and potential energy.",
    # "Energy transformation is the change from one form to another.",
    # "A system is a set of interacting parts considered together.",
    # "Energy is conserved in all physical processes."
]


LEVELS = [
    ("Easy", 80),
    ("Medium", 50),
    ("Hard", 25)
]


def split_words(words):
    n = len(words)
    chunk = n // 3
    return [
        words[:chunk],
        words[chunk:2*chunk],
        words[2*chunk:]
    ]


LEVEL_WORDS = split_words(WORDS)


def typing_game(page: ft.Page):
    page.title = "Typing Game"
    page.bgcolor = ft.Colors.WHITE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 0  # Remove page padding

    timer_value = ft.Ref[int]()
    timer_text = ft.Ref[ft.Text]()
    input_field = ft.Ref[ft.TextField]()
    feedback_text = ft.Ref[ft.Text]()
    start_button = ft.Ref[ft.ElevatedButton]()
    restart_button = ft.Ref[ft.ElevatedButton]()
    level_selector = ft.Ref[ft.Dropdown]()
    next_level_button = ft.Ref[ft.ElevatedButton]()

    current_word = ft.Ref[str]()
    timer_running = ft.Ref[bool]()
    letter_row = ft.Ref[ft.ListView]()
    word_list = ft.Ref[list]()
    current_level = ft.Ref[int]()
    word_index = ft.Ref[int]()

    letter_row.current = ft.ListView(
        controls=[],
        horizontal=True,
        expand=True,
        height=60,
        padding=0,
        spacing=0,
    )
    lv = letter_row.current

    async def timer_loop():
        timer_running.current = True
        while timer_value.current > 0 and timer_running.current:
            await asyncio.sleep(1)
            timer_value.current -= 1
            timer_text.current.value = f"Time left: {timer_value.current}s"
            page.update()
        if timer_running.current and timer_value.current <= 0:
            input_field.current.disabled = True
            feedback_text.current.value = f"Time's up! The word was: {current_word.current}"
            start_button.current.disabled = False
            restart_button.current.disabled = True
            page.update()
        timer_running.current = False

    def update_letter_row():
        typed = input_field.current.value or ""
        word = current_word.current or ""
        letters = []
        isValid = True
        for i, c in enumerate(word): 
            if i < len(typed):
                if typed[i] == c:
                    color = ACCENT_COLOR
                else:
                    color = ft.Colors.RED_500
                    isValid = False
                
                border = None
            elif i == len(typed):
                color = ft.Colors.CYAN_100
                border = ft.Border(bottom=ft.BorderSide(4, ACCENT_COLOR))
            else:
                color = TEXT_COLOR
                border = None
            letters.append(ft.Container(
                content=ft.Text(c, size=30, weight=ft.FontWeight.W_600, color=color),
                border=border,
                padding=ft.padding.only(bottom=2,right=5),
                key=str(i),
            ))
        if len(typed) > 0 and  isValid :
            #if last typed is space, add a space container
            if typed[-1] == " ":
                lv.scroll_to(key=str(len(typed)-3), duration=100)
        letter_row.current.controls = letters

        page.update()

    def next_word():
        if word_index.current is None:
            word_index.current = 0
        else:
            word_index.current += 1
        if word_index.current >= len(word_list.current):
            if current_level.current == len(LEVELS) - 1:
                AppDatabase.save_self_user_data_2({"beginner_feedback":{"score": 450}})
                # All levels complete
                page.views[-1].controls = [
                    ft.Stack([
                        get_background_image(),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("🎉 All levels complete! 🎉", size=28, weight=ft.FontWeight.W_600, color=ft.Colors.GREEN_500),
                            ], alignment="center", horizontal_alignment="center", spacing=20),
                            alignment=ft.alignment.center,
                            padding=40,
                            bgcolor=ft.Colors.TRANSPARENT,
                            border_radius=16,
                        ),
                        confetti
                    ], expand=True)
                ]
                page.confetti.animate_confetti()
                page.play_audio1()
                page.update()
                return
            else:
                page.confetti.animate_confetti()
                page.play_audio1()
                feedback_text.current.value = "Level complete! 🎉"
                input_field.current.disabled = True
                start_button.current.disabled = False
                restart_button.current.disabled = True
                timer_text.current.value = ""
                # Show next level button if not last level
                if current_level.current < len(LEVELS) - 1:
                    next_level_button.current.visible = True
                else:
                    next_level_button.current.visible = False
                page.update()
                return
        current_word.current = word_list.current[word_index.current]
        input_field.current.value = ""
        input_field.current.disabled = False
        input_field.current.focus()
        feedback_text.current.value = ""
        timer_value.current = LEVELS[current_level.current][1]
        timer_text.current.value = f"Time left: {timer_value.current}s"
        timer_running.current = True
        page.update()
        page.run_task(timer_loop)
        update_letter_row()

    def on_input_change(e):
        typed = input_field.current.value or ""
        word = current_word.current or ""
        if len(typed) > 0:
            for i in range(len(typed)):
                if i >= len(word) or typed[i] != word[i]:
                    input_field.current.value = typed[:i]
                    break
        update_letter_row()
        if input_field.current.value == word:
            timer_running.current = False
            feedback_text.current.value = "Correct! 🎉"
            page.confetti.animate_confetti()
            page.play_audio1()
            input_field.current.disabled = True
            page.update()
            async def pause_and_next():
                await asyncio.sleep(1)
                next_word()
                lv.scroll_to(offset=0, duration=1000)
            page.run_task(pause_and_next)

    def start_game(e=None):
        level_idx = int(level_selector.current.value)
        current_level.current = level_idx
        word_list.current = LEVEL_WORDS[level_idx]
        word_index.current = None
        next_word()
        start_button.current.disabled = True
        restart_button.current.disabled = False
        input_field.current.on_change = on_input_change
        lv.scroll_to(offset=0, duration=1000)
        page.update()

    def check_input(e):
        if input_field.current.value.strip() == current_word.current:
            timer_running.current = False
            feedback_text.current.value = "Correct! 🎉"
            input_field.current.disabled = True
            start_button.current.disabled = False
            restart_button.current.disabled = True
        else:
            feedback_text.current.value = "Keep trying!"
        page.update()

    def restart_game(e=None):
        timer_running.current = False
        input_field.current.value = ""
        input_field.current.disabled = True
        feedback_text.current.value = ""
        timer_text.current.value = ""
        start_button.current.disabled = False
        restart_button.current.disabled = True
        letter_row.current.controls = []
        word_index.current = None
        page.update()

    def go_to_next_level(e=None):
        if current_level.current < len(LEVELS) - 1:
            current_level.current += 1
            level_selector.current.value = str(current_level.current)
            word_list.current = LEVEL_WORDS[current_level.current]
            word_index.current = None
            next_level_button.current.visible = False
            next_word()
            start_button.current.disabled = True
            restart_button.current.disabled = False
            input_field.current.on_change = on_input_change
            page.update()


    # Add AppBar with back button
    def on_back(e):
        # page.go_back() if hasattr(page, 'go_back') else page.window_close()
        page.go("/dashboard") # Navigate to dashboard
    count= 0 if current_level.current is None else current_level.current
    appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=on_back,),
        title=ft.Text(f"Typing Game", weight=ft.FontWeight.W_600),
        bgcolor=BG_COLOR, # Defined in utils
        center_title=True,
        color=TEXT_COLOR,
        actions=[
            ft.Dropdown(
                ref=level_selector,
                width=130,
                value="0",
                options=[ft.dropdown.Option(str(i), text=LEVELS[i][0]) for i in range(3)],
                disabled=True
            ),
        ]
        # elevation=2,
    )


    confetti = ConfettiWidget()
    page.confetti=confetti
    return ft.View(
        "/typing_game",
        [
            ft.Stack([
            # Background image container
                get_background_image(),
                ft.Container(
                content= ft.Column(
                controls=[
                    # ft.Text("Type the word shown below before the timer runs out!", size=18),
                    ft.Row([
            
                        ft.ElevatedButton("Start", ref=start_button, on_click=start_game,bgcolor=PRIMARY_COLOR, color=ft.Colors.WHITE,),
                        ft.ElevatedButton("Restart", ref=restart_button, on_click=restart_game, disabled=True, bgcolor=PRIMARY_COLOR, color=ft.Colors.WHITE,),
                        ft.ElevatedButton("Next Level", ref=next_level_button, on_click=go_to_next_level, visible=False, bgcolor=PRIMARY_COLOR, color=ft.Colors.WHITE,),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text(ref=timer_text, size=20, color=TEXT_COLOR),
                    ft.Container(
                        content=letter_row.current,
                        alignment=ft.alignment.center,
                        padding=0,
                        expand=True,
                    ),
                    ft.TextField(ref=input_field, label="Type here...", on_submit=None, on_change=on_input_change, disabled=True, autofocus=True),
                    ft.Text(ref=feedback_text, size=20, color=ft.Colors.BLUE_500),
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    expand=True,
                ),
                padding=ft.padding.only(20, 10, 20, 0),
            ),
            confetti
            ],expand=True),

        ],
        padding=0,
        bgcolor=BG_COLOR,
        appbar=appbar,
    )