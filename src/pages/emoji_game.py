import flet as ft
import os

from utils import BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING

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
    
    # {
    #     "emoji": "🏔️⬆️📦🪫",
    #     "clue": "Lifting an object increases this type of stored energy.",
    #     "hint": "The higher you lift it, the more energy it gains.",
    #     "answer": "GRAVITATIONAL POTENTIAL ENERGY"
    # },
    # {
    #     "emoji": "🛰️🔁🌍",
    #     "clue": "Satellites and moons do this around planets.",
    #     "hint": "This motion balances gravity and speed.",
    #     "answer": "ORBITAL MOTION"
    # },
    # {
    #     "emoji": "🔭📏📐🪐",
    #     "clue": "These describe how planets move around the Sun.",
    #     "hint": "There are three of them and they involve ellipses, area, and time.",
    #     "answer": "KEPLER’S LAWS"
    # },
    # {
    #     "emoji": "🌞🧲🌍",
    #     "clue": "The Sun 'pulls' the Earth, keeping it in orbit.",
    #     "hint": "It's the force behind all planetary movement.",
    #     "answer": "GRAVITY"
    # },
    # {
    #     "emoji": "⏳🌕🌍🔁",
    #     "clue": "The Moon takes about 27.3 days to do this once.",
    #     "hint": "Time taken for a full orbit.",
    #     "answer": "ORBITAL PERIOD"
    # },
    # {
    #     "emoji": "🛸💨⬆️💥",
    #     "clue": "The speed needed to break free from gravity.",
    #     "hint": "If you reach this, you won’t fall back.",
    #     "answer": "ESCAPE VELOCITY"
    # },
    # {
    #     "emoji": "🌍↔️🌝🪢",
    #     "clue": "This causes tides and can lock rotation.",
    #     "hint": "Force between Earth and Moon.",
    #     "answer": "GRAVITATIONAL ATTRACTION"
    # },
    # {
    #     "emoji": "🌀🌍⚖️",
    #     "clue": "Gravity pulling inward, speed pushing outward.",
    #     "hint": "This keeps satellites from crashing or flying away.",
    #     "answer": "CENTRIPETAL FORCE"
    # },

]

import random
import string
import asyncio

