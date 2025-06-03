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
        page.go("/references")

    def go_to_videos(e):
        page.go("/videos")

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

def references_page(page: ft.Page):
    references = [
        {
            "text": "Halliday, D., Resnick, R., & Walker, J. (2014). Fundamentals of Physics (10th ed.). Wiley.",
            "link": "https://elearn.daffodilvarsity.edu.bd/pluginfile.php/987150/mod_label/intro/fundamentals-of-physics-textbook.pdf"
        },
        {
            "text": "Fundamentals-of-Physics-Mechanics-Relativity-and-Thermodynamics-R.-Shankar-Edisi-1-2014",
            "link": "https://industri.fatek.unpatti.ac.id/wp-content/uploads/2019/03/041-Fundamentals-of-Physics-Mechanics-Relativity-and-Thermodynamics-R.-Shankar-Edisi-1-2014.pdf"
        }
    ]
    
    def create_ref_control(ref):
        return ft.Column([
            ft.Text(ref["text"], size=16, color=TEXT_COLOR, italic=False),
            ft.TextButton(
                "Visit Link",
                on_click=lambda e, url=ref["link"]: page.launch_url(url),
                style=ft.ButtonStyle(
                    color=PRIMARY_COLOR,
                )
            )
        ], spacing=4)

    ref_controls = [create_ref_control(ref) for ref in references]
    
    return ft.View(
        route="/references",
        controls=[
            ft.AppBar(
                leading=ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    on_click=lambda _: page.go("/learning_modules"),
                    icon_color=TEXT_COLOR,
                    icon_size=30
                ),
                title=ft.Text("References", size=28, weight=ft.FontWeight.W_600, color=TEXT_COLOR, italic=True),
                center_title=True,
                bgcolor=BG_COLOR,
                elevation=0
            ),
            ft.Container(
                content=ft.Column(ref_controls, spacing=16, expand=True),
                expand=True,
                alignment=ft.alignment.top_left,
                padding=ft.padding.symmetric(horizontal=20, vertical=20),
                bgcolor=BG_COLOR,
            )
        ],
        bgcolor=BG_COLOR,
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )


def videos_view(page: ft.Page):
    physics_videos = {
        "Unit 1: Reference Frames, Displacement, and Velocity": {
            "1.2: Position, Displacement, Velocity": [
                "https://youtu.be/NxAvWfs92U4?si=hTY0bNmNfxZWGMXv",
                "https://youtu.be/-Py2zI29THg?si=dz-xWefZlpFsNaUd",
                "https://youtu.be/QaU9jMHh7gE?si=68rG8qINT6kjpjxx",
                "https://youtu.be/yfnM0PNm9Q8?si=C3Ct4OuVMH8gGezG",
                "https://youtu.be/apewLkLAR-U?si=zSOp5Uz2w1CzB2U1"
            ],
            "1.3: Reference Frame Changes and Relative Motion": [
                "https://youtu.be/3yaZ7lkQPUQ?si=Qky-HjPjuZPxQ27F",
                "https://youtu.be/pdX74x3xiMk?si=Lwinn4JFWVf16hxK",
                "https://youtu.be/pygnrS75HLs?si=XDt8G1sNAY9Ab9qJ",
                "https://youtu.be/wD7C4V9smG4?si=OyS5orSlA4oIWwrr",
                "https://youtu.be/b97NEQh99kA?si=7Y0Nhl23Ka7IEqmu"
            ]
        },
        "Unit 2: Acceleration": {
            "2.1: The Law of Inertia": [
                "https://youtu.be/g550H4e5FCY?si=8bLoS-dTbb6xoeyL",
                "https://youtu.be/Fr5EMXZaujc?si=_iODXVdp26jVEOmG",
                "https://youtu.be/LQyFshgm-hU?si=6chFeng-DuM9Uhny"
            ],
            "2.2: Acceleration": [
                "https://youtu.be/P0UYC8S4kUI?si=8A2Yk_5dcqsSyPml",
                "https://youtu.be/JSPwCtIPfQw?si=m29ownVJuZYG7X3N",
                "https://youtu.be/NAobjpuboRE?si=l7hs-X9lhlW1VNeh"
            ],
            "2.3: Free Fall": [
                "https://youtu.be/6mFGzESlmxI?si=wRKxY2CFW3tS1dYn",
                "https://youtu.be/XlFhOygrDoM?si=AVVvhHpLL48ppQvR",
                "https://youtu.be/BVgemK1Y2wA?si=bs8VV1cEL0X5uqy-",
                "https://youtu.be/MIDSMgeben0?si=ezRONtzZYdztqbSv"
            ]
        },
        "Unit 3: Momentum and Inertia": {
            "3.1: Inertia": [
                "https://youtu.be/lZhjyP3-lME?si=K7JOz_pVKkycZJBB",
                "https://youtu.be/wL9XopHoevU?si=apftGPAIk3VaYaSl"
            ],
            "3.2: Momentum": [
                "https://youtu.be/F8DnNqBhUfQ?si=A_NS5AVKapHX9e7i",
                "https://youtu.be/ZU6rJQTz7FI?si=VGCyknccguzFd6Wn",
                "https://youtu.be/ZJlFKCGPTjU?si=imvd4rEb1ztexey8",
                "https://youtu.be/SP2hy3Uf0Ls?si=UYgC-aNxqSR6Ndy7"
            ],
            "3.3: Extended Systems and Center of Mass": [
                "https://youtu.be/WLoBo-enxAw?si=I8skbJWU4p5ebyGL",
                "https://youtu.be/nyJeaUe7wXM?si=DjaE1Uwo9e7W_t9x",
                "https://youtu.be/O-q-MAYpNLI?si=D5C_Rz5DiLAaffey",
                "https://youtu.be/a4KhrJJvD3w?si=cXvpqa0meq0G7356",
                "https://youtu.be/2uszSnvzBEU?si=9ILyW79bdI3ZflQv"
            ]
        },
        "Unit 4: Kinetic Energy": {
            "4.1: Kinetic Energy": [
                "https://youtu.be/WrFCHt21kVA?si=hxijKSyVxffDvFqN",
                "https://youtu.be/eVW8X_TsBzE?si=G531rBVwFseudUWO",
                "https://youtu.be/g7u6pIfUVy4?si=MDdYLO28NvMw2FIO",
                "https://youtu.be/DyaVgHGssos?si=nrBYoWa40QoAdJgq"
            ],
            "4.2: \"Convertible\" and \"Translational\" Kinetic Energy": [
                "https://youtu.be/N_qP72ugYyE?si=_16th3fyrQqg5L13",
                "https://youtu.be/MjM6fUV1Qz4?si=w6Cocp86L4RygYM8",
                "https://youtu.be/DpywKXIYLnM?si=nEPVIz8OM1BBLpFh",
                "https://youtu.be/PD9m9uLEVQY?si=Qz9oT1JutgLrYN4W",
                "https://youtu.be/bg5d5BFANVU?si=gZCJkjrR7o0SPNIy",
                "https://youtu.be/m6HhlBS5_WM?si=vJCK0fwVICE7I3HW"
            ]
        },
        "Unit 5: Interactions I - Energy": {
            "5.1: Conservative Interactions": [
                "https://youtu.be/N7DAqKuSCsk?si=LxhAWiiLKHkDA3iG",
                "https://youtu.be/OTK9JrKC6EY?si=Zp1GN0uWMylwngqO",
                "https://youtu.be/_DwG8fukuj4?si=Qd657N_XwJ7GYBec"
            ],
            "5.2: Dissipation of Energy and Thermal Energy": [
                "https://youtube.com/playlist?list=PLQ4ifcaxRmEhzHcRRqDeOA7SyzreSBKOu&si=H7ok2_8cPxfF2qof",
                "https://youtube.com/playlist?list=PLbxp2OQvwuKgmJ1DImFskp-Gpm_ilPXdY&si=CbsXPYuBVlvQhjDm",
                "https://youtu.be/-7Gl-yKF6Y4?si=y--k9ZJD9V2nwC6R",
                "https://youtu.be/egURSFBCaOU?si=gPjX6pmx90oYIwY5",
                "https://youtu.be/qlX-dah7MlU?si=_MJlXepX4ANkmPbZ"
            ],
            "5.3: Fundamental Interactions, and Other Forms of Energy": [
                "https://youtu.be/669QUJrF4u0?si=29UU5E-1R2ZiDp9X",
                "https://youtu.be/k1jaDh97Q_g?si=TQF41iw0RQ3Xhuxp",
                "https://youtu.be/wlb7ZVS2L38?si=WEw4SfgIgT0tM-HM",
                "https://youtu.be/T1xqwVvtcf8?si=Xb91zM554t3sauNF",
                "https://youtu.be/XiNx7YBnM-s?si=BBmDTbxsWcd5UAwZ",
                "https://youtu.be/jhKejoBqiYc?si=pc5Rk0oMpRlH4AnA"
            ],
            "5.4: Conservation of Energy": [
                "https://youtu.be/BcZfRSlaw7s?si=bajmNj3nbSUL3Zk6",
                "https://youtu.be/TLUZnCvuGBk?si=lh8tm_FipL3q6KJn",
                "https://youtu.be/LjijcG-IbR4?si=zVY4avYvWYlNtxq6"
            ]
        }
    }
    def create_video_button(unit, video):
        return ft.ElevatedButton(
            content=ft.Text(video, text_align=ft.TextAlign.CENTER),
            on_click=lambda e: page.launch_url(physics_videos[unit][video][0]),
            style=common_button_style,
            width=320,
            height=60
        )
    video_buttons = []
    for unit, videos in physics_videos.items():
        video_buttons.append(ft.Text(unit, size=20, weight=ft.FontWeight.W_600, color=TEXT_COLOR))
        for video in videos:
            video_buttons.append(create_video_button(unit, video))
            video_buttons.append(ft.Container(height=10))  # Spacer between buttons
    view_content = ft.Column(
        [
            ft.Text(
                "Physics Videos",
                size=32,
                weight=ft.FontWeight.W_600,
                color=TEXT_COLOR
            ),
            ft.Container(height=20),  # Spacer
            *video_buttons,  # Unpack the list of buttons
            ft.Container(height=20),  # Spacer
            ft.Text(
                "More videos are coming soon!",
                size=16,
                color=TEXT_COLOR,
                italic=True,
                text_align=ft.TextAlign.CENTER
            )
        ],
        alignment=ft.MainAxisAlignment.START,  # Align content to the start (top)
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        spacing=15,  # Spacing between elements in the main column
        scroll=ft.ScrollMode.AUTO  # Enable scrolling if content overflows
    )

    return ft.View(
        route="/videos",
        controls=[
            ft.AppBar(
                leading=ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    on_click=lambda _: page.go("/modules_details"),  # Back to modules_details
                    icon_color=TEXT_COLOR,
                    icon_size=30
                ),
                bgcolor=BG_COLOR,
                elevation=0
            ),
            ft.Container(
                content=view_content,
                expand=True,
                alignment=ft.alignment.top_center,  # Align content to top_center
                padding=ft.padding.symmetric(horizontal=20, vertical=20)  # Add padding
            )
        ],
        bgcolor=BG_COLOR,
        vertical_alignment=ft.MainAxisAlignment.START,  # Align view content to start
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

