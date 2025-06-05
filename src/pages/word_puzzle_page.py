import flet as ft
from .utils import BG_COLOR,APPBAR_FONT_SIZE,get_background_image,ConfettiWidget, TEXT_COLOR, PRIMARY_COLOR, ACCENT_COLOR
from .db import AppDatabase
# play_click_sound,play_error_sound
def play_click_sound():
    pass
def play_error_sound():
    pass
def play_audio1():
    pass

# Word search puzzle data based on the image
WORD_GRID = [
    ['R', 'P', 'H', 'D', 'I', 'Y', 'H', 'K', 'H', 'C', 'M', 'N', 'D'],
    ['E', 'G', 'T', 'Z', 'N', 'T', 'I', 'Q', 'R', 'O', 'O', "R", 'I'],
    ['F', 'H', 'U', 'I', 'E', 'I', 'N', 'H', 'O', 'I', 'M', "O", 'S'],
    ['E', 'G', 'G', 'S', 'R', 'C', 'T', 'G', 'T', 'R', 'E', "T", 'P'],
    ['R', 'U', 'R', 'P', 'T', 'O', 'E', 'A', 'C', 'H', 'N', "C", 'L'],
    ['E', 'O', 'B', 'O', 'I', 'L', 'R', 'L', 'E', 'N', 'T', "E", 'A'],
    ['N', 'T', 'U', 'A', 'A', 'E', 'A', 'H', 'V', 'R', 'U', "V", 'C'],
    ['C', 'O', 'R', 'C', 'L', 'V', 'C', 'A', 'T', 'S', 'M', "R", 'E'],
    ['E', 'U', 'T', 'E', 'R', 'O', 'T', 'V', 'H', 'L', 'P', 'D', 'M'],
    ['F', 'E', 'C', 'N', 'A', 'T', 'S', 'I', 'D', 'B', 'R', 'V', 'E'],
    ['B', 'C', 'U', 'E', 'I', 'S', 'O', 'A', 'N', 'C', 'E', 'M', 'N'],
    ['A', 'K', 'C', 'O', 'U', 'E', 'N', 'E', 'R', 'G', 'Y', 'N', 'T']
]

# WORDS_TO_FIND = [
#     "REFERENCE",
# ]
WORDS_TO_FIND = [
    "ACCELERATION", "REFERENCE", "DISPLACEMENT", "VELOCITY", 
    "MOMENTUM", "INERTIA", "DISTANCE", 
    "VECTOR", "ENERGY"
]

WORD_DESCRIPTIONS = {
    "ACCELERATION": "The rate at which an object's velocity changes with time. It is a vector quantity, having both magnitude and direction.",
    "REFERENCE": "A reference point or frame is a fixed place or object used to determine the position or motion of other objects.",
    "DISPLACEMENT": "The shortest straight-line distance from an object's initial position to its final position, along with the direction.",
    "VELOCITY": "The speed of an object in a particular direction. It is a vector quantity, indicating both how fast and in which direction.",
    "MOMENTUM": "The product of an object's mass and its velocity. It is a measure of how much motion an object has.",
    "INERTIA": "The tendency of an object to resist changes in its state of motion. Objects with more mass have greater inertia.",
    "DISTANCE": "The total length of the path traveled by an object, regardless of direction. It is a scalar quantity.",
    "VECTOR": "A quantity that has both magnitude and direction, such as velocity, acceleration, or force.",
    "ENERGY": "The capacity to do work. It exists in various forms such as kinetic, potential, thermal, and more."
}

# Define colors for found words
FOUND_WORD_CELL_COLOR = ft.Colors.with_opacity(0.8, ft.Colors.GREEN_ACCENT_700)
FOUND_WORD_LIST_COLOR = ft.Colors.GREEN_ACCENT_700


