import flet as ft
import flet.canvas as cv
import collections

# Maze configurations for 5 levels
# 0 = path, 1 = wall, 'S' = start, 'E' = end
MAZES = [
    # Level 1 (10x10) - Multiple simple paths
    [
        [1, 1, 1, 1, 1, 1, 1, 'E', 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 'S', 1, 1]
    ],
    # Level 2 (12x12) - Multiple paths, more complex (corrected)
    [
        [1, 1, 1, 1, 1, 1, 'E', 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 'S', 1, 1, 1, 1, 1]
    ],
    # Level 3 (15x15) - More complex with multiple distinct paths
    [
        [1, 1, 1, 1, 1, 1, 1, 'E', 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 'S', 1, 1, 1, 1, 1, 1, 1]
    ],
    # Level 4 (18x18) - Significantly more complex with multiple winding paths (corrected)
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 'E', 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 'S', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    # Level 5 (20x20) - Most challenging with multiple complex routes
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 'E', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 'S', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
]

MAX_CANVAS_DIMENSION = 600

class MazeGame(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.alignment = ft.alignment.center
        self.current_level = 0
        self.score = 0
        self.maze_grid = []
        self.start_pos = None
        self.end_pos = None
        self.cell_size = 0
        self.maze_rows = 0
        self.maze_cols = 0
        self.user_path = []
        self.is_drawing = False
        self.shortest_path_length = 0

        self.user_path_paint = ft.Paint(
            stroke_cap=ft.StrokeCap.ROUND,
            stroke_join=ft.StrokeJoin.ROUND,
            style=ft.PaintingStyle.STROKE,
            color=ft.Colors.GREEN_500,
            # stroke_width will be set in _update_maze_dimensions
        )
        self.user_path_shape = cv.Path(elements=[], paint=self.user_path_paint)

        self.shortest_path_paint = ft.Paint(
            stroke_cap=ft.StrokeCap.ROUND,
            stroke_join=ft.StrokeJoin.ROUND,
            style=ft.PaintingStyle.STROKE,
            color=ft.Colors.RED_500,
            stroke_dash_pattern=[5, 5],
            # stroke_width will be set in _update_maze_dimensions
        )
        self.shortest_path_shape = cv.Path(elements=[], paint=self.shortest_path_paint)

        self.message_text = ft.Text("Draw a path from the house to the pizza place!", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_900)
        self.score_level_text = ft.Text("Score: 0 | Level: 1", size=18, weight=ft.FontWeight.BOLD)

        self.canvas = cv.Canvas(
            shapes=[],  # Initialize with an empty list of shapes
            # Event handlers like on_pan_start are assigned after initialization
            expand=True,
            # bgcolor and border_radius are not constructor arguments for cv.Canvas
        )
        # Assign pan event handlers as attributes
        self.canvas.on_pan_start = self.start_drawing
        self.canvas.on_pan_update = self.draw
        self.canvas.on_pan_end = self.stop_drawing
        # Assign other properties as attributes
        self.canvas.bgcolor = ft.Colors.BLUE_50
        self.canvas.border_radius = ft.border_radius.all(12)

        self.controls = [
            ft.Text("🍕 Pizza Delivery Maze Challenge 🏠", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800),
            ft.Container(
                content=self.canvas,
                width=MAX_CANVAS_DIMENSION,
                height=MAX_CANVAS_DIMENSION,
                border=ft.border.all(2, ft.Colors.BLUE_600),
                border_radius=ft.border_radius.all(12),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.BLUE_GREY_300,
                    offset=ft.Offset(0, 0),
                    blur_style=ft.ShadowBlurStyle.OUTER,
                ),
            ),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Clear Path",
                        on_click=self.clear_path,
                        style=ft.ButtonStyle(
                            bgcolor={"": ft.Colors.BLUE_GREY_600},
                            color={"": ft.Colors.WHITE},
                            shape=ft.RoundedRectangleBorder(radius=12),
                            shadow_color=ft.Colors.BLUE_GREY_300,
                        )
                    ),
                    ft.ElevatedButton(
                        "Check Path",
                        on_click=self.check_path,
                        style=ft.ButtonStyle(
                            bgcolor={"": ft.Colors.BLUE_600},
                            color={"": ft.Colors.WHITE},
                            shape=ft.RoundedRectangleBorder(radius=12),
                            shadow_color=ft.Colors.BLUE_300,
                        )
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=16
            ),
            ft.Container(
                content=self.message_text,
                padding=ft.padding.symmetric(vertical=16, horizontal=24),
                bgcolor=ft.Colors.BLUE_100,
                border_radius=ft.border_radius.all(12),
                expand=True,
                alignment=ft.alignment.center,
            ),
            self.score_level_text,
        ]
        # Set the content to a Column containing all controls so the UI is visible
        self.content = ft.Column(self.controls, expand=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def did_mount(self):
        self.start_game()

    def _update_maze_dimensions(self):
        self.maze_grid = MAZES[self.current_level]
        self.maze_rows = len(self.maze_grid)
        self.maze_cols = len(self.maze_grid[0])
        self.cell_size = min(
            MAX_CANVAS_DIMENSION // self.maze_cols,
            MAX_CANVAS_DIMENSION // self.maze_rows
        )
        # Adjust canvas size to fit the maze perfectly with calculated cell_size
        self.canvas.width = self.maze_cols * self.cell_size
        self.canvas.height = self.maze_rows * self.cell_size

        # Update paint properties that depend on cell_size
        self.user_path_paint.stroke_width = self.cell_size / 4
        self.shortest_path_paint.stroke_width = self.cell_size / 6

        # Find start and end positions for the current maze
        self.start_pos = None
        self.end_pos = None
        for r in range(self.maze_rows):
            for c in range(self.maze_cols):
                if self.maze_grid[r][c] == 'S':
                    self.start_pos = {'row': r, 'col': c}
                elif self.maze_grid[r][c] == 'E':
                    self.end_pos = {'row': r, 'col': c}

    def draw_maze(self):
        self.canvas.shapes.clear()  # Use shapes attribute

        wall_paint = ft.Paint(color=ft.Colors.BLUE_GREY_700, style=ft.PaintingStyle.FILL)
        path_cell_paint = ft.Paint(color=ft.Colors.BLUE_50, style=ft.PaintingStyle.FILL)

        for r_idx, row_data in enumerate(self.maze_grid):
            for c_idx, cell_type in enumerate(row_data):
                x = c_idx * self.cell_size
                y = r_idx * self.cell_size

                # Draw wall or path cell
                if cell_type == 1:  # Wall
                    self.canvas.shapes.append(
                        cv.Rect(x=x, y=y, width=self.cell_size, height=self.cell_size, paint=wall_paint)
                    )
                else:  # Path cell (0, 'S', or 'E')
                    self.canvas.shapes.append(
                        cv.Rect(x=x, y=y, width=self.cell_size, height=self.cell_size, paint=path_cell_paint)
                    )

                # Draw start/end icons
                icon_text = None
                if cell_type == 'S':
                    icon_text = "🏠"
                elif cell_type == 'E':
                    icon_text = "🍕"

                if icon_text:
                    text_size = self.cell_size * 0.7
                    text_x = x + self.cell_size / 2
                    text_y = y + self.cell_size / 2  # For cv.Text, y is baseline. Adjust if needed for vertical center.
                    self.canvas.shapes.append(
                        cv.Text(
                            x=text_x,
                            y=text_y,
                            text=icon_text,
                            text_align=ft.TextAlign.CENTER,
                        )
                    )
        
        # Always add path shapes to the canvas shapes list
        self.canvas.shapes.append(self.user_path_shape)
        self.canvas.shapes.append(self.shortest_path_shape)
            
        if hasattr(self, 'page') and self.page:
            self.page.update()
    def draw_user_path(self):
        if not self.user_path:
            self.user_path_shape.elements.clear()
            if hasattr(self, 'page') and self.page:
                self.page.update()
            return

        new_path_elements = []
        start_x = self.user_path[0]['col'] * self.cell_size + self.cell_size / 2
        start_y = self.user_path[0]['row'] * self.cell_size + self.cell_size / 2
        new_path_elements.append(cv.Path.MoveTo(start_x, start_y))

        for i in range(1, len(self.user_path)):
            x = self.user_path[i]['col'] * self.cell_size + self.cell_size / 2
            y = self.user_path[i]['row'] * self.cell_size + self.cell_size / 2
            new_path_elements.append(cv.Path.LineTo(x, y))

        self.user_path_shape.elements = new_path_elements
        if hasattr(self, 'page') and self.page:
            self.page.update()

    def get_grid_coords(self, x, y):
        col = int(x // self.cell_size)
        row = int(y // self.cell_size)
        return {'row': row, 'col': col}

    def is_valid_cell(self, row, col):
        return 0 <= row < self.maze_rows and \
               0 <= col < self.maze_cols and \
               self.maze_grid[row][col] != 1

    def add_point_to_path(self, row, col):
        if not self.is_valid_cell(row, col):
            return False

        if not self.user_path:
            # First point must be the start position
            if row == self.start_pos['row'] and col == self.start_pos['col']:
                self.user_path.append({'row': row, 'col': col})
                self.draw_user_path()  # Draw after first point
                return True
            else:
                self.show_modal('Invalid Start!', 'Please start drawing from the House 🏠.')
                return False

        last_point = self.user_path[-1]

        # Check if the new point is adjacent (horizontally or vertically)
        is_adjacent = (abs(row - last_point['row']) + abs(col - last_point['col']) == 1)

        # Check if the new point is already the last point (prevent duplicates)
        is_same_as_last = (row == last_point['row'] and col == last_point['col'])

        if is_adjacent and not is_same_as_last:
            self.user_path.append({'row': row, 'col': col})
            self.draw_user_path()  # Draw updated path using the dedicated shape
            return True
        elif not is_same_as_last and not is_adjacent:
            self.is_drawing = False
            self.show_modal('Invalid Move!', 'You can only draw to adjacent cells (up, down, left, right).')
            return False
        return True  # If it's the same cell, just ignore

    def start_drawing(self, e: ft.ControlEvent):
        self.is_drawing = True
        self.user_path = []
        self.user_path_shape.elements.clear()  # Clear the path shape when starting
        if hasattr(self, 'page') and self.page:
            self.page.update()  # Update the canvas immediately
        coords = self.get_grid_coords(e.local_x, e.local_y)
        self.add_point_to_path(coords['row'], coords['col'])

    def draw(self, e: ft.ControlEvent):
        if not self.is_drawing:
            return
        coords = self.get_grid_coords(e.local_x, e.local_y)
        # Only add if the cell is different from the last one
        if not self.user_path or coords['row'] != self.user_path[-1]['row'] or coords['col'] != self.user_path[-1]['col']:
            self.add_point_to_path(coords['row'], coords['col'])

    def stop_drawing(self, e: ft.ControlEvent):
        self.is_drawing = False

    def find_shortest_path_bfs(self, maze, start, end):
        queue = collections.deque([{'row': start['row'], 'col': start['col'], 'path': [{'row': start['row'], 'col': start['col']}]}])
        visited = set()
        visited.add(f"{start['row']},{start['col']}")

        directions = [
            {'dr': -1, 'dc': 0}, # Up
            {'dr': 1, 'dc': 0},  # Down
            {'dr': 0, 'dc': -1}, # Left
            {'dr': 0, 'dc': 1}   # Right
        ]

        while queue:
            current = queue.popleft()
            row, col, path = current['row'], current['col'], current['path']

            if row == end['row'] and col == end['col']:
                return path # Found the shortest path

            for direction in directions:
                new_row = row + direction['dr']
                new_col = col + direction['dc']
                cell_key = f"{new_row},{new_col}"

                if self.is_valid_cell(new_row, new_col) and cell_key not in visited:
                    visited.add(cell_key)
                    queue.append({'row': new_row, 'col': new_col, 'path': path + [{'row': new_row, 'col': new_col}]})
        return None # No path found

    def check_path(self, e):
        if not self.user_path:
            self.show_modal('No Path Drawn!', 'Please draw a path from the house to the pizza place.')
            return

        first_point = self.user_path[0]
        if first_point['row'] != self.start_pos['row'] or first_point['col'] != self.start_pos['col']:
            self.show_modal('Invalid Path!', 'Your path must start at the House 🏠.')
            return

        last_point = self.user_path[-1]
        if last_point['row'] != self.end_pos['row'] or last_point['col'] != self.end_pos['col']:
            self.show_modal('Incomplete Path!', 'Your path must reach the Pizza Shop 🍕.')
            return

        for p in self.user_path:
            if self.maze_grid[p['row']][p['col']] == 1:
                self.show_modal('Invalid Path!', 'Your path went through a wall! Try again.')
                return

        user_path_length = len(set(f"{p['row']},{p['col']}" for p in self.user_path))

        shortest_path = self.find_shortest_path_bfs(self.maze_grid, self.start_pos, self.end_pos)

        if not shortest_path:
            self.show_modal('Error!', 'Could not find a valid path in the maze. This should not happen.')
            return

        self.shortest_path_length = len(shortest_path)
        length_difference = user_path_length - self.shortest_path_length

        points_awarded = 0
        message = ''
        show_next = False

        if length_difference == 0:
            points_awarded = 10
            message = 'Perfect! You found the shortest path! 🎉'
            show_next = True
        elif length_difference <= 2:
            points_awarded = 5
            message = f"Great job! Your path was only {length_difference} cells longer than the shortest."
            show_next = True
        elif length_difference <= 5:
            points_awarded = 2
            message = f"Good effort! Your path was {length_difference} cells longer than the shortest."
            show_next = True
        else:
            points_awarded = 0
            message = f"Your path was quite long ({length_difference} cells longer). Keep trying!"
            show_next = False

        self.score += points_awarded
        self.update_score_display()
        self.show_modal('Path Checked!', message + f" You earned {points_awarded} points.", show_next)

        self.draw_shortest_path(shortest_path)

    def draw_shortest_path(self, path):
        if path:  # Ensure path is not None or empty
            new_path_elements = []
            start_x = path[0]['col'] * self.cell_size + self.cell_size / 2
            start_y = path[0]['row'] * self.cell_size + self.cell_size / 2
            new_path_elements.append(cv.Path.MoveTo(start_x, start_y))

            for i in range(1, len(path)):
                x = path[i]['col'] * self.cell_size + self.cell_size / 2
                y = path[i]['row'] * self.cell_size + self.cell_size / 2
                new_path_elements.append(cv.Path.LineTo(x, y))

            self.shortest_path_shape.elements = new_path_elements
            if hasattr(self, 'page') and self.page:
                self.page.update()

    def clear_path(self, e):
        self.user_path = []
        self.user_path_shape.elements.clear()
        self.shortest_path_shape.elements.clear() # Also clear the displayed shortest path
        self.message_text.value = 'Path cleared. Draw a new path!'
        if hasattr(self, 'page') and self.page:
            self.page.update()

    def update_score_display(self):
        # In a real Flet app, you'd get the user ID from Firebase Auth in Python
        # For this example, we'll use a placeholder.
        display_user_id = "flet_user_id..." # Replace with actual user ID if Firebase is integrated
        self.score_level_text.value = f"Score: {self.score} | Level: {self.current_level + 1} | User: {display_user_id}"
        self.page.update()

    def start_game(self):
        self.user_path = []
        self._update_maze_dimensions() # Update dimensions for current level
        self.draw_maze()
        self.update_score_display()
        self.message_text.value = f"Level {self.current_level + 1}: Draw a path from the house to the pizza place!"
        
        # Calculate shortest path length once at the start of each level
        shortest_path = self.find_shortest_path_bfs(self.maze_grid, self.start_pos, self.end_pos)
        if shortest_path:
            self.shortest_path_length = len(shortest_path)
            print(f"Level {self.current_level + 1} shortest path length: {self.shortest_path_length}")
        else:
            print("Could not find shortest path during game initialization for current level.")
        self.page.update()

    def show_modal(self, title, message, show_next_level_button=False):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.close_modal(e, dlg)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dismissed!"),
        )
        if show_next_level_button and self.current_level < len(MAZES) - 1:
            dlg.actions.append(
                ft.ElevatedButton(
                    "Next Level",
                    on_click=lambda e: self.go_to_next_level(e, dlg),
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.Colors.BLUE_600},  # Changed ft.MaterialState.DEFAULT to ""
                        color={"": ft.Colors.WHITE},  # Changed ft.MaterialState.DEFAULT to ""
                        shape=ft.RoundedRectangleBorder(radius=8),
                    )
                )
            )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def close_modal(self, e, dlg):
        dlg.open = False
        self.page.update()

    def go_to_next_level(self, e, dlg):
        self.close_modal(e, dlg)
        self.current_level += 1
        if self.current_level < len(MAZES):
            self.start_game()
        else:
            self.show_modal('Congratulations!', f'You have completed all levels! Your final score is {self.score} points.')
            self.current_level = 0 # Reset for replay
            self.score = 0
            self.start_game() # Start from level 1 again


def main(page: ft.Page):
    page.title = "Pizza Delivery Maze Challenge"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 800
    page.window_height = 900
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.fonts = {
        "Inter": "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
    }
    page.theme = ft.Theme(font_family="Inter")

    game = MazeGame()
    page.add(game)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
