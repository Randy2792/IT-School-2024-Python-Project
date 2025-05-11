import pygame
from random import choice

class Cell:
    # Class that represents a single cell within the grid

    def __init__(self, x, y):
        # Set the grid coordinates (column & row) of each cell within the maze
        (self.x, self.y) = (x, y)

        # Track the presence of walls surrounding the cell (all walls are initially present)
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

        # Keep track of whether the cell has been visited during maze generation or traversal
        self.visited = False

    def draw(self, screen, wall_surf, tile, thickness):
        # Create and add walls for each grid cell
        
        # Set pixel width (tile) and height (thickness) of wall
        horizontal_wall = pygame.transform.scale(wall_surf, (tile, thickness))
        vertical_wall = pygame.transform.rotate(horizontal_wall, -90)

        # Convert grid coordinates to pixel coordinates to get the top-left corner of the cell
        (x, y) = (self.x * tile, self.y * tile)

        # Check if the wall exists and draw it
        if self.walls["top"]:
            screen.blit(horizontal_wall, (x, y))
        if self.walls["right"]:
            screen.blit(vertical_wall, (x + tile - thickness, y))
        if self.walls["bottom"]:
            screen.blit(horizontal_wall, (x, y + tile - thickness))
        if self.walls["left"]:
            screen.blit(vertical_wall, (x, y))

    def check_cell(self, x, y, cols, rows, grid_cells):
        # Check if the cell at the given coordinates exists and return it if it does
        
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False

        # Convert 2D coordinates (x, y) into a 1D index using row‑major order
        find_index = lambda x, y: x + y * cols
        return grid_cells[find_index(x, y)]

    def check_neighbors(self, cols, rows, grid_cells):
        # Check cell neighbors of current cell if visited or not

        neighbors = []
        top = self.check_cell(self.x, self.y - 1, cols, rows, grid_cells)
        right = self.check_cell(self.x + 1, self.y, cols, rows, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, cols, rows, grid_cells)
        left = self.check_cell(self.x - 1, self.y, cols, rows, grid_cells)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        
        return choice(neighbors) if neighbors else False