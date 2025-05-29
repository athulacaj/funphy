import flet as ft
from .utils import get_background_image, BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING

# Sample Physics Questions - Can be expanded or loaded from an external source
physics_questions = [
    {
        "id": 1,
        "question": "According to Newton's First Law, an object will:",
        "options": [
            {"id": "A", "text": "Accelerate without force acting on it"},
            {"id": "B", "text": "Remain at rest or move with the constant velocity unless acted upon by a net force."},
            {"id": "C", "text": "Always move in a circle"},
            {"id": "D", "text": "Stop moving when a force is applied."}
        ],
        "correct": "B"
    },
    {
        "id": 2,
        "question": "The SI unit of force is:",
        "options": [
            {"id": "A", "text": "Joule"},
            {"id": "B", "text": "Watt"},
            {"id": "C", "text": "Newton"},
            {"id": "D", "text": "Pascal"}
        ],
        "correct": "C"
    },
    {
        "id": 3,
        "question": "Which of the following is a vector quantity?",
        "options": [
            {"id": "A", "text": "Speed"},
            {"id": "B", "text": "Distance"},
            {"id": "C", "text": "Mass"},
            {"id": "D", "text": "Velocity"}
        ],
        "correct": "D"
    }
    # Add more questions as needed (e.g., up to 10 as per image)
]

# Assessment state to track user progress
class AssessmentState:
    def __init__(self):
        self.user_answers = {}
        self.score = 0
        self.total_questions = len(physics_questions)
        self.current_question_index = 0

    def reset(self):
        self.current_question_index = 0
        self.user_answers = {}
        self.score = 0
        self.total_questions = len(physics_questions)

    def record_answer(self, question_id, answer_id):
        self.user_answers[question_id] = answer_id

    def calculate_score(self):
        self.score = 0
        for i in range(self.total_questions):
            if i < len(physics_questions):
                question = physics_questions[i]
                question_id = question["id"] # This is an int
                correct_answer = question["correct"] # This is a str (e.g., "B")
                
                # user_answers maps question_id (int) to the selected option_id (str, e.g., "A")
                user_answer = self.user_answers.get(question_id)
                
                if user_answer == correct_answer:
                    self.score += 1
        return self.score

    def get_level_and_feedback(self):
        if self.total_questions == 0:
            return "N/A", "No questions available for assessment.", "Please check the question set."

        percentage = (self.score / self.total_questions) * 100
        level = ""
        feedback = ""
        recommended = ""

        if percentage >= 70:
            level = "Advanced"
            feedback = "Excellent understanding of physics concepts!"
            recommended = "Explore advanced topics and challenges."
        elif percentage >= 40:
            level = "Intermediate"
            feedback = "Good grasp of fundamental concepts. Some areas need review."
            recommended = "Review specific topics and practice more problems."
        else:
            level = "Beginner"
            feedback = "Needs significant improvement in understanding basic concepts."
            recommended = "Start with foundational topics and build up knowledge gradually."
        return level, feedback, recommended

# Global instance of assessment state
assessment_state = AssessmentState()

def _create_base_view(page: ft.Page, controls: list, title: str, route_suffix: str):
    return ft.View(
        route=f"/assessment/{route_suffix}",
        controls=[
            ft.Stack([
                get_background_image(),
                ft.Container(
                    content=ft.Column(
                        controls,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                    padding=20
                )
            ])
        ],
        bgcolor=BG_COLOR
    )

def user_assessment_intro_page(page: ft.Page):
    def go_to_diagnostic(e):
        page.go("/assessment/diagnostic")

    content = [
        ft.Text(
            "User Assessment",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ACCENT_COLOR,
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Ready to became the Master of Physics?",
                        size=20,
                        weight=ft.FontWeight.W_600, 
                        color=TEXT_COLOR,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "Take our simple assessment and kick off your fun and exciting journey into the realm of \"Physica\" and became Master of Physics!",
                        size=16,
                        color=TEXT_COLOR,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        "Disclaimer: This Assessment is designed only to determine the user's/player's knowledge in Physics",
                        size=12,
                        color=TEXT_COLOR,
                        text_align=ft.TextAlign.CENTER,
                        italic=True
                    ),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(25),
            border_radius=ft.border_radius.all(15),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            width=450, 
            border=ft.border.all(2, PRIMARY_COLOR),
        ),
        ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
            icon_color=PRIMARY_COLOR,
            icon_size=35,
            tooltip="Next",
            on_click=go_to_diagnostic,
            bgcolor=ft.Colors.with_opacity(0.2, PRIMARY_COLOR),
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                padding=ft.padding.all(15),
            ),
        ),
    ]
    return _create_base_view(page, content, "User Assessment Intro", "intro")

