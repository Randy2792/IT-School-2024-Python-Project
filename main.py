import pygame
from random import randint
from maze import Maze
from player import Player
from enemy import Enemy
from game import Exit, Sound, Animation
from hud import HeadsUpDisplay
from buttons import Button

# Initialize pygame modules
pygame.init()

# Set window title and icon
pygame.display.set_caption("Escape the Maze")
window_img = pygame.image.load("./graphics/icons/minotaur.png")
pygame.display.set_icon(window_img)

# Set game window and game HUD
HUD_WIDTH = 60
HUD_HEIGHT = 40
win_res = (window_width, window_height) = (1280 + HUD_WIDTH, 1024 + HUD_HEIGHT)
screen = pygame.display.set_mode(win_res, flags=pygame.SCALED | pygame.RESIZABLE)
cell_tile_size = 64  # pixel dimensions (width x height) of each grid cell

# Set number of grid columns and rows
cols = 20
rows = 16

# Set the game framerate
clock = pygame.time.Clock()

# Game initial states
game_running = True
game_active = False
victory = False
game_turn = None

# Delay the enemy's turn by "x" milliseconds
ENEMY_DELAY = 500

# Import images and font
button_img = pygame.image.load("./graphics/icons/button.png").convert_alpha()

terrain_surface = pygame.image.load("./graphics/maze/floor.png").convert()
terrain_surface = pygame.transform.scale(terrain_surface, (cell_tile_size, cell_tile_size))

wall_surface = pygame.image.load("./graphics/maze/wall.png").convert()
wall_thickness = 8

menu_background = pygame.image.load("./graphics/icons/background.png")
menu_background = pygame.transform.scale(menu_background, (window_width, window_height))

