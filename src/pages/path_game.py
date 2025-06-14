import flet as ft
import math # Add this import
from typing import List, Tuple, Set, Dict # Assuming these are used or will be
from collections import deque # Added for BFS
from .db import AppDatabase

from .utils import BG_COLOR,get_background_image,ConfettiWidget, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING

# Placeholder for level configurations - ensure these are properly defined

# LEVEL_CONFIGS: Dict[int, Dict[str, Any]] = {
#     1: {
#         "grid_size": 6,
#         "start_pos": (5, 5),
#         "end_pos": (0, 5),
#         "walls": {
#             (1, 1), (1, 2), (1, 3), (1, 4),
#             (2, 1), (3, 1), (4, 1),
#             (4, 2), (4, 3), (4, 4)
#         },
#         "message": "Level 1: Draw a path from the house to the pizza place!"
#     },
#     2: {
#         "grid_size": 7,
#         "start_pos": (6, 0),
#         "end_pos": (0, 6),
#         "walls": {
#             (1,1), (1,5), (2,2), (2,3), (2,4), (3,1), (3,5),
#             (4,1), (4,5), (5,2), (5,3), (5,4)
#         },
#         "message": "Level 2: A trickier route awaits!"
#     },
#     3: {
#         "grid_size": 8,
#         "start_pos": (7, 3),
#         "end_pos": (0, 3),
#         "walls": {
#             (1,0), (1,1), (1,2), (1,4), (1,5), (1,6), (1,7),
#             (2,2), (2,5), (3,0), (3,1), (3,3), (3,4), (3,6), (3,7),
#             (4,3), (4,4), (5,0), (5,1), (5,2), (5,5), (5,6), (5,7),
#             (6,2), (6,5)
#         },
#         "message": "Level 3: The final challenge!"
#     },
#     4: {
#         "grid_size": 9,
#         "start_pos": (8, 4),
#         "end_pos": (0, 4),
#         "walls": {
#             (0,0), (0,1), (0,2), (0,3), (0,5), (0,6), (0,7), (0,8),
#             (1,1), (1,3), (1,5), (1,7),
#             (2,0), (2,1), (2,2), (2,4), (2,6), (2,7), (2,8),
#             (3,1), (3,3), (3,5), (3,7),
#             (4,0), (4,2), (4,4), (4,6), (4,8),
#             (5,1), (5,3), (5,5), (5,7),
#             (6,0), (6,2), (6,4), (6,6), (6,8),
#             (7,1), (7,3), (7,5), (7,7),
#             (8,0), (8,1), (8,2), (8,3), (8,5), (8,6), (8,7), (8,8)
#         },
#         "message": "Level 4: The Maze Expands!"
#     },
#     5: {
#         "grid_size": 10,
#         "start_pos": (9, 0),
#         "end_pos": (0, 9),
#         "walls": {
#             # Outer border walls to make it more contained
#             (0,1), (0,2),
#             (1,0), (1,2), (1,4), (1,6), (1,8), (1,9),
#             (2,1), (2,3), (2,5), (2,7), (2,9),
#             (3,0), (3,2), (3,4), (3,6), (3,8),
#             (4,1), (4,3), (4,5), (4,7), (4,9),
#             (5,0), (5,2), (5,4), (5,6), (5,8),
#             (6,1), (6,3), (6,5), (6,7), (6,9),
#             (7,0), (7,2), (7,4), (7,6), (7,8),
#             (8,1), (8,3), (8,5), (8,7), (8,9),
#             (9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7), (9,8),
#             # Inner complex walls
#             (2,2), (2,6), (3,5), (4,2), (4,8), (5,1), (5,7), (6,4), (7,3), (7,7)
#         },
#         "message": "Level 5: The Ultimate Pizza Quest!"
#     }

# }