def main(page: ft.Page):
    page.title = "Emoji Science Quiz"
    page.bgcolor = BG_COLOR
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.scroll = "auto"
    page.padding = 8
    page.window_min_width = 320
    page.window_min_height = 600
    
    # Remove all usage of page.session for total_score, keep only in state
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
        page.go_back() if hasattr(page, 'go_back') else page.window_close()

    appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=on_back),
        title=ft.Text("Emoji Science Quiz", weight=ft.FontWeight.W_600),
        bgcolor=BG_COLOR,
        center_title=True,
        elevation=2,
    )

    def build_ui():
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
        hint_btn = ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.LIGHT_MODE, color=TEXT_COLOR),
                    ft.Text("Hint", weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                    ft.Container(
                        content=ft.Text(str(state["hints_left"]), color=ft.Colors.RED_500, size=14),
                        margin=ft.margin.only(left=4)
                    )
                ]),
                bgcolor=PRIMARY_COLOR,
                on_click=on_hint,
                disabled=state["hints_left"] == 0,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
            ),
            padding=BUTTON_PADDING
        )
        hint_row = ft.Row([
            hint_btn
        ], alignment="center")

        # Hint text
        hint_text = ft.Text(q["hint"], color=ACCENT_COLOR, size=16, italic=True) if state["show_hint"] else ft.Text("")

        # Letter buttons
        letter_row = ft.Row([
            ft.OutlinedButton(
                c,
                width=44,
                height=44,
                on_click=lambda e, ch=c: on_letter(ch),
                # disabled=(c in state["guessed"]),
                style=ft.ButtonStyle(
                    color=TEXT_COLOR,
                    bgcolor=PRIMARY_COLOR,
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.padding.all(0),
                )
            ) for c in letters
        ], alignment="center", wrap=True, spacing=6)

        # Clue
        clue_text = ft.Text(q["clue"], color=TEXT_COLOR, size=15, italic=True, text_align="center")

        # Score
        score_text = ft.Text(f"Score: {state['score']}", color=ft.Colors.GREEN_500, size=18, weight=ft.FontWeight.W_600) if state["completed"] else ft.Text("")

        # Total score display
        total_score_text = ft.Text(f"Total Score: {state['total_score']}", color=ft.Colors.BLUE_500, size=16, weight=ft.FontWeight.W_600)

        # Navigation
        nav_row = []
        if state["showNext"]:
            nav_row = ft.Row([
                # ft.IconButton(ft.Icons.ARROW_LEFT, on_click=on_prev, disabled=state["current"] == 0, icon_color=PRIMARY_COLOR),
                ft.Text(f"{state['current']+1}/{len(QUESTIONS)}", size=15, color=TEXT_COLOR),
                ft.IconButton(ft.Icons.ARROW_RIGHT, on_click=on_next, icon_color=PRIMARY_COLOR)
            ], alignment="center")
        else:
            nav_row =  ft.Row([
                ft.Text(f"{state['current']+1}/{len(QUESTIONS)}", size=15, color=TEXT_COLOR),
            ], alignment="center")

        page.controls = [
            ft.Container(
                content=ft.Column([
                    emoji_row,
                    answer_row,
                    hint_row,
                    hint_text,
                    letter_row,
                    clue_text,
                    score_text,
                    total_score_text,
                    nav_row
                ], alignment="center", horizontal_alignment="center", spacing=10),
                padding=16,
                alignment=ft.alignment.center,
                width=400,
                bgcolor=BG_COLOR,
                border_radius=16,
                # shadow=ft.BoxShadow(blur_radius=8, color=PRIMARY_COLOR, spread_radius=0.1, offset=ft.Offset(0, 2)),
                margin=ft.margin.symmetric(vertical=8, horizontal=0),
                expand=False
            )
        ]
        page.appbar = appbar
        page.update()

    def on_letter(ch):
        if(ch in state["guessed"]):
            state["click_count"] += 1
            return
        if state["completed"]:
            state["click_count"] += 1
            return
        state["guessed"].add(ch)
        state["click_count"] += 1
        q = QUESTIONS[state["current"]]
        answer = q["answer"].upper()
        # Check if all answer letters are guessed
        if all((not c.isalpha()) or (c in state["guessed"]) for c in answer):
            state["completed"] = True
            state["score"] = calculate_score(answer, state["click_count"], state["hint_used"])
            # Only add to total_score if not already scored for this question
            if state["current"] not in state["scored_questions"]:
                state["total_score"] += state["score"]
                state["scored_questions"].add(state["current"])
                state["showNext"] = True
            build_ui()
            return
        build_ui()

    def on_hint(e):
        if state["hints_left"] > 0:
            state["hints_left"] -= 1
            state["hint_used"] += 1
            state["show_hint"] = True
            build_ui()

    def on_prev(e):
        if state["current"] > 0:
            state["current"] -= 1
            state["guessed"] = set()
            state["show_hint"] = False
            state["hints_left"] = 3  # Reset hints
            state["click_count"] = 0
            state["score"] = 0
            state["hint_used"] = 0
            state["completed"] = (state["current"] in state["scored_questions"])
            build_ui()

    def on_next(e):
        if state["current"] < len(QUESTIONS) - 1:
            state["current"] += 1
            state["guessed"] = set()
            state["show_hint"] = False
            state["hints_left"] = 3  # Reset hints
            state["click_count"] = 0
            state["score"] = 0
            state["hint_used"] = 0
            state["showNext"] = False
            state["completed"] = (state["current"] in state["scored_questions"])
            build_ui()

    build_ui()

ft.app(target=main)
