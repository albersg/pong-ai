import pygame
from ball import Ball
from paddle import Paddle
from agent import Agent
import numpy as np

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

    # Create paddles and ball objects
    paddle_a = Paddle(WHITE, 10, 100)
    paddle_a.rect.x = 20
    paddle_a.rect.y = 200

    paddle_b = Paddle(WHITE, 10, 100)
    paddle_b.rect.x = 670
    paddle_b.rect.y = 200

    ball = Ball(WHITE, 10, 10)
    ball.rect.x = 345
    ball.rect.y = 195

    # Group all sprites to manage them easily
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(paddle_a)
    all_sprites_list.add(paddle_b)
    all_sprites_list.add(ball)

    score_a = 0
    score_b = 0

    state_size = 5
    action_size = 3

    # Create an agent with the given state and action sizes
    agent_b = Agent(state_size, action_size)
    agent_b.load_model("AgenteB")

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

        # Get the current state for Agent B
        state_b = np.array([ball.rect.x, ball.rect.y, paddle_b.rect.y, ball.velocity[0], ball.velocity[1]])

        # Let Agent B act based on the current state and move the paddle accordingly
        action_b = agent_b.act(state_b)
        if action_b == 0:
            paddle_b.move_up(5)
        elif action_b == 1:
            paddle_b.move_down(5)

        # Handle scoring and ball collisions with walls and paddles
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

        # Draw the center line
        for y in range(0, 500, 15):
            pygame.draw.line(window, WHITE, (349, y), (349, y + 5), 6)

        # Draw all sprites on the window
        all_sprites_list.draw(window)

        # Draw the scores on the window
        font = pygame.font.Font(None, 74)
        text = font.render(str(score_a), 1, WHITE)
        window.blit(text, (250, 10))
        text = font.render(str(score_b), 1, WHITE)
        window.blit(text, (420, 10))

        # Update the display
        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()