LEVEL_CONFIGS: Dict[int, Dict] = {
    1: {
        "grid_size": 5,
        "start_pos": (4, 0),
        "end_pos": (0, 4),
        "walls": set([(1,1), (1,2), (1,3), (2,1), (3,1), (3,2), (3,3)]),
        "message": "Level 1: Draw a path from the house to the pizza place!"
    },
    2: {
        "grid_size": 6,
        "start_pos": (5, 0),
        "end_pos": (0, 5),
        "walls": set([(1,1), (1,2), (2,2), (2,4), (3,1), (3,4), (4,1), (4,3)]),
        "message": "Level 2: Another tricky delivery!"
    },
    3:{
        "grid_size": 8,
        "start_pos": (7, 3),
        "end_pos": (0, 3),
        "walls": set([
            (1,0), (1,1), (1,2), (1,4), (1,5), (1,6), (1,7),
            (2,2), (2,5), (3,0), (3,1), (3,3), (3,4), (3,6), (3,7),
            (4,3), (4,4), (5,0), (5,1), (5,2), (5,5), (5,6), (5,7),
            (6,2), (6,5)
        ]),
        "message": "Level 3: The final challenge!"
    },
    4: {
        "grid_size": 9,
        "start_pos": (8, 4),
        "end_pos": (0, 4),
        "walls": set([
            (0,0), (0,1), (0,2), (0,3), (0,5), (0,6), (0,7), (0,8),
            (1,1), (1,3), (1,5), (1,7),
            (2,0), (2,1), (2,2), (2,4), (2,6), (2,7), (2,8),
            (3,1), (3,3), (3,5), (3,7),
            (4,0), (4,2), (4,4), (4,6), (4,8),
            (5,1), (5,3), (5,5), (5,7),
            (6,0), (6,2), (6,4), (6,6), (6,8),
            (7,1), (7,3), (7,5), (7,7),
            (8,0), (8,1), (8,2), (8,3), (8,5), (8,6), (8,7), (8,8)
        ]),
        "message": "Level 4: The Maze Expands!"
    },
    5: {
        "grid_size": 10,
        "start_pos": (9, 0),
        "end_pos": (0, 9),
        "walls":set([
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
        ]),
        "message": "Level 5: The Ultimate Pizza Quest!"
    }

}

MAX_LEVELS = len(LEVEL_CONFIGS)  # Automatically determine max levels from configs

