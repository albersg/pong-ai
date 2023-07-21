import matplotlib.pyplot as plt
import numpy as np
import pygame

from agent import Agent
from ball import Ball
from paddle import Paddle

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

    # Create agents for both paddles
    agent_a = Agent(state_size, action_size)
    agent_b = Agent(state_size, action_size)

    running = True
    frame_counter = 0
    g_score = 10
    history = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Catch the states and let the agents decide the action
        state_a = np.array([ball.rect.x, ball.rect.y, paddle_a.rect.y, ball.velocity[0], ball.velocity[1]])
        state_b = np.array([ball.rect.x, ball.rect.y, paddle_b.rect.y, ball.velocity[0], ball.velocity[1]])

        action_a = agent_a.act(state_a)
        action_b = agent_b.act(state_b)

        if action_a == 0:
            paddle_a.move_up(5)
        elif action_a == 1:
            paddle_a.move_down(5)

        if action_b == 0:
            paddle_b.move_up(5)
        elif action_b == 1:
            paddle_b.move_down(5)

        reward_a = 0
        reward_b = 0

        # Handle scoring and ball collisions with walls and paddles
        if ball.rect.x >= 690:
            score_a += 1
            reward_b = -10
            ball.reset()
        if ball.rect.x <= 0:
            score_b += 1
            reward_a = -10
            ball.reset()
        if ball.rect.y > 490:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y < 0:
            ball.velocity[1] = -ball.velocity[1]

        if pygame.sprite.collide_mask(ball, paddle_a) or pygame.sprite.collide_mask(ball, paddle_b):
            if pygame.sprite.collide_mask(ball, paddle_a):
                ball.bounce(paddle_a)
                ball.rect.x += 10
                reward_a = 10
            elif pygame.sprite.collide_mask(ball, paddle_b):
                ball.bounce(paddle_b)
                ball.rect.x -= 10
                reward_b = 10

        # Metric to measure the improvement (or decrease) in performance
        if -10 == reward_b or reward_b == 10:
            g_score = 0.05 * reward_b + g_score * 0.95

        all_sprites_list.update()

        next_state_a = np.array([ball.rect.x, ball.rect.y, paddle_a.rect.y, ball.velocity[0], ball.velocity[1]])
        next_state_b = np.array([ball.rect.x, ball.rect.y, paddle_b.rect.y, ball.velocity[0], ball.velocity[1]])

        # Capture the experiences of the agents for later learning
        agent_a.capture_sample((state_a, action_a, reward_a, next_state_a))
        agent_b.capture_sample((state_b, action_b, reward_b, next_state_b))

        # Process the training of the agents
        agent_a.process()
        agent_b.process()

        # Display the game every 100 frames
        if frame_counter % 100 == 0:
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

            print(frame_counter)

        # Store game history for plotting
        if frame_counter % 200 == 0:
            history.append((frame_counter, g_score))
        frame_counter = frame_counter + 1

    # Plot the game score history
    x_val = [x[0] for x in history]
    y_val = [x[1] for x in history]

    plt.plot(x_val, y_val)
    plt.xlabel("Game Time")
    plt.ylabel("Score")
    plt.show()

    # Save Agent B's trained model
    agent_b.save_model("AgenteB")

    pygame.quit()


if __name__ == '__main__':
    main()
