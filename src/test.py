import flet as ft
import random
import asyncio

WORDS = [
    # Unit 1: Reference Frames, Displacement, and Velocity
    "A reference frame is a perspective from which motion is observed.",
    "Displacement is the shortest distance from the initial to the final position.",
    "Velocity is the rate of change of displacement with time.",
    # "Relative motion depends on the observer's reference frame.",
    # "A position vector points from the origin to the object's location.",
    # # Unit 2: Acceleration
    # "Acceleration is the rate of change of velocity.",
    # "Uniform acceleration means velocity changes at a constant rate.",
    # "Instantaneous acceleration is acceleration at a specific moment.",
    # "Deceleration is negative acceleration, slowing an object down.",
    # # Unit 3: Momentum and Inertia
    # "Momentum is the product of mass and velocity.",
    # "Inertia is an object's resistance to changes in motion.",
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
                    color = ft.Colors.GREEN_500
                else:
                    color = ft.Colors.RED_500
                    isValid = False
                
                border = None
            elif i == len(typed):
                color = ft.Colors.BLACK
                border = ft.Border(bottom=ft.BorderSide(2, ft.Colors.BLUE_500))
            else:
                color = ft.Colors.BLACK
                border = None
            letters.append(ft.Container(
                content=ft.Text(c, size=30, weight=ft.FontWeight.W_600, color=color),
                border=border,
                padding=ft.padding.only(bottom=2),
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
            input_field.current.disabled = True
            page.update()
            async def pause_and_next():
                await asyncio.sleep(0.5)
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

    return ft.Container(
            content= ft.Column(
            controls=[
                # ft.Text("Type the word shown below before the timer runs out!", size=18),
                ft.Dropdown(
                    ref=level_selector,
                    width=120,
                    value="0",
                    options=[ft.dropdown.Option(str(i), text=LEVELS[i][0]) for i in range(3)],
                    disabled=True
                ),
                ft.Row([
           
                    ft.ElevatedButton("Start", ref=start_button, on_click=start_game),
                    ft.ElevatedButton("Restart", ref=restart_button, on_click=restart_game, disabled=True),
                    ft.ElevatedButton("Next Level", ref=next_level_button, on_click=go_to_next_level, visible=False),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text(ref=timer_text, size=20, color=ft.Colors.BLUE_500),
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
            spacing=20
        ),
        padding=ft.padding.all(20),
    )

def main(page: ft.Page):
    page.session.set("play_sound", True)
    page.add(typing_game(page))


ft.app(target=main)