class PizzaMazeGame(ft.Container):
    def __init__(self, page: ft.Page, level: int = 1):
        super().__init__()
        self.page = page
        self.current_level = level
        self.current_path: List[Tuple[int, int]] = []
        self.is_drawing = False
        
        # self.total_score = self.page.session.get("total_score") if self.page.session.contains_key("total_score") else 0
        self.total_score = 0
        self._load_level_config()

        self.title_text = ft.Text( # Added for dynamic title
            f"Level {self.current_level}",
            size=24,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.WHITE
        )
        self.level_text = ft.Text(size=16, color=ft.Colors.WHITE)
        self.score_text = ft.Text(f"Total Score: {self.total_score}", size=18, weight=ft.FontWeight.W_600, color=ACCENT_COLOR)
        self.clear_button = ft.ElevatedButton(
            "Clear Path",
            on_click=self.clear_path,
            bgcolor=PRIMARY_COLOR,
            color=TEXT_COLOR
        )
        self.check_button = ft.ElevatedButton(
            "Check Path",
            on_click=self.check_path,
            bgcolor=PRIMARY_COLOR,
            color=TEXT_COLOR
        )
        self.next_level_button = ft.ElevatedButton(
            "Next Level",
            on_click=self.go_to_next_level,
            bgcolor=PRIMARY_COLOR,
            color=TEXT_COLOR,
            visible=False  # Initially hidden
        )
        self.game_grid_column = ft.Column(spacing=2) # To hold the grid rows

        self.info_row = ft.Row([
            ft.Icon(ft.Icons.INFO, color=ft.Colors.BLUE_500),
            ft.Text("Click the green cell to start marking. \nReach the red cell to finish.", color=ft.Colors.WHITE)
        ], alignment=ft.MainAxisAlignment.CENTER)

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
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[self.create_cell(row, col) for col in range(self.grid_size)]
            ) for row in range(self.grid_size)
        ]
        return self.game_grid_column

    def build(self):
        self.level_text.value = self.level_message
        self.game_grid_container = ft.Container(
                content=self.build_game_grid(),
                padding=20,
                bgcolor=ft.Colors.TRANSPARENT,  # Use BG_COLOR for grid container
                border_radius=10,
                alignment=ft.alignment.center,  # Center the grid in the container
            
            )
        

        return ft.Container(
            bgcolor=ft.Colors.TRANSPARENT,  # Use BG_COLOR for main container
            padding=ft.padding.all(16),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.title_text,
                    self.info_row,
                    self.score_text, 
                    self.game_grid_container,
                    self.level_text,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            self.clear_button,
                            self.check_button,
                        ]
                    ),
                    self.next_level_button
                ]
            )
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
            width=28,
            height=28,
            bgcolor=bgcolor,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=4,
            data=f"{row},{col}",
            on_hover=self.cell_hover, 
            on_click=self.cell_click
        )

    def get_cell_control(self, row: int, col: int) -> ft.Container | None:
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            if self.game_grid_column and \
               row < len(self.game_grid_column.controls) and \
               col < len(self.game_grid_column.controls[row].controls):
                return self.game_grid_column.controls[row].controls[col]
        return None

    def update_cell_appearance(self, row: int, col: int, is_path: bool):
        cell = self.get_cell_control(row, col)
        if not cell: return

        original_bgcolor = cell.bgcolor 

        if (row, col) == self.start_pos:
            cell.bgcolor = ft.Colors.GREEN_ACCENT_200 if is_path else ft.Colors.GREEN_500
        elif (row, col) == self.end_pos:
            cell.bgcolor = ft.Colors.RED_ACCENT_200 if is_path else ft.Colors.RED_500
        elif (row, col) in self.walls:
            cell.bgcolor = ft.Colors.GREY_700 
        elif is_path:
            cell.bgcolor = ft.Colors.LIGHT_BLUE_ACCENT_200
        else: 
            cell.bgcolor = ft.Colors.WHITE
        
        if cell.bgcolor != original_bgcolor:
            cell.update()

    def cell_hover(self, e: ft.HoverEvent):
        pass

    def cell_click(self, e: ft.ControlEvent):
        row, col = map(int, e.control.data.split(","))

        if (row, col) in self.walls:
            self.page.play_error_sound()
            return
        self.page.play_click_sound()

        if not self.is_drawing:
            if (row, col) == self.start_pos:
                self.is_drawing = True
                self.current_path = [(row, col)]
                self.update_cell_appearance(row, col, is_path=True)
            return

        if self.is_valid_move(row, col):
            self.add_to_path(row, col)
            self.update_cell_appearance(row, col, is_path=True)

            if (row, col) == self.end_pos:
                self.is_drawing = False
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

    def calculate_current_path_distance(self) -> float:
        if not self.current_path or len(self.current_path) < 2:
            return 0.0

        total_distance = 0.0
        for i in range(len(self.current_path) - 1):
            p1_row, p1_col = self.current_path[i]
            p2_row, p2_col = self.current_path[i+1]

            delta_row = abs(p1_row - p2_row)
            delta_col = abs(p1_col - p2_col)

            if delta_row == 1 and delta_col == 1:  # Diagonal move
                total_distance += math.sqrt(2)
            elif (delta_row == 1 and delta_col == 0) or \
                 (delta_row == 0 and delta_col == 1):  # Cardinal move
                total_distance += 1.0
        return total_distance

    def enable_game_interactions(self, enabled: bool):
        for r_idx in range(self.grid_size):
            for c_idx in range(self.grid_size):
                cell = self.get_cell_control(r_idx, c_idx)
                if cell:
                    if enabled:
                        cell.on_click = self.cell_click
                        cell.on_hover = self.cell_hover 
                    else:
                        cell.on_click = None
                        cell.on_hover = None
        
        self.check_button.disabled = not enabled
        self.clear_button.disabled = not enabled
        # Next level button visibility is handled separately

    def clear_path(self, e: ft.ControlEvent = None):
        path_to_clear = list(self.current_path)
        self.current_path = []
        self.is_drawing = False 

        for r, c in path_to_clear:
            self.update_cell_appearance(r, c, is_path=False) 
        
        # Ensure start/end cells are correctly reset if they were part of the path
        if self.start_pos != (-1,-1) : self.update_cell_appearance(self.start_pos[0], self.start_pos[1], is_path=False)
        if self.end_pos != (-1,-1) : self.update_cell_appearance(self.end_pos[0], self.end_pos[1], is_path=False)


        self.enable_game_interactions(True)
        self.next_level_button.visible = False
        
        self.check_button.update()
        self.clear_button.update()
        self.next_level_button.update()
        self.page.update()

    async def check_path(self, e: ft.ControlEvent = None):
        if not self.current_path:
            # Correct way to show SnackBar
            self.page.overlay.append(ft.SnackBar(ft.Text("Draw a path first!", color=ft.Colors.WHITE), open=True))
            self.page.update()
            return

        path_starts_correctly = self.current_path[0] == self.start_pos
        path_ends_correctly = self.current_path[-1] == self.end_pos

        if not path_starts_correctly:
            # Correct way to show SnackBar
            self.page.overlay.append(ft.SnackBar(ft.Text("Path must start at the green square!", color=ft.Colors.WHITE), open=True))
            self.page.update()
            return

        if not path_ends_correctly:
            # Correct way to show SnackBar
            self.page.overlay.append(ft.SnackBar(ft.Text("Path must end at the red square!", color=ft.Colors.WHITE), open=True))
            self.page.update()
            return
        distance = self.calculate_current_path_distance()
        shortest_distance = self.bfs_shortest_path_distance()
        if distance == 0 or shortest_distance == float('inf'):
            level_score = 0
        else:
            # Score: 100 if optimal, less if longer, min 0
            level_score = max(0, int(100 * (shortest_distance / distance)))
        if(level_score > 100):
            level_score = 100
        elif(level_score!=100 and level_score > 20):
            level_score -=20
        self.total_score += level_score
        self.page.session.set("total_score", self.total_score)
        self.score_text.value = f"Total Score: {self.total_score}"
        
        # Correct way to show SnackBar
        self.page.overlay.append(
            ft.SnackBar(
                ft.Text(f"Path complete! Distance: {distance:.2f} (Optimal: {shortest_distance:.2f}). You earned {level_score} points.", color=ft.Colors.WHITE),
                open=True
            )
        )
        # self.page.update() is called at the end of this method already

        self.enable_game_interactions(False)

        if self.current_level < MAX_LEVELS:
            self.page.confetti.animate_confetti()
            self.page.play_audio1()
            self.next_level_button.visible = True
            self.next_level_button.update()  # Ensure update is called immediately after visibility change
        else:
            self.page.confetti.animate_confetti() 
            self.page.play_audio1()
            self.level_text.value = "Congratulations! All levels completed!"
            self.next_level_button.visible = False
            self.level_text.update()
            self.next_level_button.update()
            await AppDatabase.save_self_user_data({"intermediate_feedback":{"score": self.total_score}})

        self.score_text.update()
        self.check_button.update()
        self.clear_button.update()
        self.page.update()
        
    def go_to_next_level(self, e: ft.ControlEvent):
        if self.current_level < MAX_LEVELS:
            self.current_level += 1
            self._load_level_config() 

            self.title_text.value = f"Level {self.current_level}"
            self.level_text.value = self.level_message
            
            self.game_grid_container.content = self.build_game_grid()
            
            self.enable_game_interactions(True)
            self.next_level_button.visible = False

            self.title_text.update()
            self.level_text.update()
            self.update()  # Add this line to update the main control
            self.check_button.update()
            self.clear_button.update()
            self.next_level_button.update()
            self.page.update()
        else:
            # Correct way to show SnackBar
            self.page.overlay.append(ft.SnackBar(ft.Text("You've completed all levels!", color=ft.Colors.WHITE), open=True))
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

    # BFS to find the minimal possible path distance (considering diagonals)
    def bfs_shortest_path_distance(self) -> float:
        if not self.start_pos or not self.end_pos or self.start_pos == (-1,-1):
            return float('inf')
        if self.start_pos in self.walls or self.end_pos in self.walls:
            return float('inf')

        queue = deque([(self.start_pos, 0.0)])  # (position, current_path_distance)
        visited = {self.start_pos}

        while queue:
            (r, c), dist = queue.popleft()
            if (r, c) == self.end_pos:
                return dist
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and (nr, nc) not in self.walls:
                        if (nr, nc) not in visited:
                            visited.add((nr, nc))
                            if abs(dr) == 1 and abs(dc) == 1:
                                queue.append(((nr, nc), dist + math.sqrt(2)))
                            else:
                                queue.append(((nr, nc), dist + 1.0))
        return float('inf')

# def addPathGame(page: ft.Page):
#     def route_change(e):
#         route = page.route
#         if route == "/path_game":
#             page.views.append(ft.View("/path_game", [PizzaMazeGame(page)]))
#         # ...add other routes as needed...
#         # else: ...
#     page.on_route_change = route_change
#     page.go(page.route)

def path_game(page: ft.Page):
    def go_back(e):
        page.go("/dashboard")
    confetti = ConfettiWidget()
    page.confetti=confetti
    return ft.View("/path_game", [
         ft.Stack([
                # Background image container
                    get_background_image(),
                    PizzaMazeGame(page),
                    confetti
        ],expand=True, alignment=ft.alignment.center),
    ],
    appbar=ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back, tooltip="Back"),
        title=ft.Text("Path Maze Game"),
        color=TEXT_COLOR,
        bgcolor=BG_COLOR, # Defined in utils
        # bgcolor=ft.Colors.BLACK12 # Adjust color as needed
    ),
    bgcolor=BG_COLOR,
    padding=0
)