"""
Classic Snake Game
Control the snake to eat food and grow longer without hitting walls or yourself
"""
import pygame
import random
from typing import List, Tuple, Optional
from games.base_game import BaseGame
from common.constants import BLACK, WHITE, RED, GREEN, DEFAULT_FPS
from common.ui import GameOverlay, ScoreDisplay


class SnakeGame(BaseGame):
    """Classic Snake game implementation"""

    # Class-level metadata
    GAME_NAME = "Snake"
    GAME_DESCRIPTION = "Eat food, grow longer, don't hit yourself!"

    # Game constants
    GRID_SIZE = 20
    GRID_WIDTH = 30
    GRID_HEIGHT = 25
    WINDOW_WIDTH = GRID_SIZE * GRID_WIDTH
    WINDOW_HEIGHT = GRID_SIZE * GRID_HEIGHT + 50  # Extra space for score

    # Colors
    BG_COLOR = BLACK
    GRID_COLOR = (20, 20, 20)
    SNAKE_COLOR = GREEN
    SNAKE_HEAD_COLOR = (0, 200, 0)
    FOOD_COLOR = RED
    TEXT_COLOR = WHITE
    GAME_OVER_COLOR = (255, 100, 100)

    # Directions
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    # Game settings
    INITIAL_SPEED = 8
    MAX_SPEED = 20
    SPEED_INCREASE_THRESHOLD = 50

    def __init__(self):
        """Initialize the snake game"""
        self.screen: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.font: Optional[pygame.font.Font] = None
        self.small_font: Optional[pygame.font.Font] = None
        self.overlay: Optional[GameOverlay] = None
        self.score_display: Optional[ScoreDisplay] = None

        # Game state
        self.snake: List[Tuple[int, int]] = []
        self.direction: Tuple[int, int] = self.RIGHT
        self.next_direction: Tuple[int, int] = self.RIGHT
        self.food: Optional[Tuple[int, int]] = None
        self.score: int = 0
        self.speed: int = self.INITIAL_SPEED
        self.running: bool = True
        self.game_over: bool = False

    def initialize_display(self) -> None:
        """Initialize pygame display and fonts"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.overlay = GameOverlay(self.screen)
        self.score_display = ScoreDisplay()

    def reset_game_state(self) -> None:
        """Reset game state to initial values"""
        self.snake = [(self.GRID_WIDTH // 2, self.GRID_HEIGHT // 2)]
        self.direction = self.RIGHT
        self.next_direction = self.RIGHT
        self.score = 0
        self.game_over = False
        self.speed = self.INITIAL_SPEED
        self.food = self.spawn_food()

    def spawn_food(self) -> Tuple[int, int]:
        """Spawn food at random location not on snake"""
        while True:
            pos = (
                random.randint(0, self.GRID_WIDTH - 1),
                random.randint(0, self.GRID_HEIGHT - 1)
            )
            if pos not in self.snake:
                return pos

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handle keyboard input"""
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif not self.game_over:
                self._handle_direction_input(event.key)
            elif event.key == pygame.K_SPACE:
                self.reset_game_state()

    def _handle_direction_input(self, key: int) -> None:
        """Handle direction change input (prevent 180 degree turns)"""
        direction_map = {
            pygame.K_UP: (self.UP, self.DOWN),
            pygame.K_DOWN: (self.DOWN, self.UP),
            pygame.K_LEFT: (self.LEFT, self.RIGHT),
            pygame.K_RIGHT: (self.RIGHT, self.LEFT),
        }

        if key in direction_map:
            new_direction, opposite = direction_map[key]
            if self.direction != opposite:
                self.next_direction = new_direction

    def update_game_state(self) -> None:
        """Update game state for one frame"""
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Check collisions
        if self._check_collision(new_head):
            self.game_over = True
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
            self._increase_speed()
        else:
            # Remove tail if not eating
            self.snake.pop()

    def _check_collision(self, pos: Tuple[int, int]) -> bool:
        """Check if position collides with walls or snake body"""
        x, y = pos
        return (
            x < 0 or x >= self.GRID_WIDTH or
            y < 0 or y >= self.GRID_HEIGHT or
            pos in self.snake
        )

    def _increase_speed(self) -> None:
        """Increase game speed based on score"""
        self.speed = min(
            self.INITIAL_SPEED + self.score // self.SPEED_INCREASE_THRESHOLD,
            self.MAX_SPEED
        )

    def draw_game(self) -> None:
        """Draw the game state"""
        self.screen.fill(self.BG_COLOR)
        self._draw_grid()
        self._draw_snake()
        self._draw_food()
        self._draw_ui()

        if self.game_over:
            self._draw_game_over()

    def _draw_grid(self) -> None:
        """Draw the game grid"""
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_HEIGHT):
                rect = pygame.Rect(x * self.GRID_SIZE, y * self.GRID_SIZE,
                                   self.GRID_SIZE, self.GRID_SIZE)
                pygame.draw.rect(self.screen, self.GRID_COLOR, rect, 1)

    def _draw_snake(self) -> None:
        """Draw the snake"""
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(
                x * self.GRID_SIZE + 1, y * self.GRID_SIZE + 1,
                self.GRID_SIZE - 2, self.GRID_SIZE - 2
            )
            color = self.SNAKE_HEAD_COLOR if i == 0 else self.SNAKE_COLOR
            pygame.draw.rect(self.screen, color, rect)

    def _draw_food(self) -> None:
        """Draw the food"""
        if self.food:
            x, y = self.food
            center = (
                x * self.GRID_SIZE + self.GRID_SIZE // 2,
                y * self.GRID_SIZE + self.GRID_SIZE // 2
            )
            pygame.draw.circle(self.screen, self.FOOD_COLOR, center,
                               self.GRID_SIZE // 2 - 2)

    def _draw_ui(self) -> None:
        """Draw score and game info"""
        self.score_display.draw(
            self.screen, f"Score: {self.score}",
            (10, self.GRID_HEIGHT * self.GRID_SIZE + 10),
            self.TEXT_COLOR
        )

        length_text = self.small_font.render(f"Length: {len(self.snake)}", True, self.TEXT_COLOR)
        self.screen.blit(length_text, (self.WINDOW_WIDTH - 150, self.GRID_HEIGHT * self.GRID_SIZE + 15))

    def _draw_game_over(self) -> None:
        """Draw game over overlay"""
        self.overlay.draw_overlay(
            title="GAME OVER!",
            subtitle=f"Final Score: {self.score}",
            instructions="Press SPACE to restart or ESC to quit",
            title_color=self.GAME_OVER_COLOR,
            text_color=self.TEXT_COLOR
        )

    def run(self) -> None:
        """Run the Snake game"""
        self.initialize_display()
        self.reset_game_state()

        while self.running:
            # Event handling
            for event in pygame.event.get():
                self.handle_input(event)

            # Update game state
            self.update_game_state()

            # Draw everything
            self.draw_game()

            pygame.display.flip()
            self.clock.tick(self.speed)

        pygame.quit()
