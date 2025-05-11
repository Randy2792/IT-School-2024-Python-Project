import pygame
from cell import Cell
from random import choice

class Maze:
    # Class that generates the maze

    def __init__(self, cols, rows, tile):
        # Set the grid dimensions (number of columns and rows)
        self.cols = cols
        self.rows = rows

        # Create the grid (flat list of Cell objects)
        self.grid_cells = [Cell(col, row) for row in range(self.rows) for col in range(self.cols)]

        # Set the starting positions for the player and enemy
        half = tile // 2

        top_left = (half, half)
        top_right = (((cols - 1) * tile + half), half)
        bottom_left = (half, ((rows - 1) * tile + half))
        bottom_right = ((cols - 1) * tile + half, (rows - 1) * tile + half)
        middle = ((cols // 2) * tile + half, (rows // 2) * tile + half)

        self.start_positions = {"player": [top_left, top_right, bottom_left, bottom_right], "enemy": middle}

    def remove_walls(self, current, next):
        # Remove the walls between 2 adjacent cells in the maze to create a path

        # Calculate the difference in the x coordinates between the current and next cells
        dx = current.x - next.x
        if dx == 1:
            current.walls["left"] = False
            next.walls["right"] = False
        elif dx == -1:
            current.walls["right"] = False
            next.walls["left"] = False

        # Calculate the difference in the y coordinates between the current and next cells
        dy = current.y - next.y
        if dy == 1:
            current.walls["top"] = False
            next.walls["bottom"] = False
        elif dy == -1:
            current.walls["bottom"] = False
            next.walls["top"] = False

    def generate_maze(self):
        # Randomized depth‑first search maze algorithm ("recursive backtracker")

        current_cell = self.grid_cells[0]
        stack = []
        visited_count = 1

        while visited_count != len(self.grid_cells):
            current_cell.visited = True

            # Check for a unvisited neighboring cell
            next_cell = current_cell.check_neighbors(self.cols, self.rows, self.grid_cells)
            if next_cell:
                next_cell.visited = True
                visited_count += 1
                stack.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif stack:
                current_cell = stack.pop()

        # Return the fully generated maze
        return self.grid_cells