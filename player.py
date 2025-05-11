import pygame
from random import choice

class Player:
    # Class that manages the player's character

    def __init__(self, cols, rows, maze, tile):
        # Set the player's initial pixel position to a random corner of the maze
        self.image = pygame.image.load("./graphics/characters/player.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 1.5)

        self.maze = maze
        self.position = choice(self.maze.start_positions["player"])
        self.rect = self.image.get_rect(center=self.position)

        # Convert pixel coordinates to grid coordinates to store the player's initial cell position
        self.col = self.position[0] // tile
        self.row = self.position[1] // tile

    def attempt_move(self, key, maze, tile):
        # Get the current grid cell where the player is located
        current_cell = maze.grid_cells[self.col + self.row * maze.cols]

        # Determine which way the player wants to go
        dx = dy = 0
        if key == pygame.K_LEFT or key == pygame.K_a: dx = -1
        if key == pygame.K_RIGHT or key == pygame.K_d: dx = 1
        if key == pygame.K_UP or key == pygame.K_w: dy = -1
        if key == pygame.K_DOWN or key == pygame.K_s: dy = 1

        # Guard clause if no movement keys are pressed
        if dx == 0 and dy == 0: return False

        # Check if there's a wall in that direction
        if dx == -1 and current_cell.walls["left"]: return False
        if dx == 1 and current_cell.walls["right"]: return False
        if dy == -1 and current_cell.walls["top"]: return False
        if dy == 1 and current_cell.walls["bottom"]: return False

        # Check target cell grid coordinates for out-of-bounds
        new_col = self.col + dx
        new_row = self.row + dy
        if not (0 <= new_col < maze.cols and 0 <= new_row < maze.rows): return False

        # Commit the player's move
        half = tile // 2
        self.col, self.row = new_col, new_row
        self.rect.center = (self.col * tile + half, self.row * tile + half)

        return True