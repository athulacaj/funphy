import flet as ft
from .db import AppDatabase

from .utils import BG_COLOR,get_background_image, PRIMARY_COLOR,ConfettiWidget, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING

# Game data: emoji, clue, hint, answer
QUESTIONS = [
    {
        "emoji": "🍎⬇️👴",
        "clue": "A falling apple helped him realize something important.",
        "hint": "It's about how all objects attract each other, no matter the distance.",
        "answer": "NEWTON'S LAW "
    },
    {
        "emoji": "🌍➡️🎯",
        "clue": "The Earth pulls objects toward its center, even if they're not touching it.",
        "hint": "Think of an invisible force map around a planet.",
        "answer": "GRAVITATIONAL FIELD"
    },
    
    {
        "emoji": "🏔️⬆️📦🪫",
        "clue": "Lifting an object increases this type of stored energy.",
        "hint": "The higher you lift it, the more energy it gains.",
        "answer": "GRAVITATIONAL POTENTIAL ENERGY"
    },
    {
        "emoji": "🛰️🔁🌍",
        "clue": "Satellites and moons do this around planets.",
        "hint": "This motion balances gravity and speed.",
        "answer": "ORBITAL MOTION"
    },
    {
        "emoji": "🔭📏📐🪐",
        "clue": "These describe how planets move around the Sun.",
        "hint": "There are three of them and they involve ellipses, area, and time.",
        "answer": "KEPLER’S LAWS"
    },
    {
        "emoji": "🌞🧲🌍",
        "clue": "The Sun 'pulls' the Earth, keeping it in orbit.",
        "hint": "It's the force behind all planetary movement.",
        "answer": "GRAVITY"
    },
    {
        "emoji": "⏳🌕🌍🔁",
        "clue": "The Moon takes about 27.3 days to do this once.",
        "hint": "Time taken for a full orbit.",
        "answer": "ORBITAL PERIOD"
    },
    {
        "emoji": "🛸💨⬆️💥",
        "clue": "The speed needed to break free from gravity.",
        "hint": "If you reach this, you won’t fall back.",
        "answer": "ESCAPE VELOCITY"
    },
    {
        "emoji": "🌍↔️🌝🪢",
        "clue": "This causes tides and can lock rotation.",
        "hint": "Force between Earth and Moon.",
        "answer": "GRAVITATIONAL ATTRACTION"
    },
    {
        "emoji": "🌀🌍⚖️",
        "clue": "Gravity pulling inward, speed pushing outward.",
        "hint": "This keeps satellites from crashing or flying away.",
        "answer": "CENTRIPETAL FORCE"
    },

]

import random
import string
import asyncio

