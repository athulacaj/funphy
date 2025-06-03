import flet as ft
from .utils import PRIMARY_COLOR, TEXT_COLOR, BUTTON_PADDING, BG_COLOR
from .db import AppDatabase


# Common button style
common_button_style = ft.ButtonStyle(
    bgcolor=PRIMARY_COLOR,
    color=TEXT_COLOR,
    padding=BUTTON_PADDING,
    shape=ft.RoundedRectangleBorder(radius=10),
)

def learning_modules_view(page: ft.Page):
    def go_to_modules_details(e):
        page.go("/modules_details")

    def go_to_references(e):
        page.show_snack_bar(ft.SnackBar(ft.Text("References: Content coming soon!"), open=True))

    def go_to_videos(e):
        page.show_snack_bar(ft.SnackBar(ft.Text("Videos: Content coming soon!"), open=True))

    view_content = ft.Column(
        [
            ft.Text(
                "Learning Modules",
                size=32,
                weight=ft.FontWeight.W_600,
                color=TEXT_COLOR
            ),
            ft.Container(height=30),  # Spacer
            ft.ElevatedButton(
                "Modules",
                on_click=go_to_modules_details,
                style=common_button_style,
                width=280, # Increased width for better text fit
                height=50
            ),
            ft.Container(height=15),  # Spacer
            ft.ElevatedButton(
                "References",
                on_click=go_to_references,
                style=common_button_style,
                width=280,
                height=50
            ),
            ft.Container(height=15),  # Spacer
            ft.ElevatedButton(
                "Videos",
                on_click=go_to_videos,
                style=common_button_style,
                width=280,
                height=50
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        spacing=20 # Added spacing between elements in column
    )

    return ft.View(
        route="/learning_modules",
        controls=[
            ft.AppBar(
                leading=ft.IconButton(
                    ft.Icons.CHEVRON_LEFT, # Changed to CHEVRON_LEFT as per image style
                    on_click=lambda _: page.go("/dashboard"), # Assumes back goes to dashboard
                    icon_color=TEXT_COLOR,
                    icon_size=30
                ),
                bgcolor=BG_COLOR,
                elevation=0
            ),
            ft.Container(
                content=view_content,
                expand=True,
                alignment=ft.alignment.center, # Ensure content column is centered
                padding=ft.padding.symmetric(horizontal=20) # Add some horizontal padding
            )
        ],
        bgcolor=BG_COLOR,
        vertical_alignment=ft.MainAxisAlignment.CENTER, # Center view content vertically
        horizontal_alignment=ft.CrossAxisAlignment.CENTER # Center view content horizontally
    )

def modules_details_view(page: ft.Page):
    def go_to_lessons(e):
        page.go("/lessons") # Changed to navigate to /lessons

    def go_to_notes(e):
        page.go("/notes")

    view_content = ft.Column(
        [
            ft.Text(
                "Modules",
                size=32,
                weight=ft.FontWeight.W_600,
                color=TEXT_COLOR
            ),
            ft.Container(height=30),  # Spacer
            ft.ElevatedButton(
                "Lessons",
                on_click=go_to_lessons,
                style=common_button_style,
                width=280,
                height=50
            ),
            ft.Container(height=15),  # Spacer
            ft.ElevatedButton(
                "Notes",
                on_click=go_to_notes,
                style=common_button_style,
                width=280,
                height=50
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        spacing=20
    )

    return ft.View(
        route="/modules_details",
        controls=[
            ft.AppBar(
                leading=ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    on_click=lambda _: page.go("/learning_modules"), # Back to parent page
                    icon_color=TEXT_COLOR,
                    icon_size=30
                ),
                bgcolor=BG_COLOR,
                elevation=0
            ),
             ft.Container(
                content=view_content,
                expand=True,
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(horizontal=20)
            )
        ],
        bgcolor=BG_COLOR,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

def lessons_view(page: ft.Page):
    # Handler for individual unit clicks
    def on_unit_click(e, ukey, udata):
        page.launch_url(udata["html_asset"])  # Open the HTML asset in a new tab

    lesson_units = {
        "unit1": {
            "title": "Reference Frames, Displacement, and Velocity",
            "html_asset": "https://funphy.netlify.app/unit1",
        },
        "unit2": {"title": "Acceleration","html_asset": "https://funphy.netlify.app/unit2"},
        "unit3": {"title": "Momentum and Inertia", "html_asset": "https://funphy.netlify.app/unit3"},
        "unit4": {"title": "Kinetic Energy", "html_asset": "https://funphy.netlify.app/unit4"},
        "unit5": {"title": "Interaction 1 Energy", "html_asset": "https://funphy.netlify.app/unit5"},
    }

    unit_buttons = []
    for unit_key, unit_data in lesson_units.items():
        unit_title = unit_data["title"]
        display_text = f"{unit_key}: {unit_title}"
        unit_buttons.append(
            ft.ElevatedButton(
                content=ft.Text(display_text, text_align=ft.TextAlign.CENTER), # Center align text
                # Pass unit_key and unit_data to the handler
                on_click=lambda e, k=unit_key, d=unit_data: on_unit_click(e, k, d),
                style=common_button_style,
                width=320,  # Adjusted width for longer text
                height=60 # Adjusted height for multi-line text
            )
        )
        unit_buttons.append(ft.Container(height=10)) # Spacer between buttons

    view_content = ft.Column(
        [
            ft.Text(
                "Lessons",
                size=32,
                weight=ft.FontWeight.W_600,
                color=TEXT_COLOR
            ),
            ft.Container(height=20),  # Spacer
            *unit_buttons, # Unpack the list of buttons
            ft.Container(height=20), # Spacer
            ft.Text(
                "More units are coming soon!",
                size=16,
                color=TEXT_COLOR,
                italic=True,
                text_align=ft.TextAlign.CENTER
            )
        ],
        alignment=ft.MainAxisAlignment.START, # Align content to the start (top)
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        spacing=15, # Spacing between elements in the main column
        scroll=ft.ScrollMode.AUTO # Enable scrolling if content overflows
    )

    return ft.View(
        route="/lessons",
        controls=[
            ft.AppBar(
                leading=ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    on_click=lambda _: page.go("/modules_details"), # Back to modules_details
                    icon_color=TEXT_COLOR,
                    icon_size=30
                ),
                bgcolor=BG_COLOR,
                elevation=0
            ),
            ft.Container(
                content=view_content,
                expand=True,
                alignment=ft.alignment.top_center, # Align content to top_center
                padding=ft.padding.symmetric(horizontal=20, vertical=20) # Add padding
            )
        ],
        bgcolor=BG_COLOR,
        vertical_alignment=ft.MainAxisAlignment.START, # Align view content to start
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

def notes_page(page: ft.Page):
    # Use page-level state for notes
    user = page.session.get("user") 
    page.notes = user.get("notes", []) if user else []
    def refresh_notes():
        notes_list.controls.clear()
        for note in page.notes:
            notes_list.controls.append(
                ft.Container(
                    content=ft.Text(note["title"], size=16, color=TEXT_COLOR),
                    bgcolor=BG_COLOR,
                    border=ft.border.all(1, PRIMARY_COLOR),
                    border_radius=20,
                    padding=ft.padding.symmetric(vertical=8, horizontal=16),
                    margin=ft.margin.only(bottom=8),
                    alignment=ft.alignment.center_left,
                    expand=False,
                    on_click=lambda e, n=note: show_note_dialog(n)
                )
            )
        notes_count.value = f"{len(page.notes)} notes"
        page.update()

    def on_add_note(e):
        title_field = ft.TextField(label="Title", width=400, color=TEXT_COLOR, bgcolor=BG_COLOR)
        content_field = ft.TextField(label="Content", multiline=True, min_lines=3, max_lines=5, width=300, color=TEXT_COLOR, bgcolor=BG_COLOR)
        def add_note_action(ev):
            page.notes.append({"title": title_field.value, "content": content_field.value})
            AppDatabase.save_self_user_data_2({"notes":page.notes})  # Save notes to database
            page.close(dialog)
            refresh_notes()
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add Note", size=20, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
            content=ft.Column([
                title_field,
                content_field
            ], spacing=10),
            actions=[
                ft.TextButton("Add", on_click=add_note_action),
                ft.TextButton("Cancel", on_click=lambda ev: page.close(dialog)),
            ],
            bgcolor=BG_COLOR,
        )
        page.open(dialog)

    def on_search(e):
        page.show_snack_bar(ft.SnackBar(ft.Text("Search: Feature coming soon!"), open=True))

    def show_note_dialog(note):
        dialog = ft.AlertDialog(
            title=ft.Text(note["title"], size=20, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
            content=ft.Text(note["content"], size=16, color=TEXT_COLOR),
            actions=[ft.TextButton("Close", on_click=lambda e: page.close(dialog))],
            bgcolor=BG_COLOR,
        )
        page.open(dialog)

    notes_count = ft.Text(f"{len(page.notes)} notes", size=14, color=TEXT_COLOR, italic=True)
    notes_list = ft.Column([], spacing=0, expand=True)
    refresh_notes()

    fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        bgcolor=PRIMARY_COLOR,
        on_click=on_add_note,
        shape=ft.CircleBorder(),
        mini=False
    )

    return ft.View(
        route="/notes",
        controls=[
            ft.AppBar(
                leading=ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    on_click=lambda _: page.go("/modules_details"),
                    icon_color=TEXT_COLOR,
                    icon_size=30
                ),
                title=ft.Text("My notes", size=28, weight=ft.FontWeight.W_600, color=TEXT_COLOR, italic=True),
                center_title=True,
                bgcolor=BG_COLOR,
                elevation=0,
                actions=[
                    # ft.IconButton(
                    #     icon=ft.Icons.SEARCH,
                    #     icon_color=TEXT_COLOR,
                    #     on_click=on_search
                    # ),
                    # ft.PopupMenuButton(items=[]),
                ],
            ),
            ft.Container(
                content=ft.Column([
                    notes_count,
                    notes_list,
                ], expand=True, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                bgcolor=BG_COLOR,
            ),
            ft.Container(
                content=fab,
                alignment=ft.alignment.bottom_right,
                padding=ft.padding.only(right=16, bottom=16),
                expand=False
            )
        ],
        bgcolor=BG_COLOR,
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