class WordSearchGame:
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_cells = [] 
        self.selected_cell_containers = [] 
        self.selection_direction = None 
        self.word_list_text_widgets = {}
        self.answered_words = []
        self.found_word_cells_coords = set() # Keep track of cells in found words

        self.cell_dimension = 35
        self.spacing_val = 2
        
        self.current_level = 1
        self.level_configs = {
            1: {"display_cols": 6, "display_rows": 9, "cumulative_words_to_reach_next": 3},
            2: {"display_cols": 12, "display_rows": 9, "cumulative_words_to_reach_next": 5}, # 3 (L1) + 2 (L2)
            3: {"display_cols": len(WORD_GRID[0]), "display_rows": len(WORD_GRID), "cumulative_words_to_reach_next": len(WORDS_TO_FIND)} # All words for full grid
        }
        
        self.score = 2000 # Initialize score
        self.max_score = 2000 # Max possible score

        self.all_cell_containers_map = {} # To store all cell ft.Container objects
        self.grid_view = ft.GridView( # Initialize GridView here
            expand=False, # Will be sized by content
            child_aspect_ratio=1.0,
            spacing=self.spacing_val,
            run_spacing=self.spacing_val,
            expand_loose= True, # Allow GridView to expand based on content,
            auto_scroll=False
        )
        self.level_status_text = ft.Text(value="", color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

        self.ui_root = self._build_ui()

    def _build_ui(self):
        # Create all cell containers ONCE and store them
        for r_idx, row_val in enumerate(WORD_GRID):
            for c_idx, letter in enumerate(row_val):
                cell = ft.Container(
                    content=ft.Text(letter, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                    alignment=ft.alignment.center,
                    width=self.cell_dimension,
                    height=self.cell_dimension,
                    bgcolor=PRIMARY_COLOR,
                    border_radius=ft.border_radius.all(5),
                    data=(r_idx, c_idx), # Store original full grid coordinates
                    on_click=self.cell_clicked,
                )
                self.all_cell_containers_map[(r_idx, c_idx)] = cell
        
        # Populate grid_view for the initial level
        self._populate_grid_view_for_current_level(initial_call=True)

        word_controls = []
        for word in WORDS_TO_FIND:
            text_control = ft.Text(word, color=TEXT_COLOR, size=16)
            word_controls.append(text_control)
            self.word_list_text_widgets[word] = text_control

        self.words_list_view = ft.Column(
            controls=word_controls,
            spacing=5,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
        
        # title_text = ft.Text(
        #     "PHYSICS WORDSEARCH",
        #     size=28,
        #     weight=ft.FontWeight.BOLD,
        #     color=ACCENT_COLOR,
        #     text_align=ft.TextAlign.CENTER
        # )
        
        game_layout = ft.Column(
            [
                ft.Column([self.grid_view], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=2),
                ft.Container(
                    ft.Column([
                        ft.Text("WORDS TO FIND:", weight=ft.FontWeight.BOLD, color=TEXT_COLOR, size=18),
                        self.level_status_text, # Added level status text
                        ft.Divider(height=5, color=ft.Colors.TRANSPARENT), # Optional: add some spacing
                        self.words_list_view
                        ], 
                        alignment=ft.MainAxisAlignment.START, 
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        expand=1,
                    ),
                    padding=ft.padding.all(22),
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            # vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=20
        )
        self._update_level_status_display(initial_call=True) # Initial call to set status, no update
        return ft.Column( 
            [
                # title_text,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                game_layout,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )


    def _update_level_status_display(self, initial_call=False):
        total_words_for_level_up = self.level_configs[self.current_level]["cumulative_words_to_reach_next"]
        words_found_count = len(self.answered_words)
        words_needed = total_words_for_level_up - words_found_count

        if self.current_level < 3:
            if words_needed > 0:
                self.level_status_text.value = f"Level {self.current_level}: Find {words_needed} more to advance."
            else: # Should ideally not happen if level up logic is correct, but as a fallback
                self.level_status_text.value = f"Level {self.current_level}: Advancing soon..."
        elif self.current_level == 3:
            remaining_overall = len(WORDS_TO_FIND) - words_found_count
            if remaining_overall > 0:
                self.level_status_text.value = f"Final Level: Find all remaning words!"
            else:
                self.level_status_text.value = f"All words found! Congratulations! Score: {self.score}/{self.max_score}"
                AppDatabase.save_self_user_data_2({"beginner_feedback":{"score": self.score}})

        
        if len(self.answered_words) == len(WORDS_TO_FIND):
             self.level_status_text.value = f"All words found! Congratulations! Score: {self.score}/{self.max_score}"
             AppDatabase.save_self_user_data_2({"beginner_feedback":{"score": self.score}})

        if not initial_call:
            self.level_status_text.update()

    def _populate_grid_view_for_current_level(self, initial_call=False):
        level_conf = self.level_configs[self.current_level]
        display_cols = level_conf["display_cols"]
        display_rows = level_conf["display_rows"]

        self.grid_view.controls.clear()
        self.grid_view.runs_count = display_cols
        
        # Calculate and set fixed width and height for the GridView based on current level
        grid_width = (display_cols * self.cell_dimension) + ((display_cols - 1) * self.spacing_val if display_cols > 0 else 0)
        grid_height = (display_rows * self.cell_dimension) + ((display_rows - 1) * self.spacing_val if display_rows > 0 else 0)
        self.grid_view.width = grid_width
        self.grid_view.height = grid_height

        for r in range(display_rows):
            for c in range(display_cols):
                # Ensure (r,c) is within the bounds of the full WORD_GRID
                if r < len(WORD_GRID) and c < len(WORD_GRID[0]):
                    cell_container = self.all_cell_containers_map.get((r, c))
                    if cell_container: # Should always exist if (r,c) is valid
                        self.grid_view.controls.append(cell_container)
        
        if not initial_call:
            self.grid_view.update()
        # Consider self.page.update() if layout changes significantly
        # For now, let's see if grid_view.update() is enough.
        # If the overall game_layout needs to resize, self.ui_root.update() or self.page.update() might be needed


    def _reset_ui_for_current_selection(self):
        for container in self.selected_cell_containers:
            if container.on_click is not None: 
                # Check if the cell is part of an already found word
                if container.data in self.found_word_cells_coords:
                    container.bgcolor = FOUND_WORD_CELL_COLOR
                else:
                    container.bgcolor = PRIMARY_COLOR
                container.update()

    def _check_for_word(self):
        if len(self.selected_cells) < 2:
            return False

        current_selection_str = "".join([WORD_GRID[r][c] for r, c in self.selected_cells])
        current_selection_str_upper = current_selection_str.upper()
        
        found_word_details = None

        for word_to_find in WORDS_TO_FIND:
            if word_to_find not in self.answered_words:
                if word_to_find == current_selection_str_upper:
                    found_word_details = (word_to_find, False)
                    break
                reversed_selection_str_upper = current_selection_str_upper[::-1]
                if word_to_find == reversed_selection_str_upper:
                    found_word_details = (word_to_find, True)
                    break
        
        if found_word_details:
            actual_found_word = found_word_details[0]
            self.page.confetti.animate_confetti()
            play_audio1()
            self.answered_words.append(actual_found_word)

            # Show Snackbar with word description
            word_description = WORD_DESCRIPTIONS.get(actual_found_word, "No description available.")
            snack_bar = ft.SnackBar(
                ft.Text(f"{actual_found_word}: {word_description}", color=TEXT_COLOR),
                open=True,
                # bgcolor=ACCENT_COLOR,
                duration=15000 # milliseconds
            )
            self.page.overlay.append(snack_bar)
            self.page.update()

            for cell_container in self.selected_cell_containers:
                cell_container.bgcolor = FOUND_WORD_CELL_COLOR
                self.found_word_cells_coords.add(cell_container.data) # Add to set of found word cells
                # cell_container.on_click = None # Allow re-selection for common cells in different words
                cell_container.update()

            if actual_found_word in self.word_list_text_widgets:
                text_widget = self.word_list_text_widgets[actual_found_word]
                text_widget.spans = [
                    ft.TextSpan(
                        actual_found_word,
                        ft.TextStyle(
                            decoration=ft.TextDecoration.LINE_THROUGH,
                            color=FOUND_WORD_LIST_COLOR 
                        )
                    )
                ]
                text_widget.update()

            self.selected_cells.clear()
            self.selected_cell_containers.clear()
            self.selection_direction = None
            
            # Check for game completion
            if len(self.answered_words) == len(WORDS_TO_FIND):
                print("Congratulations! All words found!")
                self._update_level_status_display() # Update status for completion
                # You can add a dialog or banner here:
                # self.page.dialog = ft.AlertDialog(title=ft.Text("You found all words!"), open=True)
                # self.page.update()
                return True # Word found, game complete

            # If game not complete, check for level up
            if self.current_level < 3: 
                cumulative_words_needed_for_this_level_progression = self.level_configs[self.current_level]["cumulative_words_to_reach_next"]
                
                if len(self.answered_words) >= cumulative_words_needed_for_this_level_progression:
                    self.current_level += 1
                    print(f"Level up to {self.current_level}!")
                    self._populate_grid_view_for_current_level() 
            
            self._update_level_status_display() # Update status after finding a word / leveling up
            return True # Word found
        
        # If no word was found, but selection changed, still update status if needed (e.g. if a word was deselected)
        # However, current logic only calls _check_for_word on valid selections or new selections.
        # If you want to update on every click, this call might need to be in cell_clicked too.
        # For now, let's assume it's fine here.
        # self._update_level_status_display() # Potentially call here too if needed on non-word-finding clicks
        return False

    def cell_clicked(self, e: ft.ControlEvent):
        if e.control.on_click is None:
            self.page.confetti.play_error_sound()
            return
        # self.page.confetti.play_click_sound()
        r, c = e.control.data
        clicked_cell_container = e.control 
        current_click_coords = (r, c)
        play_cilck_sound=True

        if clicked_cell_container in self.selected_cell_containers:
            if clicked_cell_container == self.selected_cell_containers[-1]:
                self.selected_cells.pop()
                play_cilck_sound=False # Don't play sound on deselection
                popped_container = self.selected_cell_containers.pop()
                # Check if the popped cell is part of an already found word
                if popped_container.data in self.found_word_cells_coords:
                    # If it was part of a found word, keep its "found" color
                    # This case might not be strictly necessary if found cells are non-interactive
                    # but good for robustness if they can be part of a new selection attempt.
                    pass # Color is already FOUND_WORD_CELL_COLOR
                else:
                    # Reset to primary color if not part of an already found word
                    popped_container.bgcolor = PRIMARY_COLOR 
                popped_container.update()
                
                if len(self.selected_cells) < 2:
                    self.selection_direction = None # Reset direction if selection is too short
            else:
                # Clicked on a selected cell that is NOT the last one in the selection
                # This means the current selection chain is broken.
                self.score = max(100, self.score - 100) # Decrease score
                print(f"Invalid selection reset. Score: {self.score}") # For debugging
                self._reset_ui_for_current_selection() 
                self.selected_cells.clear()
                play_cilck_sound=False
                self.selected_cell_containers.clear() # Clear selection
                self.selection_direction = None
            # self._check_for_word() # Check if the modified selection forms a word (might be needed if deselecting forms a word)
            # For now, let's assume word check happens after adding cells or on explicit action.
            # Consider if _update_level_status_display should be called here too.
            return

        can_extend_selection = False
        if not self.selected_cells:
            can_extend_selection = True
            self.selection_direction = None 
        elif len(self.selected_cells) == 1:
            prev_r, prev_c = self.selected_cells[0]
            dr = r - prev_r
            dc = c - prev_c
            if abs(dr) <= 1 and abs(dc) <= 1 and (dr, dc) != (0,0): 
                can_extend_selection = True
                self.selection_direction = (dr, dc)
        else: 
            last_r, last_c = self.selected_cells[-1]
            if self.selection_direction: 
                expected_dr, expected_dc = self.selection_direction
                if r == last_r + expected_dr and c == last_c + expected_dc:
                    can_extend_selection = True
            
        if can_extend_selection:
            self.selected_cells.append(current_click_coords)
            self.selected_cell_containers.append(clicked_cell_container)
            clicked_cell_container.bgcolor = ACCENT_COLOR
            clicked_cell_container.update()
        else:
            self._reset_ui_for_current_selection() 
            play_cilck_sound=False # Don't play sound on invalid selection
            self.selected_cells.clear()
            self.selected_cell_containers.clear()
            self.score = max(100, self.score - 100) # Decrease score
            print(f"Invalid selection reset. Score: {self.score}") # For debugging
            self.selected_cells.append(current_click_coords)
            self.selected_cell_containers.append(clicked_cell_container)
            clicked_cell_container.bgcolor = ACCENT_COLOR
            clicked_cell_container.update()
            self.selection_direction = None 
        if play_cilck_sound:
            # self.page.confetti.play_click_sound()
            play_click_sound()
        else:
            play_error_sound()
        if self.selected_cells: 
            self._check_for_word()
        
    def get_ui(self):
        return self.ui_root

def word_puzzle_page(page: ft.Page):
    game_manager = WordSearchGame(page)

    content = ft.Column(
        controls=[
            game_manager.get_ui() 
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    # Check if page.add() or page.update() is needed after initial setup
    # For a View, usually setting its controls is enough.
    # If WordSearchGame modifies things that affect the whole page layout significantly,
    # then game_manager might need to call self.page.update() internally.


    # Add AppBar with back button
    def on_back(e):
        page.go("/dashboard") # Navigate to dashboard



    appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=on_back),
        title=ft.Text("PHYSICS WORDSEARCH",size=APPBAR_FONT_SIZE),
        bgcolor=BG_COLOR, # Defined in utils
        center_title=True,
        # elevation=2,
        color=TEXT_COLOR,

    )
    confetti = ConfettiWidget()
    page.confetti=confetti
    return ft.View(
        "/word_puzzle",
        [
            ft.Stack([
                # Background image container
                get_background_image(),
                ft.Container(
                    content=content,
                    expand=True,
                    padding=ft.padding.all(8),
                    alignment=ft.alignment.center,
                    # bgcolor=ft.Colors.with_opacity(0.6, BG_COLOR), # Assuming BG_COLOR is defined
                    # bgcolor=ft.Colors.with_opacity(0.6, "0x2E2E2E") # Example, replace with your BG_COLOR
                ),
                confetti
            ])
        ],
        bgcolor=BG_COLOR, # Assuming BG_COLOR is defined
        appbar=appbar,
        padding=0,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO, # Enable scrolling if content overflows
    )
