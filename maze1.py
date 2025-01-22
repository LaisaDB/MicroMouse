import tkinter as tk
from collections import deque

CELL_SIZE = 40
NUM_COLS = 6
NUM_ROWS = 6


DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

START = 'S'
GOAL = 'G'
WALL = 'W'
OPEN = 'O'

class MazeSolverApp:
    def __init__(self, root):
        self.root = root
        self.grid = [[OPEN for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
        self.start_pos = None
        self.goal_pos = None
        self.current_tool = OPEN  


        self.canvas = tk.Canvas(root, width=NUM_COLS * CELL_SIZE, height=NUM_ROWS * CELL_SIZE, bg='#f4f4f9')
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.canvas.bind("<Button-1>", self.on_grid_click)


        self.tool_panel = tk.Frame(root, padx=15, pady=10, bg='#282c34')
        self.tool_panel.grid(row=0, column=1, sticky="n", padx=10)
        self.wall_button = tk.Button(self.tool_panel, text="Place Wall", command=self.activate_wall_tool, bg='#ff6f61', fg='white', font=('Arial', 12), relief="raised", width=15)
        self.wall_button.grid(row=0, column=0, pady=5)

        self.start_button = tk.Button(self.tool_panel, text="Set Start", command=self.activate_start_tool, bg='#4caf50', fg='white', font=('Arial', 12), relief="raised", width=15)
        self.start_button.grid(row=1, column=0, pady=5)

        self.goal_button = tk.Button(self.tool_panel, text="Set Goal", command=self.activate_goal_tool, bg='#f44336', fg='white', font=('Arial', 12), relief="raised", width=15)
        self.goal_button.grid(row=2, column=0, pady=5)

        self.solve_button = tk.Button(self.tool_panel, text="Solve", command=self.solve_maze, bg='#3f51b5', fg='white', font=('Arial', 12), relief="raised", width=15)
        self.solve_button.grid(row=3, column=0, pady=5)

        self.reset_button = tk.Button(self.tool_panel, text="Reset", command=self.reset_grid, bg='#607d8b', fg='white', font=('Arial', 12), relief="raised", width=15)
        self.reset_button.grid(row=4, column=0, pady=5)

        self.draw_grid()

    def activate_wall_tool(self):
        self.current_tool = WALL

    def activate_start_tool(self):
        self.current_tool = START

    def activate_goal_tool(self):
        self.current_tool = GOAL

    def draw_grid(self):
        """ Draw the grid based on the current state. """
        self.canvas.delete("all")  
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                x0 = col * CELL_SIZE
                y0 = row * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE

              
                if self.grid[row][col] == WALL:
                    color = "#424242"  
                elif self.grid[row][col] == START:
                    color = "#66bb6a" 
                elif self.grid[row][col] == GOAL:
                    color = "#ff7043" 
                else:
                    color = "#ffffff" 

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#2e2e2e", width=2)

        for row in range(NUM_ROWS + 1):
            self.canvas.create_line(0, row * CELL_SIZE, NUM_COLS * CELL_SIZE, row * CELL_SIZE, fill="#bbbbbb", width=2)
        for col in range(NUM_COLS + 1):
            self.canvas.create_line(col * CELL_SIZE, 0, col * CELL_SIZE, NUM_ROWS * CELL_SIZE, fill="#bbbbbb", width=2)

    def on_grid_click(self, event):
        """ Handle user clicks on the grid. """
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        if self.current_tool == WALL:
            self.grid[row][col] = WALL
        elif self.current_tool == START:
            if self.start_pos:
                self.grid[self.start_pos[0]][self.start_pos[1]] = OPEN
            self.grid[row][col] = START
            self.start_pos = (row, col)
        elif self.current_tool == GOAL:
            if self.goal_pos:
                self.grid[self.goal_pos[0]][self.goal_pos[1]] = OPEN
            self.grid[row][col] = GOAL
            self.goal_pos = (row, col)

        self.draw_grid()

    def reset_grid(self):
        """ Reset the grid to its initial state. """
        self.grid = [[OPEN for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
        self.start_pos = None
        self.goal_pos = None
        self.draw_grid()

    def solve_maze(self):
        """ Solve the maze using BFS and highlight the path. """
        if not self.start_pos or not self.goal_pos:
            print("Start and goal must be set!")
            return

        path = self.bfs(self.start_pos, self.goal_pos)
        if path:
            self.highlight_path(path)
        else:
            print("No path found!")

    def bfs(self, start, goal):
        """ Perform BFS to find the shortest path from start to goal. """
        queue = deque([start])
        parent_map = {start: None}
        visited = set()
        visited.add(start)

        while queue:
            current = queue.popleft()

            if current == goal:
               
                path = []
                while current:
                    path.append(current)
                    current = parent_map[current]
                path.reverse()
                return path

            for direction in DIRECTIONS:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

             
                if 0 <= neighbor[0] < NUM_ROWS and 0 <= neighbor[1] < NUM_COLS:
                    if neighbor not in visited and self.grid[neighbor[0]][neighbor[1]] != WALL:
                        visited.add(neighbor)
                        parent_map[neighbor] = current
                        queue.append(neighbor)

        return None

    def highlight_path(self, path):
        """ Highlight the found path in cyan. """
        for row, col in path:
            x0 = col * CELL_SIZE
            y0 = row * CELL_SIZE
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="#00bcd4", outline="#2e2e2e", width=2)


root = tk.Tk()
root.title("Maze Solver with BFS")

app = MazeSolverApp(root)

root.mainloop()