game_over_surface = pygame.image.load("./graphics/icons/game_over.png").convert_alpha()
game_over_surface = pygame.transform.rotozoom(game_over_surface, 0, 0.7)
game_over_rect = game_over_surface.get_rect(center=(screen.width // 2, screen.height // 2))

game_over_font = pygame.font.Font("./graphics/fonts/button_font.ttf", size=33)
game_over_lose_surface = game_over_font.render("YOUR BONES WILL SATE THE MINOTAUR'S HUNGER", True, (123,24,24))
game_over_lose_rect = game_over_lose_surface.get_rect(center=(screen.width // 2, 268))
game_over_win_surface = game_over_font.render("THE MAZE'S SHADOWS COULDN'T HOLD YOU", True, (25,97,24))
game_over_win_rect = game_over_win_surface.get_rect(center=(screen.width // 2, 268))

# Set main menu animation and sound
minotaur_animation = Animation()
sound = Sound()
sound.play_menu()

# Set game buttons
start_button = Button(window_width // 2, window_height // 2 + 75, button_img, 1, "START")
exit_button = Button(window_width // 2, window_height // 2 + 165, button_img, 1, "EXIT")
return_button = Button(window_width // 2, window_height // 2 + 260, button_img, 1, "RETURN")

# Game loop
while game_running:
    
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

        if game_active is True:
            # Game over when countdown timer reaches 0
            if event.type == game.countdown_timer_event:
                game.start_countdown()
                if game.time_left == 0:
                    game_active = None

            if event.type == sound.scary_event:
                sound.start.play(fade_ms=1000)

            # Game over when player presses ESC key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sound.ambience.stop()
                    game_active = False
                    sound.play_menu()

            if game_turn == 1:
                # Player moves
                if event.type == pygame.KEYDOWN:
                    player_moved = hero.attempt_move(event.key, maze, cell_tile_size)
                    if player_moved:
                        sound.player_step.play()
                        # Record the timestamp when the player successfully moves
                        last_player_move_time = pygame.time.get_ticks()

                        # Pass turn to the enemy
                        game_turn = 0

            elif game_turn == 0:
                # Enemy moves
                current_time = pygame.time.get_ticks()
                if current_time - last_player_move_time >= ENEMY_DELAY:
                    # Check if enemy has any movement points left at the start of the enemy turn
                    if minotaur.move_points == 0:
                        minotaur.move_points = 2
                    
                    # Enemy takes one step after delay
                    enemy_moved = minotaur.attempt_move(maze, cell_tile_size)
                    if enemy_moved: sound.enemy_step.play()
                    minotaur.move_points -= 1

                    # Reset the delay timer
                    last_player_move_time = pygame.time.get_ticks()
                    
                    # Pass turn to the player when the enemy has no more movement points left
                    if minotaur.move_points == 0:
                        game_turn = 1

    # Draw game run
    if game_active is True:
        for cell in cells:
            screen.blit(terrain_surface, (cell.x * terrain_surface.width, cell.y * terrain_surface.height))
            cell.draw(screen, wall_surface, cell_tile_size, wall_thickness)

        screen.blit(hero.image, hero.rect)
        screen.blit(minotaur.image, minotaur.rect)
        screen.blit(game_exit.image, game_exit.rect)
        pygame.draw.rect(screen, "black", (0, 1024, window_width, HUD_HEIGHT))
        screen.blit(game.timer_surface, game.timer_rect)
        screen.blit(game.quit_surface, game.quit_rect)
        screen.blit(game.hint_surface, game.hint_rect)

        # Display turns on HUD
        if game_turn == 1:
            pygame.draw.rect(screen, (89, 130, 255), (1280, 0, HUD_WIDTH, window_height - HUD_HEIGHT))
            screen.blit(game.player_move_surface, game.player_move_rect)
        else:
            pygame.draw.rect(screen, (255, 89, 130), (1280, 0, HUD_WIDTH, window_height - HUD_HEIGHT))
            screen.blit(game.enemy_move_surface, game.enemy_move_rect)

        # Game over when enemy reaches player
        if hero.rect.colliderect(minotaur.rect):
            # Player has 50% chance to dodge the enemy upon encounter
            if randint(0, 1):
                game_active = None

        # Game over when player reaches maze exit
        if hero.rect.colliderect(game_exit.rect):
            victory = True
            game_active = None

    # Draw "GAME OVER" screen
    elif game_active is None:
        # Disable the custom user event when game run is over
        pygame.time.set_timer(sound.scary_event, millis=0)
        sound.ambience.stop()

        if victory:
            sound.victory.play()
            screen.blit(menu_background, (0, 0))
            screen.blit(game_over_surface, (game_over_rect))
            screen.blit(game_over_win_surface, game_over_win_rect)

        else:
            sound.defeat.play()
            screen.blit(menu_background, (0, 0))
            screen.blit(game_over_surface, (game_over_rect))
            screen.blit(game_over_lose_surface, game_over_lose_rect)

        if return_button.draw(screen):
            sound.victory.stop()
            sound.defeat.stop()
            game_active = False
            sound.play_menu()

    # Draw "Main Menu" screen
    elif game_active is False:
        # Disable the custom user event when game run is over
        pygame.time.set_timer(sound.scary_event, millis=0)

        screen.blit(menu_background, (0, 0))
        minotaur_animation.draw(screen)
        
        if start_button.draw(screen):
            # Start a new game
            maze = Maze(cols, rows, cell_tile_size)
            cells = maze.generate_maze()

            hero = Player(cols, rows, maze, cell_tile_size)
            minotaur = Enemy(cols, rows, maze, cell_tile_size)
            game_exit = Exit(cols, rows, hero, maze)

            # Player may choose game run duration (default is 5 minutes)
            game = HeadsUpDisplay(screen, 300)

            pygame.time.set_timer(sound.scary_event, millis=60_000)

            game_turn = 1
            last_player_move_time = 0
            sound.stop_menu()
            sound.ambience.play(-1)
            game_active = True
            victory = False

        if exit_button.draw(screen):
            # Exit game
            game_running = False

    # Update game window at each iteration
    pygame.display.update()
    
    # Set game FPS to 60
    clock.tick(60)

pygame.quit()