import flet as ft
from .utils import PRIMARY_COLOR, TEXT_COLOR, BUTTON_PADDING, BG_COLOR

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
        page.show_snack_bar(ft.SnackBar(ft.Text("Notes: Content coming soon!"), open=True))

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
        page.session.set("current_unit_key", ukey)  # Save unit_key to session
        page.session.set("current_unit_data", udata)  # Save unit_data to session
        page.go("/lesson_content") # Navigate to the new view

    lesson_units = {
        "Unit 1": {"title": "Reference Frames, Displacement, and Velocity","pdf":"https://example.com/unit1.pdf"},
        "Unit 2": {"title": "Acceleration"},
        "Unit 3": {"title": "Momentum and Inertia"},
        "Unit 4": {"title": "Kinetic Energy"},
        "Unit 5": {"title": "Interaction 1 Energy"}
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

def lesson_content_view(page: ft.Page):
    # current_unit_key = page.session.get("current_unit_key") # Retrieve if needed elsewhere
    current_lesson_data = page.session.get("current_unit_data")

    if not current_lesson_data:
        # Fallback if session data is missing
        return ft.View(
            route="/lesson_content",
            controls=[
                ft.AppBar(
                    title=ft.Text("Error", color=TEXT_COLOR),
                    leading=ft.IconButton(
                        ft.Icons.CHEVRON_LEFT,
                        on_click=lambda _: page.go("/lessons"),
                        icon_color=TEXT_COLOR,
                        icon_size=30
                    ),
                    bgcolor=BG_COLOR,
                    elevation=0
                ),
                ft.Container(
                    content=ft.Text("Lesson content not found. Please go back to lessons.", color=TEXT_COLOR),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ],
            bgcolor=BG_COLOR,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    unit_title = current_lesson_data.get("title", "Lesson Content")
    pdf_url = current_lesson_data.get("pdf")

    content_items = []
    if pdf_url:
        content_items.append(ft.Text(f"PDF URL: {pdf_url}", color=TEXT_COLOR, size=16))
        content_items.append(ft.Container(height=10)) # Spacer
        content_items.append(
            ft.ElevatedButton(
                "Open PDF in browser",
                on_click=lambda _: page.launch_url(pdf_url),
                style=common_button_style,
                width=280,
                height=50
            )
        )
    else:
        content_items.append(
            ft.Text(
                "No PDF available for this unit. Content will be available soon.",
                color=TEXT_COLOR,
                size=16,
                italic=True,
                text_align=ft.TextAlign.CENTER
            )
        )

    view_content = ft.Column(
        content_items,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        expand=True
    )

    return ft.View(
        route="/lesson_content",
        controls=[
            ft.AppBar(
                title=ft.Text(unit_title, color=TEXT_COLOR, weight=ft.FontWeight.W_600),
                leading=ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    on_click=lambda _: page.go("/lessons"), # Back to lessons view
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
                padding=ft.padding.symmetric(horizontal=20, vertical=20)
            )
        ],
        bgcolor=BG_COLOR,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
