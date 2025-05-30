import flet as ft
from typing import List, Tuple, Dict, Any
from collections import deque # Added for BFS

LEVEL_CONFIGS: Dict[int, Dict[str, Any]] = {
    1: {
        "grid_size": 6,
        "start_pos": (5, 5),
        "end_pos": (0, 5),
        "walls": {
            (1, 1), (1, 2), (1, 3), (1, 4),
            (2, 1), (3, 1), (4, 1),
            (4, 2), (4, 3), (4, 4)
        },
        "message": "Level 1: Draw a path from the house to the pizza place!"
    },
    2: {
        "grid_size": 7,
        "start_pos": (6, 0),
        "end_pos": (0, 6),
        "walls": {
            (1,1), (1,5), (2,2), (2,3), (2,4), (3,1), (3,5),
            (4,1), (4,5), (5,2), (5,3), (5,4)
        },
        "message": "Level 2: A trickier route awaits!"
    },
    3: {
        "grid_size": 8,
        "start_pos": (7, 3),
        "end_pos": (0, 3),
        "walls": {
            (1,0), (1,1), (1,2), (1,4), (1,5), (1,6), (1,7),
            (2,2), (2,5), (3,0), (3,1), (3,3), (3,4), (3,6), (3,7),
            (4,3), (4,4), (5,0), (5,1), (5,2), (5,5), (5,6), (5,7),
            (6,2), (6,5)
        },
        "message": "Level 3: The final challenge!"
    },
    4: {
        "grid_size": 9,
        "start_pos": (8, 4),
        "end_pos": (0, 4),
        "walls": {
            (0,0), (0,1), (0,2), (0,3), (0,5), (0,6), (0,7), (0,8),
            (1,1), (1,3), (1,5), (1,7),
            (2,0), (2,1), (2,2), (2,4), (2,6), (2,7), (2,8),
            (3,1), (3,3), (3,5), (3,7),
            (4,0), (4,2), (4,4), (4,6), (4,8),
            (5,1), (5,3), (5,5), (5,7),
            (6,0), (6,2), (6,4), (6,6), (6,8),
            (7,1), (7,3), (7,5), (7,7),
            (8,0), (8,1), (8,2), (8,3), (8,5), (8,6), (8,7), (8,8)
        },
        "message": "Level 4: The Maze Expands!"
    },
    5: {
        "grid_size": 10,
        "start_pos": (9, 0),
        "end_pos": (0, 9),
        "walls": {
            # Outer border walls to make it more contained
            (0,1), (0,2),
            (1,0), (1,2), (1,4), (1,6), (1,8), (1,9),
            (2,1), (2,3), (2,5), (2,7), (2,9),
            (3,0), (3,2), (3,4), (3,6), (3,8),
            (4,1), (4,3), (4,5), (4,7), (4,9),
            (5,0), (5,2), (5,4), (5,6), (5,8),
            (6,1), (6,3), (6,5), (6,7), (6,9),
            (7,0), (7,2), (7,4), (7,6), (7,8),
            (8,1), (8,3), (8,5), (8,7), (8,9),
            (9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7), (9,8),
            # Inner complex walls
            (2,2), (2,6), (3,5), (4,2), (4,8), (5,1), (5,7), (6,4), (7,3), (7,7)
        },
        "message": "Level 5: The Ultimate Pizza Quest!"
    }
}
MAX_LEVELS = len(LEVEL_CONFIGS)

