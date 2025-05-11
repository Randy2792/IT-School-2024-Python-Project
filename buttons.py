import pygame

class Button:
    # Class that sets and displays the game's buttons

    def __init__(self, x, y, image, scale, message):
        # Scale the button image
        width = image.get_width()
        height = image.get_height()
        self.button_image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        
        # Ignore the transparent borders of the button image and crop it
        self.button_rect = self.button_image.get_bounding_rect()
        self.button_image = self.button_image.subsurface(self.button_rect)
        self.button_rect.center = (x, y)

        self.text_font = pygame.font.Font("./graphics/fonts/button_font.ttf", size=30)
        self.text_surface = self.text_font.render(f"{message}", True, (244,205,42))
        self.text_rect = self.text_surface.get_rect(center=(self.button_image.width // 2 + 3, self.button_image.height // 2 + 6))

        # Buttons are initially not clicked
        self.clicked = False

    def draw(self, screen):
        # Create and add buttons on the menu screen

        action = False
        click = pygame.mixer.Sound("./audio/click.ogg")
        click.set_volume(0.1)

        # Get mouse position
        mouse_position = pygame.mouse.get_pos()

        # Check if button is clicked by the left mouse button
        if self.button_rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == True and not self.clicked:
                click.play()
                self.clicked = True
                action = True

        # Check if left mouse button is not clicked
        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False

        # Draw button on screen
        screen.blit(self.button_image, self.button_rect)

        # Draw text on the button
        self.button_image.blit(self.text_surface, self.text_rect)

        # Return the button action
        return action