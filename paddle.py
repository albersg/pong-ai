import pygame

BLACK = (0, 0, 0)

# Define a Paddle class that represents the player's paddle.
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        # Create a surface for the paddle sprite with the specified width and height.
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw a rectangle (paddle) on the surface with the specified color.
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Get the rectangle that contains the paddle sprite.
        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        # Move the paddle up by 'pixels' number of pixels.
        self.rect.y -= pixels
        if self.rect.y < 0:
            # Ensure the paddle does not go beyond the top boundary.
            self.rect.y = 0

    def move_down(self, pixels):
        # Move the paddle down by 'pixels' number of pixels.
        self.rect.y += pixels
        if self.rect.y > 400:
            # Ensure the paddle does not go beyond the bottom boundary.
            self.rect.y = 400
