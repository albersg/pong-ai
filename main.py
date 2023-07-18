import pygame
from ball import Ball
from paddle import Paddle
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def main():
    width = 700
    height = 500
    fps = 60

    pygame.init()

    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")

    clock = pygame.time.Clock()

    paddle_a = Paddle(WHITE, 10, 100)
    paddle_a.rect.x = 20
    paddle_a.rect.y = 200

    paddle_b = Paddle(WHITE, 10, 100)
    paddle_b.rect.x = 670
    paddle_b.rect.y = 200

    ball = Ball(WHITE, 10, 10)
    ball.rect.x = 345
    ball.rect.y = 195

    all_sprites_list = pygame.sprite.Group()

    all_sprites_list.add(paddle_a)
    all_sprites_list.add(paddle_b)
    all_sprites_list.add(ball)

    score_a = 0
    score_b = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle_a.move_up(5)
        if keys[pygame.K_s]:
            paddle_a.move_down(5)
        if keys[pygame.K_UP]:
            paddle_b.move_up(5)
        if keys[pygame.K_DOWN]:
            paddle_b.move_down(5)

        if ball.rect.x >= 690:
            score_a += 1
            ball.reset()
        if ball.rect.x <= 0:
            score_b += 1
            ball.reset()
        if ball.rect.y > 490:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y < 0:
            ball.velocity[1] = -ball.velocity[1]

        if pygame.sprite.collide_mask(ball, paddle_a) or pygame.sprite.collide_mask(ball, paddle_b):
            if pygame.sprite.collide_mask(ball, paddle_a):
                ball.bounce(paddle_a)
                ball.rect.x += 10
            elif pygame.sprite.collide_mask(ball, paddle_b):
                ball.bounce(paddle_b)
                ball.rect.x -= 10

        all_sprites_list.update()

        window.fill(BLACK)

        for y in range(0, 500, 15):
            pygame.draw.line(window, WHITE, (349, y), (349, y + 5), 6)

        all_sprites_list.draw(window)

        font = pygame.font.Font(None, 74)
        text = font.render(str(score_a), 1, WHITE)
        window.blit(text, (250, 10))
        text = font.render(str(score_b), 1, WHITE)
        window.blit(text, (420, 10))

        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()