def build_emoj_game(page: ft.Page):
    # Initialize page specific properties if not already set by main app
    page.title = "Emoji Science Quiz"
    # page.bgcolor = BG_COLOR # Comment out or remove as main.py sets this
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.scroll = "auto"
    page.padding = 8
    page.window_min_width = 320
    page.window_min_height = 600

    state = {
        "showNext": False,  # Track if next button should be shown
        "current": 0,
        "guessed": set(),
        "hints_left": 3,
        "show_hint": False,
        "click_count": 0,  # Track letter clicks
        "score": 0,        # Track score for current question
        "hint_used": 0,    # Track hints used per question
        "completed": False, # Track if question is completed
        "total_score": 0, # Track total score only in state
        "scored_questions": set(), # Track which questions have been scored
        "can_show_animation":False
    }

    def get_letter_choices(answer):
        letters = [c for c in answer if c in string.ascii_uppercase]
        extra = random.choices(string.ascii_uppercase, k=max(0, 14 - len(letters)))
        all_letters = list(set(letters + extra))
        random.shuffle(all_letters)
        return all_letters[:14]

    def calculate_score(answer, click_count, hint_used):
        base_score = 100
        l=len(set(''.join(char for char in answer if char.isalpha())))
        extra_types = max(0, click_count - l)
        score = base_score - (extra_types*10) - (hint_used * 10)
        return max(score, 0)

    # Add AppBar with back button
    def on_back(e):
        # page.go_back() if hasattr(page, 'go_back') else page.window_close()
        page.go("/dashboard") # Navigate to dashboard

    appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=on_back,),
        title=ft.Text("Emoji Science Quiz", weight=ft.FontWeight.W_600),
        bgcolor=BG_COLOR, # Defined in utils
        center_title=True,
        color=TEXT_COLOR,
        elevation=2,
    )

    def build_main_content_container():
        q = QUESTIONS[state["current"]]
        answer = q["answer"].upper()
        letters = get_letter_choices(answer)
        
        # Emoji row
        emoji_row = ft.Row([
            ft.Text(q["emoji"], size=30, color=PRIMARY_COLOR)
        ], alignment="center")

        # Answer boxes
        answer_row = ft.Row([
            ft.Container(
                content=ft.Text(
                    c if (c in state["guessed"] or not c.isalpha()) else "",
                    size=18,
                    weight=ft.FontWeight.W_600,
                    color=BG_COLOR,
                ),
                bgcolor=TEXT_COLOR if c.isalpha() else ACCENT_COLOR,
                width=36,
                height=36,
                border_radius=10,
                alignment=ft.alignment.center,
                margin=ft.margin.only(right=3, bottom=3)
            ) if c != " " else ft.Container(width=18) for c in answer
        ], alignment="center", wrap=True)

        # Hint button
        hint_btn_content = ft.Row([
            ft.Icon(ft.Icons.LIGHT_MODE, color=TEXT_COLOR),
            ft.Text("Hint", weight=ft.FontWeight.W_600, color=TEXT_COLOR),
            ft.Container(
                content=ft.Text(str(state["hints_left"]), color=ft.Colors.RED_500, size=14),
                margin=ft.margin.only(left=4)
            )
        ])
        
        hint_btn = ft.Container(
            content=ft.ElevatedButton(
                content=hint_btn_content,
                bgcolor=PRIMARY_COLOR,
                on_click=on_hint,
                disabled=state["hints_left"] == 0 or state["show_hint"], # Disable if hint shown or no hints
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
            ),
            padding=BUTTON_PADDING
        )
        hint_row = ft.Row([hint_btn], alignment="center")

        # Hint text
        hint_text_widget = ft.Text(q["hint"], color=ACCENT_COLOR, size=16, italic=True) if state["show_hint"] else ft.Text("")

        # Letter buttons
        letter_buttons = [
            ft.OutlinedButton(
                c,
                width=44,
                height=44,
                on_click=lambda e, ch=c: on_letter(ch),
                # disabled=(c in state["guessed"] and state["completed"]) or (c in state["guessed"]), # Disable if guessed, or if completed and guessed
                style=ft.ButtonStyle(
                    color=TEXT_COLOR,
                    bgcolor=PRIMARY_COLOR,
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.padding.all(0),
                )
            ) for c in letters
        ]
        letter_row = ft.Row(letter_buttons, alignment="center", wrap=True, spacing=6)

        # Clue
        clue_text_widget = ft.Text(q["clue"], color=TEXT_COLOR, size=15, italic=True, text_align="center")

        # Score
        score_text_widget = ft.Text(f"Score: {state['score']}", color=ft.Colors.GREEN_500, size=18, weight=ft.FontWeight.W_600) if state["completed"] else ft.Text("")

        # Total score display
        total_score_text_widget = ft.Text(f"Total Score: {state['total_score']}", color=ft.Colors.BLUE_500, size=16, weight=ft.FontWeight.W_600)

        # Navigation
        nav_row_content = [ft.Text(f"{state['current']+1}/{len(QUESTIONS)}", size=15, color=TEXT_COLOR)]
        if state["showNext"]:
            nav_row_content.append(ft.IconButton(ft.Icons.ARROW_RIGHT, on_click=on_next, icon_color=PRIMARY_COLOR))
        
        nav_row = ft.Row(nav_row_content, alignment="center")

        return ft.Container(
            content=ft.Column([
                emoji_row,
                answer_row,
                hint_row,
                hint_text_widget,
                letter_row,
                clue_text_widget,
                score_text_widget,
                total_score_text_widget,
                nav_row
            ], alignment="center", horizontal_alignment="center", spacing=10),
            padding=16,
            alignment=ft.alignment.center,
            width=400,
            bgcolor=BG_COLOR,
            border_radius=16,
            margin=ft.margin.symmetric(vertical=8, horizontal=0),
            expand=False
        )

    def update_view_content(can_show_animation=False):
        confetti = ConfettiWidget()
        page.confetti=confetti
        page.confetti=confetti
        if page.views:
            current_view = page.views[-1]
            current_view.controls = [
                ft.Stack([
                # Background image container
                    get_background_image(),
                    build_main_content_container(),
                    confetti
                ]),
            ]
            
            page.update()
            if(can_show_animation):
                page.confetti.animate_confetti()
 

    def save_progress():
           if state["current"] >= len(QUESTIONS) - 1:
                AppDatabase.save_self_user_data_2({"advanced_feedback":{"score": state["total_score"]}})

    def on_letter(ch):
        if (ch in state["guessed"] and state["completed"]) or (ch in state["guessed"]):
            # If the letter is already guessed and the question is completed, do nothing
            state["click_count"] += 1
            page.confetti.play_error_sound()
            return                                          
        if state["completed"]:
            # Allow clicking letters even if completed, but it won't change score or guessed set
            # state["click_count"] += 1 # Optionally count clicks after completion
            page.confetti.play_error_sound()
            return

        if ch in state["guessed"]:
            state["click_count"] += 1 # Count clicks on already guessed letters
            # No UI update needed as the letter is already shown as guessed
            page.confetti.play_error_sound()
            return
        page.confetti.play_click_sound()
        state["guessed"].add(ch)
        state["click_count"] += 1
        
        current_q_data = QUESTIONS[state["current"]]
        answer_str = current_q_data["answer"].upper()
        can_show_animation=False
        if all((not c.isalpha()) or (c in state["guessed"]) for c in answer_str):
            state["completed"] = True
            state["score"] = calculate_score(answer_str, state["click_count"], state["hint_used"])
            if state["current"] not in state["scored_questions"]:
                state["total_score"] += state["score"]
                state["scored_questions"].add(state["current"])
                state["showNext"] = True 
                can_show_animation=True
                save_progress()
        
        update_view_content(can_show_animation)

    def on_hint(e):
        if state["hints_left"] > 0 and not state["show_hint"]:
            state["hints_left"] -= 1
            state["hint_used"] += 1 
            state["show_hint"] = True
            update_view_content()

    def on_prev(e): # Assuming on_prev might be used later
        if state["current"] > 0:
            state["current"] -= 1
            state["guessed"] = set()
            state["show_hint"] = False
            state["click_count"] = 0
            state["score"] = 0
            state["hint_used"] = 0
            state["completed"] = (state["current"] in state["scored_questions"])
            state["showNext"] = state["completed"] # Show next if already completed
            update_view_content()

    def on_next(e):
        if state["current"] < len(QUESTIONS) - 1:
            state["current"] += 1
            state["guessed"] = set()
            state["show_hint"] = False
            # state["hints_left"] remains, it's a global pool
            state["click_count"] = 0
            state["score"] = 0
            state["hint_used"] = 0
            state["showNext"] = False 
            state["completed"] = (state["current"] in state["scored_questions"])
            state["can_show_animation"]=True
            if state["completed"]: # If the next question was already completed, showNext should be true
                 state["showNext"] = True
            update_view_content()
        # else: 
        #     page.go("/dashboard")

    initial_content = build_main_content_container()
    confetti = ConfettiWidget()
    page.confetti=confetti
    return ft.View(
        route="/emoji_game",
        controls=[
                ft.Stack([
                # Background image container
                    get_background_image(),
                    initial_content,
                    confetti
                ]),
            ],
        appbar=appbar,
        bgcolor=BG_COLOR # Set bgcolor for the View, consistent with previous version
    )
