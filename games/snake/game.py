"""
Classic Snake Game
Control the snake to eat food and grow longer without hitting walls or yourself
"""
import pygame
import random
from games.base_game import BaseGame


class SnakeGame(BaseGame):
    """Classic Snake game implementation"""

    def __init__(self):
        self.name_str = "Snake"
        self.description_str = "Eat food, grow longer, don't hit yourself!"

    @property
    def name(self) -> str:
        return self.name_str

    @property
    def description(self) -> str:
        return self.description_str

    def run(self):
        """Run the Snake game"""
        pygame.init()

        # Constants
        GRID_SIZE = 20
        GRID_WIDTH = 30
        GRID_HEIGHT = 25
        WINDOW_WIDTH = GRID_SIZE * GRID_WIDTH
        WINDOW_HEIGHT = GRID_SIZE * GRID_HEIGHT + 50  # Extra space for score

        # Colors
        BG_COLOR = (0, 0, 0)
        GRID_COLOR = (20, 20, 20)
        SNAKE_COLOR = (0, 255, 0)
        SNAKE_HEAD_COLOR = (0, 200, 0)
        FOOD_COLOR = (255, 0, 0)
        TEXT_COLOR = (255, 255, 255)
        GAME_OVER_COLOR = (255, 100, 100)

        # Directions
        UP = (0, -1)
        DOWN = (0, 1)
        LEFT = (-1, 0)
        RIGHT = (1, 0)

        # Initialize display
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake")
        clock = pygame.time.Clock()

        # Fonts
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)

        # Game state
        snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        direction = RIGHT
        next_direction = RIGHT
        food = None
        score = 0
        running = True
        game_over = False
        initial_speed = 8
        speed = initial_speed

        def spawn_food():
            """Spawn food at random location not on snake"""
            while True:
                pos = (random.randint(0, GRID_WIDTH - 1),
                       random.randint(0, GRID_HEIGHT - 1))
                if pos not in snake:
                    return pos

        food = spawn_food()

        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif not game_over:
                        # Change direction (prevent 180 degree turns)
                        if event.key == pygame.K_UP and direction != DOWN:
                            next_direction = UP
                        elif event.key == pygame.K_DOWN and direction != UP:
                            next_direction = DOWN
                        elif event.key == pygame.K_LEFT and direction != RIGHT:
                            next_direction = LEFT
                        elif event.key == pygame.K_RIGHT and direction != LEFT:
                            next_direction = RIGHT
                    else:
                        # Restart on any key after game over
                        if event.key == pygame.K_SPACE:
                            # Reset game
                            snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                            direction = RIGHT
                            next_direction = RIGHT
                            food = spawn_food()
                            score = 0
                            game_over = False
                            speed = initial_speed

            if not game_over:
                # Update direction
                direction = next_direction

                # Move snake
                head_x, head_y = snake[0]
                new_head = (head_x + direction[0], head_y + direction[1])

                # Check collisions
                if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                    new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                    new_head in snake):
                    game_over = True
                else:
                    # Add new head
                    snake.insert(0, new_head)

                    # Check if food eaten
                    if new_head == food:
                        score += 10
                        food = spawn_food()
                        # Increase speed slightly
                        speed = min(initial_speed + score // 50, 20)
                    else:
                        # Remove tail if not eating
                        snake.pop()

            # Drawing
            screen.fill(BG_COLOR)

            # Draw grid
            for x in range(GRID_WIDTH):
                for y in range(GRID_HEIGHT):
                    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(screen, GRID_COLOR, rect, 1)

            # Draw snake
            for i, segment in enumerate(snake):
                x, y = segment
                rect = pygame.Rect(x * GRID_SIZE + 1, y * GRID_SIZE + 1,
                                   GRID_SIZE - 2, GRID_SIZE - 2)
                color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
                pygame.draw.rect(screen, color, rect)

            # Draw food
            if food:
                x, y = food
                center = (x * GRID_SIZE + GRID_SIZE // 2,
                         y * GRID_SIZE + GRID_SIZE // 2)
                pygame.draw.circle(screen, FOOD_COLOR, center, GRID_SIZE // 2 - 2)

            # Draw score
            score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
            screen.blit(score_text, (10, GRID_HEIGHT * GRID_SIZE + 10))

            # Draw length
            length_text = small_font.render(f"Length: {len(snake)}", True, TEXT_COLOR)
            screen.blit(length_text, (WINDOW_WIDTH - 150, GRID_HEIGHT * GRID_SIZE + 15))

            # Draw game over message
            if game_over:
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))

                game_over_text = font.render("GAME OVER!", True, GAME_OVER_COLOR)
                game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
                screen.blit(game_over_text, game_over_rect)

                final_score_text = font.render(f"Final Score: {score}", True, TEXT_COLOR)
                final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
                screen.blit(final_score_text, final_score_rect)

                restart_text = small_font.render("Press SPACE to restart or ESC to quit", True, TEXT_COLOR)
                restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
                screen.blit(restart_text, restart_rect)

            pygame.display.flip()
            clock.tick(speed)

        pygame.quit()