class PizzaMazeGame(ft.Container):
    def __init__(self, page: ft.Page, level: int = 1):
        super().__init__()
        self.page = page
        self.current_level = level
        self.current_path: List[Tuple[int, int]] = []
        self.is_drawing = False
        
        # Scoring
        self.total_score = self.page.session.get("total_score") if self.page.session.contains_key("total_score") else 0
        
        self._load_level_config()

        # UI elements that need to be referenced
        self.level_text = ft.Text(size=16, color=ft.Colors.GREY_800)
        self.score_text = ft.Text(f"Total Score: {self.total_score}", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_700)
        self.clear_button = ft.ElevatedButton(
            "Clear Path",
            on_click=self.clear_path,
            bgcolor=ft.Colors.GREY_500
        )
        self.check_button = ft.ElevatedButton(
            "Check Path",
            on_click=self.check_path,
            bgcolor=ft.Colors.GREY_500
        )
        self.next_level_button = ft.ElevatedButton(
            "Next Level",
            on_click=self.go_to_next_level,
            bgcolor=ft.Colors.GREEN_700,
            color=ft.Colors.WHITE,
            visible=False  # Initially hidden
        )
        self.game_grid_column = ft.Column(spacing=2) # To hold the grid rows

        self.content = self.build()

    def _load_level_config(self):
        if self.current_level > MAX_LEVELS:
            # Handle game completion or invalid level
            self.grid_size = 0 # Or some default/error state
            self.walls = set()
            self.start_pos = (-1, -1)
            self.end_pos = (-1, -1)
            self.level_message = "All levels completed!"
            return

        config = LEVEL_CONFIGS[self.current_level]
        self.grid_size = config["grid_size"]
        self.start_pos = config["start_pos"]
        self.end_pos = config["end_pos"]
        self.walls = config["walls"]
        self.level_message = config["message"]
        
        # Reset game state for the new level
        self.current_path = []
        self.is_drawing = False


    def build_game_grid(self):
        self.game_grid_column.controls = [
            ft.Row(
                spacing=2,
                controls=[self.create_cell(row, col) for col in range(self.grid_size)]
            ) for row in range(self.grid_size)
        ]
        return self.game_grid_column

    def build(self):
        self.level_text.value = self.level_message
        self.game_grid_container = ft.Container(
            content=self.build_game_grid(),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10
        )

        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    f"Pizza Delivery Maze - Level {self.current_level}",
                    size=24,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_800
                ),
                self.score_text, # Display the score
                self.game_grid_container,
                self.level_text,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.clear_button,
                        self.check_button,
                    ]
                ),
                self.next_level_button # Add the next level button here
            ]
        )

    def create_cell(self, row: int, col: int) -> ft.Container:
        if (row, col) in self.walls:
            bgcolor = ft.Colors.GREY_700
        elif (row, col) == self.start_pos:
            bgcolor = ft.Colors.GREEN_500
        elif (row, col) == self.end_pos:
            bgcolor = ft.Colors.RED_500
        else:
            bgcolor = ft.Colors.WHITE

        return ft.Container(
            width=25,
            height=25,
            bgcolor=bgcolor,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=4,
            data=f"{row},{col}",
            on_hover=self.cell_hover, 
            on_click=self.cell_click
        )

    def cell_hover(self, e: ft.HoverEvent):
        # Path drawing on hover is removed. 
        # This can be used for other visual feedback, like highlighting.
        pass

    def cell_click(self, e: ft.ControlEvent):
        row, col = map(int, e.control.data.split(","))

        if not self.is_drawing:
            # If not currently drawing, only a click on the start position can initiate drawing.
            if (row, col) == self.start_pos:
                self.is_drawing = True
                self.current_path = [(row, col)]  # Start the path
                e.control.bgcolor = ft.Colors.GREEN_ACCENT  # Indicate start position clicked
                e.control.update()
            return  # If not drawing and not clicking start, do nothing further.

        # If self.is_drawing is True:
        if self.is_valid_move(row, col):
            self.add_to_path(row, col)
            # Mark the cell as part of the path if it's not the start or end cell.
            if (row, col) != self.start_pos and (row, col) != self.end_pos:
                e.control.bgcolor = ft.Colors.LIGHT_BLUE_ACCENT_200  # Changed path color
                e.control.update()

            # If the path has reached the end position, stop drawing.
            if (row, col) == self.end_pos:
                self.is_drawing = False
                e.control.bgcolor = ft.Colors.RED_ACCENT  # Indicate end position clicked
                e.control.update()
        else:
            # Log invalid moves for debugging purposes
            print(f"Invalid move: ({row}, {col})")

    def is_valid_move(self, row: int, col: int) -> bool:
        if not self.current_path or (row, col) in self.walls:
            return False
        
        last_row, last_col = self.current_path[-1]
        # Allow movement to adjacent cells (horizontally, vertically, or diagonally)
        return (abs(row - last_row) <= 1 and abs(col - last_col) <= 1) and \
               (row != last_row or col != last_col) and \
               (row, col) not in self.current_path

    def add_to_path(self, row: int, col: int):
        self.current_path.append((row, col))

    def clear_path(self, e: ft.ControlEvent):
        # Reset for the current level
        self._load_level_config() # Reload config to reset start/end/walls if they were modified
        
        # Rebuild the grid visually
        self.game_grid_container.content = self.build_game_grid()
        
        # Reset button states
        self.next_level_button.visible = False
        self.check_button.disabled = False
        self.clear_button.disabled = False
        
        self.page.update()
       
    # Helper method to get valid neighbors for BFS
    def get_neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the current cell itself
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.grid_size and \
                   0 <= nc < self.grid_size and \
                   (nr, nc) not in self.walls:
                    neighbors.append((nr, nc))
        return neighbors

    # BFS to find the length of the shortest path
    def bfs_shortest_path_length(self) -> float:
        if not self.start_pos or not self.end_pos or self.start_pos == (-1,-1): # Check for invalid start_pos
            return float('inf')
        
        # Check if start or end positions are themselves walls
        if self.start_pos in self.walls or self.end_pos in self.walls:
            return float('inf')

        queue = deque([(self.start_pos, 1)])  # (position, current_path_length)
        visited = {self.start_pos}

        while queue:
            (r, c), length = queue.popleft()

            if (r, c) == self.end_pos:
                return length  # Length is the number of cells in the path

            for nr, nc in self.get_neighbors(r, c):
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), length + 1))
        
        return float('inf')  # No path found if the queue is exhausted

    def check_path(self, e: ft.ControlEvent):
        page_to_update = self.page # Use self.page
        level_score = 0 # Initialize score for the current level

        if not self.current_path:
            self.show_message("Please draw a path first!", ft.Colors.RED_500, page_to_update)
            return

        if self.current_path[-1] != self.end_pos:
            self.show_message("Path must reach the pizza place!", ft.Colors.RED_500, page_to_update)
            return

        user_path_length = len(self.current_path)
        shortest_length = self.bfs_shortest_path_length()

        success = False
        message = ""
        message_color = ft.Colors.BLACK

        if shortest_length == float('inf'):
            message = f"Path drawn ({user_path_length} steps), but maze seems unsolvable by standard paths! You get 2 points."
            message_color = ft.Colors.ORANGE_500
            level_score = 2 
            success = True # Consider this a success for progression
        elif user_path_length == shortest_length:
            message = f"Great job! Shortest path! ({user_path_length} steps). +5 points!"
            message_color = ft.Colors.GREEN_500
            level_score = 5
            success = True
        elif user_path_length == shortest_length + 1:
            message = f"Good path! ({user_path_length} steps). Almost the shortest. +4 points!"
            message_color = ft.Colors.LIGHT_GREEN_700 # A slightly different green
            level_score = 4
            success = True
        elif user_path_length > shortest_length + 1:
            message = f"Path is correct ({user_path_length} steps), but not the shortest ({shortest_length} steps). +2 points."
            message_color = ft.Colors.AMBER_700
            level_score = 2
            success = True # Allow progression
        else: 
            message = f"Path ({user_path_length} steps) is shorter than BFS shortest ({shortest_length} steps)? Anomaly! +2 points for finding a way!"
            message_color = ft.Colors.RED_ACCENT
            level_score = 2 # Award points for this unusual case
            success = True # Allow progression

        self.show_message(message, message_color, page_to_update)

        if success:
            self.total_score += level_score
            self.page.session.set("total_score", self.total_score)
            self.score_text.value = f"Total Score: {self.total_score}"
            
            if self.current_level < MAX_LEVELS:
                self.next_level_button.visible = True
            else:
                final_message = f"Congratulations! All levels completed! Final Score: {self.total_score}"
                self.show_message(final_message, ft.Colors.GREEN_500, page_to_update)
            self.check_button.disabled = True 
            self.clear_button.disabled = True 
        
        page_to_update.update()

    def show_message(self, message: str, color: str, page: ft.Page):
        # Use a SnackBar to show the message
        # Ensure 'page' is the correct Page instance.
        if page:
            page.open(ft.SnackBar(ft.Text(message, color=color), open=True)) # Added color and open=True
            # page.update() # SnackBar updates itself, page.update() might not be needed here unless other things changed

    def go_to_next_level(self, e: ft.ControlEvent):
        if self.current_level < MAX_LEVELS:
            self.current_level += 1
            self._load_level_config() # Load new level's settings

            # Update UI elements for the new level
            self.level_text.value = self.level_message
            # Find the main title Text control and update it.
            # Assuming the title is the first control in the main Column.
            if self.content.controls and isinstance(self.content.controls[0], ft.Text):
                self.content.controls[0].value = f"Pizza Delivery Maze - Level {self.current_level}"

            self.game_grid_container.content = self.build_game_grid() # Rebuild the grid

            self.next_level_button.visible = False
            self.check_button.disabled = False
            self.clear_button.disabled = False
            
            self.page.update()
        else:
            # This case should ideally be handled after check_path shows the final message
            self.show_message("You've already completed all levels!", ft.Colors.BLUE_500, self.page)
            self.next_level_button.visible = False # Hide if somehow still visible
            self.page.update()


def main(page: ft.Page):
    page.title = "Pizza Delivery Maze"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLUE_50
    page.padding = 20
    page.window_width = 500  # Adjusted for potentially larger grids
    page.window_height = 750 # Adjusted for potentially larger grids
    page.window_resizable = False
    
    game = PizzaMazeGame(page=page, level=1)  # Start at level 1
    page.add(game)

if __name__ == "__main__":
    ft.app(target=main)