import pygame
from random import randint, choice, shuffle

class Enemy:
    # Class that manages the enemy's character

    def __init__(self, cols, rows, maze, tile):
        # Set the enemy's initial pixel position to the center of the maze
        self.image = pygame.image.load("./graphics/characters/enemy.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 1.5)

        self.maze = maze
        self.position = self.maze.start_positions["enemy"]
        self.rect = self.image.get_rect(center=self.position)

        # Convert pixel coordinates to grid coordinates to store the enemy's initial cell position
        self.col = self.position[0] // tile
        self.row = self.position[1] // tile

        # Set enemy's initial movement points per turn
        self.move_points = 0

    def attempt_move(self, maze, tile):
        # Randomly skip the enemy's turn
        if randint(1, 4) == 1: return False

        # Get the current grid cell where the enemy is located
        current_cell = maze.grid_cells[self.col + self.row * maze.cols]

        # Determine which way the enemy wants to go
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        shuffle(directions)

        # Check if there's a wall in that direction
        for dx, dy in directions:
            if dx == -1 and current_cell.walls["left"]: continue
            if dx == 1 and current_cell.walls["right"]: continue
            if dy == -1 and current_cell.walls["top"]: continue
            if dy == 1 and current_cell.walls["bottom"]: continue

            # Check target cell grid coordinates for out-of-bounds
            new_col = self.col + dx
            new_row = self.row + dy
            if not (0 <= new_col < maze.cols and 0 <= new_row < maze.rows): continue

            # Commit the enemy's move
            half = tile // 2
            self.col, self.row = new_col, new_row
            self.rect.center = (self.col * tile + half, self.row * tile + half)

            break

        return True