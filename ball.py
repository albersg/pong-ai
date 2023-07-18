import pygame
import random
import math

BLACK = (0, 0, 0)


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.bounced = False

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity_x = random.randint(5, 6)
        self.velocity = [random.randint(3, 4), random.randint(-5, 5)]

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self, paddle):
        if ~self.bounced:
            if self.velocity[0] > 0:
                self.velocity[0] = - self.velocity_x
            else:
                self.velocity[0] = self.velocity_x
            self.bounced = True
        else:
            self.velocity[0] = -self.velocity[0]

        relative_y = paddle.rect.centery - self.rect.centery
        normalized_relative_y = relative_y / (paddle.rect.height / 2.0)

        max_velocity = abs(self.velocity[0]) * 2
        self.velocity[1] = normalized_relative_y * max_velocity

    def reset(self):
        self.rect.x = 345
        self.rect.y = 245
        self.bounced = False
        self.velocity[1] = random.randint(-5, 5)

