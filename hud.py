import pygame

class HeadsUpDisplay:
    # Class that sets and displays the game's HUD (countdown timer and hints)

    def __init__(self, screen, time_left=300):
        self.screen_width = screen.width
        self.screen_height = screen.height

        # Set total game time (seconds)
        self.time_left = time_left
        self.total_mins = self.time_left // 60 # minutes left
        self.total_secs = self.time_left - (self.total_mins * 60) # seconds left
        
        self.text_font = pygame.font.Font("./graphics//fonts/hud_font.ttf", size=40)

        # Repeatedly create a custom user event every "x" milliseconds
        self.countdown_timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.countdown_timer_event, millis=1000)

        # Initial render
        self.update_text()

    def update_text(self):
        self.timer_surface = self.text_font.render(f"TIME LEFT: {self.total_mins:02}:{self.total_secs:02}", True, (255, 255, 255))
        self.timer_rect = self.timer_surface.get_rect(midbottom=(self.screen_width // 2, self.screen_height))

        self.quit_surface = self.text_font.render(f"PRESS ESC TO QUIT", True, (132, 176, 112))
        self.quit_rect = self.quit_surface.get_rect(bottomleft=(0, self.screen_height))

        self.hint_surface = self.text_font.render(f"ARROW KEYS TO MOVE", True, (223, 213, 88))
        self.hint_rect = self.hint_surface.get_rect(bottomright=(self.screen_width, self.screen_height))

        self.player_move_surface = self.text_font.render(f"P\nL\nA\nY\nE\nR\n \nM\nO\nV\nE\nS", True, (9, 0, 136))
        self.player_move_rect = self.player_move_surface.get_rect(center=(self.screen_width - 25, self.screen_height // 2))

        self.enemy_move_surface = self.text_font.render(f"E\nN\nE\nM\nY\n \nM\nO\nV\nE\nS", True, (136, 9, 0))
        self.enemy_move_rect = self.enemy_move_surface.get_rect(center=(self.screen_width - 25, self.screen_height // 2))

    def start_countdown(self):
        # Avoid negative times
        if self.time_left > 0:
            self.time_left -= 1
            self.total_mins = self.time_left // 60 # minutes left
            self.total_secs = self.time_left - (self.total_mins * 60) # seconds left
            self.update_text()
        else:
            # Disable the custom user event when countdown timer reaches zero
            pygame.time.set_timer(self.countdown_timer_event, millis=0)