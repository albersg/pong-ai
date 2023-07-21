import pygame
import random

BLACK = (0, 0, 0)


# Define a Ball class that represents the bouncing ball sprite.
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.bounced = False

        # Create a surface for the ball sprite with the specified width and height.
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw a rectangle (ball) on the surface with the specified color.
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Set the initial velocity of the ball.
        self.velocity_x = random.randint(5, 6)
        self.velocity = [random.randint(3, 4), random.randint(-5, 5)]

        # Get the rectangle that contains the ball sprite.
        self.rect = self.image.get_rect()

    def update(self):
        # Update the position of the ball based on its velocity.
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self, paddle):
        # Handle bouncing of the ball when it collides with the paddle.
        if not self.bounced:
            if self.velocity[0] > 0:
                self.velocity[0] = -self.velocity_x
            else:
                self.velocity[0] = self.velocity_x
            self.bounced = True
        else:
            self.velocity[0] = -self.velocity[0]

        # Calculate the normalized relative Y position of the ball with respect to the paddle.
        relative_y = paddle.rect.centery - self.rect.centery
        normalized_relative_y = relative_y / (paddle.rect.height / 2.0)

        # Calculate the maximum velocity of the ball based on its absolute X velocity.
        max_velocity = abs(self.velocity[0]) * 2

        # Adjust the Y velocity of the ball based on the relative Y position and the maximum velocity.
        self.velocity[1] = -(normalized_relative_y * max_velocity)

    def reset(self):
        # Reset the ball to its initial position and velocity.
        self.rect.x = 345
        self.rect.y = 245
        self.bounced = False
        self.velocity[1] = random.randint(-5, 5)