def diagnostic_assessment_page(page: ft.Page):
    def start_assessment_proper(e):
        assessment_state.reset() 
        page.go("/assessment/question")

    content = [
        ft.Text(
            "Diagnostic Assessment",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ACCENT_COLOR,
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "This assessment will identify the user's prior knowledge, strengths, and weaknesses before engaging in the game.",
                        size=16,
                        color=TEXT_COLOR,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "It will include questions to gauge familiarity with physics concepts (e.g., vectors, motion, forces) and mathematical skills (e.g., algebra, calculus basics).",
                        size=16,
                        color=TEXT_COLOR,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(25),
            border_radius=ft.border_radius.all(15),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            width=450,
            border=ft.border.all(2, PRIMARY_COLOR),
        ),
        ft.ElevatedButton(
            text="Start Assessment",
            icon=ft.Icons.PLAY_ARROW_ROUNDED,
            on_click=start_assessment_proper,
            style=ft.ButtonStyle(
                bgcolor=PRIMARY_COLOR,
                color=TEXT_COLOR,
                padding=BUTTON_PADDING,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            height=50,
            width=250
        ),
    ]
    return _create_base_view(page, content, "Diagnostic Assessment", "diagnostic")

def physics_question_page(page: ft.Page):
    current_q_index = assessment_state.current_question_index
    
    if current_q_index >= assessment_state.total_questions:
        assessment_state.calculate_score()
        page.go("/assessment/results")
        return _create_base_view(page, [ft.Text("Loading results...")], "Redirecting", "redirect_results")

    question_data = physics_questions[current_q_index]
    
    options_group = ft.RadioGroup(content=ft.Column(spacing=10))

    option_controls = []
    for opt in question_data["options"]:
        option_controls.append(
            ft.Radio(
                value=opt["id"],
                label=f'{opt["id"]}. {opt["text"]}',
                label_style=ft.TextStyle(color=TEXT_COLOR, size=16)
            )
        )
    options_group.content.controls = option_controls

    def next_question(e):
        selected_answer = options_group.value
        if selected_answer:
            assessment_state.record_answer(question_data["id"], selected_answer)
            assessment_state.current_question_index += 1
            if assessment_state.current_question_index < assessment_state.total_questions:
                # Add a unique query parameter to help ensure the page refreshes
                page.go(f"/assessment/question?qidx={assessment_state.current_question_index}")
            else:
                assessment_state.calculate_score()
                page.go("/assessment/results")
        else:
            # Correct way to show a SnackBar
            snack_bar = ft.SnackBar(ft.Text("Please select an answer!"), open=True)
            page.overlay.append(snack_bar)
            page.update()

    title_text = f"Answer the {assessment_state.total_questions} following physics questions" if assessment_state.total_questions > 1 else "Answer the following physics question"

    content = [
        ft.Text(
            title_text,
            size=24, 
            weight=ft.FontWeight.BOLD,
            color=ACCENT_COLOR,
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        f'{question_data["id"]}. {question_data["question"]}',
                        size=18,
                        weight=ft.FontWeight.W_600, 
                        color=TEXT_COLOR,
                    ),
                    ft.Container(height=15),
                    options_group,
                ],
                spacing=10,
            ),
            padding=ft.padding.all(25),
            border_radius=ft.border_radius.all(15),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            width=500, 
            border=ft.border.all(2, PRIMARY_COLOR),
        ),
        ft.ElevatedButton(
            text="Next",
            icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
            on_click=next_question,
            style=ft.ButtonStyle(
                bgcolor=PRIMARY_COLOR,
                color=TEXT_COLOR,
                padding=BUTTON_PADDING,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            height=50,
            width=150
        ),
    ]
    return _create_base_view(page, content, f"Question {current_q_index + 1}", "question")

def assessment_results_page(page: ft.Page):
    def go_to_dashboard(e): 
        page.go("/dashboard") 

    score = assessment_state.score
    total = assessment_state.total_questions
    level, feedback, recommended = assessment_state.get_level_and_feedback()

    content = [
        ft.Text(
            "Assessment Results",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ACCENT_COLOR,
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("User's Results:", size=20, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text(f"Score: {score}/{total}", size=18, color=TEXT_COLOR),
                    ft.Text(f"Level: {level}", size=18, color=TEXT_COLOR),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text("Feedback:", size=16, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                    ft.Text(feedback, size=16, color=TEXT_COLOR, text_align=ft.TextAlign.JUSTIFY),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text("Recommended:", size=16, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                    ft.Text(recommended, size=16, color=TEXT_COLOR, text_align=ft.TextAlign.JUSTIFY),
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.START, 
            ),
            padding=ft.padding.all(25),
            border_radius=ft.border_radius.all(15),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            width=450,
            border=ft.border.all(2, PRIMARY_COLOR),
        ),
        ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED, 
            icon_color=PRIMARY_COLOR,
            icon_size=35,
            tooltip="Finish & Go to Dashboard",
            on_click=go_to_dashboard,
            bgcolor=ft.Colors.with_opacity(0.2, PRIMARY_COLOR),
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                padding=ft.padding.all(15),
            ),
        ),
    ]
    return _create_base_view(page, content, "Assessment Results", "results")

def view_handler(page: ft.Page):
    route = page.route
    # page.views.clear()
    match route:
        case "/assessment/intro":
            return user_assessment_intro_page(page)
        case "/assessment/diagnostic":
            return diagnostic_assessment_page(page)
        case "/assessment/question":
            return physics_question_page(page)
        case "/assessment/results":
            return assessment_results_page(page)
        case _:
            # Fallback to intro if route is unknown
            return user_assessment_intro_page(page)



def get_assessment_pages(page: ft.Page):
    """
    Returns the assessment view based on the current route.
    This function is used in the main.py to handle assessment routes.
    """
    return view_handler(page)

