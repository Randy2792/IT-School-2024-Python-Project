import pygame
from random import choice

class Exit:
    # Class that manages the maze's exit

    def __init__(self, cols, rows, player, maze):
        # Set the maze exit to a random corner of the maze
        self.image = pygame.image.load("./graphics/maze/exit.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 1.5)

        self.player = player
        self.maze = maze

        # Exclude player's initial position
        exit_positions = [position for position in self.maze.start_positions["player"] if position != self.player.position]

        self.position = choice(exit_positions)
        self.rect = self.image.get_rect(center=self.position)

class Sound:
    # Class that manages game sound effects and music

    def __init__(self):
        # Import sound effects and background music
        pygame.mixer.music.load("./audio/main_menu.wav")
        pygame.mixer.music.set_volume(0.2)

        self.ambience = pygame.mixer.Sound("./audio/maze_ambience.wav")
        self.ambience.set_volume(0.1)

        self.start = pygame.mixer.Sound("./audio/monster_greeting.wav")
        self.start.set_volume(0.1)
        self.scary_event = pygame.USEREVENT + 2

        self.player_step = pygame.mixer.Sound("./audio/player_step.wav")
        self.player_step.set_volume(0.15)
        self.enemy_step = pygame.mixer.Sound("./audio/enemy_step.wav")
        self.enemy_step.set_volume(0.17)

        self.victory = pygame.mixer.Sound("./audio/victory_sound.wav")
        self.victory.set_volume(0.2)
        self.defeat = pygame.mixer.Sound("./audio/monster_laugh.wav")
        self.defeat.set_volume(0.2)

    def play_menu(self):
        pygame.mixer.music.play(-1)

    def stop_menu(self):
        pygame.mixer.music.stop()

class Animation:
    # Class that manages the game's animations

    def __init__(self):
        # Import enemy animation frames
        enemy_walk_1 = pygame.image.load("./graphics/animations/minotaur-S-stand.png").convert_alpha()
        enemy_walk_2 = pygame.image.load("./graphics/animations/minotaur-S-step1.png").convert_alpha()
        enemy_walk_3 = pygame.image.load("./graphics/animations/minotaur-S-step2.png").convert_alpha()

        self.enemy_walk = [enemy_walk_1, enemy_walk_2, enemy_walk_3]
        self.enemy_index = 0

    def draw(self, screen):
        # Set animation speed
        self.enemy_index += 0.06

        if self.enemy_index >= len(self.enemy_walk): self.enemy_index = 0
        self.walk_image = self.enemy_walk[int(self.enemy_index)]

        # Scale animation image
        self.walk_image = pygame.transform.rotozoom(self.walk_image, 0, 7)
        self.walk_rect = self.walk_image.get_rect(midtop=(screen.width // 2, 100))
        screen.blit(self.walk_image, self.walk_rect)