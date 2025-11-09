"""
Xonix Game
Claim territory by drawing lines while avoiding enemies
"""
import pygame
import random
from typing import List, Tuple, Set, Optional
from games.base_game import BaseGame
from common.constants import BLACK, WHITE, RED, GREEN, YELLOW
from common.ui import GameOverlay, ScoreDisplay


class Enemy:
    """Enemy ball that bounces around"""

    def __init__(self, x: float, y: float, vx: float, vy: float, radius: int = 8):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius


class XonixGame(BaseGame):
    """Xonix game implementation"""

    # Class-level metadata
    GAME_NAME = "Xonix"
    GAME_DESCRIPTION = "Claim 75% territory while avoiding enemies!"

    # Grid constants
    GRID_SIZE = 10
    GRID_WIDTH = 70
    GRID_HEIGHT = 50
    WINDOW_WIDTH = GRID_SIZE * GRID_WIDTH
    WINDOW_HEIGHT = GRID_SIZE * GRID_HEIGHT + 60

    # Colors
    BG_COLOR = BLACK
    CLAIMED_COLOR = (0, 100, 200)
    BORDER_COLOR = (0, 150, 255)
    PLAYER_COLOR = GREEN
    TRAIL_COLOR = YELLOW
    ENEMY_COLOR = RED
    TEXT_COLOR = WHITE
    GAME_OVER_COLOR = (255, 100, 100)
    WIN_COLOR = GREEN

    # Cell states
    EMPTY = 0
    CLAIMED = 1
    BORDER = 2
    TRAIL = 3

    # Game settings
    TARGET_PERCENTAGE = 75.0
    INITIAL_ENEMIES = 3
    FPS = 30

    def __init__(self):
        """Initialize the Xonix game"""
        self.screen: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.font: Optional[pygame.font.Font] = None
        self.small_font: Optional[pygame.font.Font] = None
        self.overlay: Optional[GameOverlay] = None
        self.score_display: Optional[ScoreDisplay] = None

        # Game state
        self.grid: List[List[int]] = []
        self.player_x: int = 0
        self.player_y: int = 0
        self.enemies: List[Enemy] = []
        self.trail: List[Tuple[int, int]] = []
        self.drawing: bool = False
        self.score: float = 0.0
        self.running: bool = True
        self.game_over: bool = False
        self.game_won: bool = False
        self.message: str = ""

    def initialize_display(self) -> None:
        """Initialize pygame display and fonts"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Xonix")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.overlay = GameOverlay(self.screen)
        self.score_display = ScoreDisplay()

    def reset_game_state(self) -> None:
        """Reset game state to initial values"""
        # Create grid with borders
        self.grid = [[self.EMPTY for _ in range(self.GRID_WIDTH)]
                     for _ in range(self.GRID_HEIGHT)]

        # Create border
        for x in range(self.GRID_WIDTH):
            self.grid[0][x] = self.BORDER
            self.grid[self.GRID_HEIGHT - 1][x] = self.BORDER
        for y in range(self.GRID_HEIGHT):
            self.grid[y][0] = self.BORDER
            self.grid[y][self.GRID_WIDTH - 1] = self.BORDER

        # Player starts on border
        self.player_x = self.GRID_WIDTH // 2
        self.player_y = 0

        # Create enemies
        self.enemies = []
        for _ in range(self.INITIAL_ENEMIES):
            x = random.randint(self.GRID_WIDTH // 4, 3 * self.GRID_WIDTH // 4) * self.GRID_SIZE
            y = random.randint(self.GRID_HEIGHT // 4, 3 * self.GRID_HEIGHT // 4) * self.GRID_SIZE
            vx = random.choice([-2, 2])
            vy = random.choice([-2, 2])
            self.enemies.append(Enemy(x, y, vx, vy))

        self.trail = []
        self.drawing = False
        self.score = 0.0
        self.game_over = False
        self.game_won = False
        self.message = ""

    def get_cell_state(self, x: int, y: int) -> int:
        """Get state of cell at position"""
        if 0 <= x < self.GRID_WIDTH and 0 <= y < self.GRID_HEIGHT:
            return self.grid[y][x]
        return self.BORDER

    def is_on_border_or_claimed(self, x: int, y: int) -> bool:
        """Check if position is on border or claimed territory"""
        state = self.get_cell_state(x, y)
        return state in [self.BORDER, self.CLAIMED]

    def flood_fill(self, start_x: int, start_y: int) -> Tuple[List[Tuple[int, int]], bool]:
        """Flood fill to find unclaimed area and check if enemies are present"""
        visited: Set[Tuple[int, int]] = set()
        stack = [(start_x, start_y)]
        area = []

        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            if not (0 <= x < self.GRID_WIDTH and 0 <= y < self.GRID_HEIGHT):
                continue
            if self.grid[y][x] != self.EMPTY:
                continue

            visited.add((x, y))
            area.append((x, y))

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                stack.append((x + dx, y + dy))

        # Check if any enemy is in this area
        has_enemy = any(
            (int(enemy.x // self.GRID_SIZE), int(enemy.y // self.GRID_SIZE)) in visited
            for enemy in self.enemies
        )

        return area, has_enemy

    def claim_territory(self) -> None:
        """Claim territory after completing a trail"""
        # Mark trail as border
        for x, y in self.trail:
            self.grid[y][x] = self.BORDER

        # Find all empty regions and claim those without enemies
        for y in range(1, self.GRID_HEIGHT - 1):
            for x in range(1, self.GRID_WIDTH - 1):
                if self.grid[y][x] == self.EMPTY:
                    area, has_enemy = self.flood_fill(x, y)
                    if not has_enemy and area:
                        # Claim this area
                        for ax, ay in area:
                            self.grid[ay][ax] = self.CLAIMED

    def calculate_percentage(self) -> float:
        """Calculate percentage of claimed territory"""
        total = (self.GRID_WIDTH - 2) * (self.GRID_HEIGHT - 2)
        claimed = sum(
            1 for y in range(1, self.GRID_HEIGHT - 1)
            for x in range(1, self.GRID_WIDTH - 1)
            if self.grid[y][x] in [self.CLAIMED, self.BORDER]
        )
        return (claimed / total) * 100 if total > 0 else 0.0

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handle keyboard input"""
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif (self.game_over or self.game_won) and event.key == pygame.K_SPACE:
                self.reset_game_state()

    def handle_movement(self, keys) -> None:
        """Handle player movement"""
        if self.game_over or self.game_won:
            return

        new_x, new_y = self.player_x, self.player_y
        moved = False

        if keys[pygame.K_UP]:
            new_y -= 1
            moved = True
        elif keys[pygame.K_DOWN]:
            new_y += 1
            moved = True
        elif keys[pygame.K_LEFT]:
            new_x -= 1
            moved = True
        elif keys[pygame.K_RIGHT]:
            new_x += 1
            moved = True

        if moved and 0 <= new_x < self.GRID_WIDTH and 0 <= new_y < self.GRID_HEIGHT:
            self._process_movement(new_x, new_y)

    def _process_movement(self, new_x: int, new_y: int) -> None:
        """Process player movement to new position"""
        cell_state = self.get_cell_state(new_x, new_y)

        # Start drawing trail
        if not self.drawing and cell_state == self.EMPTY:
            self.drawing = True
            self.trail = [(new_x, new_y)]
            self.player_x, self.player_y = new_x, new_y

        # Hit own trail - game over
        elif self.drawing and (new_x, new_y) in self.trail:
            self.game_over = True
            self.message = "Hit your own trail!"

        # Complete trail
        elif self.drawing and self.is_on_border_or_claimed(new_x, new_y):
            self.drawing = False
            self.claim_territory()
            self.trail = []
            self.player_x, self.player_y = new_x, new_y
            self.score = self.calculate_percentage()
            if self.score >= self.TARGET_PERCENTAGE:
                self.game_won = True
                self.message = "Victory!"

        # Continue drawing
        elif self.drawing and cell_state == self.EMPTY:
            self.trail.append((new_x, new_y))
            self.player_x, self.player_y = new_x, new_y

        # Moving on safe territory
        elif not self.drawing:
            self.player_x, self.player_y = new_x, new_y

    def update_enemies(self) -> None:
        """Update enemy positions and check collisions"""
        for enemy in self.enemies:
            enemy.x += enemy.vx
            enemy.y += enemy.vy

            ex, ey = int(enemy.x // self.GRID_SIZE), int(enemy.y // self.GRID_SIZE)

            # Bounce off walls and claimed territory
            if (enemy.x <= enemy.radius or enemy.x >= self.WINDOW_WIDTH - enemy.radius or
                (0 <= ex < self.GRID_WIDTH and 0 <= ey < self.GRID_HEIGHT and
                 self.grid[ey][ex] in [self.BORDER, self.CLAIMED])):
                enemy.vx = -enemy.vx
                enemy.x += enemy.vx * 2

            if (enemy.y <= enemy.radius or enemy.y >= self.GRID_HEIGHT * self.GRID_SIZE - enemy.radius or
                (0 <= ex < self.GRID_WIDTH and 0 <= ey < self.GRID_HEIGHT and
                 self.grid[ey][ex] in [self.BORDER, self.CLAIMED])):
                enemy.vy = -enemy.vy
                enemy.y += enemy.vy * 2

            # Check collision with player trail
            if self.drawing and self._enemy_hits_trail(enemy):
                self.game_over = True
                self.message = "Enemy hit your trail!"
                break

            # Check collision with player
            if self.drawing and self._enemy_hits_player(enemy):
                self.game_over = True
                self.message = "Enemy hit you!"

    def _enemy_hits_trail(self, enemy: Enemy) -> bool:
        """Check if enemy collides with trail"""
        for tx, ty in self.trail:
            tx_pixel, ty_pixel = tx * self.GRID_SIZE, ty * self.GRID_SIZE
            dist_sq = (enemy.x - tx_pixel) ** 2 + (enemy.y - ty_pixel) ** 2
            if dist_sq < (enemy.radius + self.GRID_SIZE // 2) ** 2:
                return True
        return False

    def _enemy_hits_player(self, enemy: Enemy) -> bool:
        """Check if enemy collides with player"""
        px_pixel, py_pixel = self.player_x * self.GRID_SIZE, self.player_y * self.GRID_SIZE
        dist_sq = (enemy.x - px_pixel) ** 2 + (enemy.y - py_pixel) ** 2
        return dist_sq < (enemy.radius + self.GRID_SIZE // 2) ** 2

    def draw_game(self) -> None:
        """Draw the game state"""
        self.screen.fill(self.BG_COLOR)
        self._draw_grid()
        self._draw_trail()
        self._draw_enemies()
        self._draw_player()
        self._draw_ui()

        if self.game_over or self.game_won:
            self._draw_game_end()

    def _draw_grid(self) -> None:
        """Draw the grid with claimed and border cells"""
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                rect = pygame.Rect(x * self.GRID_SIZE, y * self.GRID_SIZE,
                                   self.GRID_SIZE, self.GRID_SIZE)
                if self.grid[y][x] == self.CLAIMED:
                    pygame.draw.rect(self.screen, self.CLAIMED_COLOR, rect)
                elif self.grid[y][x] == self.BORDER:
                    pygame.draw.rect(self.screen, self.BORDER_COLOR, rect)

    def _draw_trail(self) -> None:
        """Draw the player's trail"""
        for x, y in self.trail:
            rect = pygame.Rect(x * self.GRID_SIZE, y * self.GRID_SIZE,
                               self.GRID_SIZE, self.GRID_SIZE)
            pygame.draw.rect(self.screen, self.TRAIL_COLOR, rect)

    def _draw_enemies(self) -> None:
        """Draw enemies"""
        for enemy in self.enemies:
            pygame.draw.circle(self.screen, self.ENEMY_COLOR,
                               (int(enemy.x), int(enemy.y)), enemy.radius)

    def _draw_player(self) -> None:
        """Draw player"""
        px = self.player_x * self.GRID_SIZE + self.GRID_SIZE // 2
        py = self.player_y * self.GRID_SIZE + self.GRID_SIZE // 2
        pygame.draw.circle(self.screen, self.PLAYER_COLOR, (px, py), self.GRID_SIZE // 2)

    def _draw_ui(self) -> None:
        """Draw UI elements"""
        percentage = self.calculate_percentage()
        self.score_display.draw(
            self.screen, f"Territory: {percentage:.1f}%",
            (10, self.GRID_HEIGHT * self.GRID_SIZE + 10),
            self.TEXT_COLOR
        )

        target_text = self.small_font.render(f"Target: {self.TARGET_PERCENTAGE:.0f}%", True, self.TEXT_COLOR)
        self.screen.blit(target_text, (300, self.GRID_HEIGHT * self.GRID_SIZE + 15))

        controls_text = self.small_font.render("Arrow keys to move | ESC to quit", True, self.TEXT_COLOR)
        self.screen.blit(controls_text, (self.WINDOW_WIDTH - 350, self.GRID_HEIGHT * self.GRID_SIZE + 15))

    def _draw_game_end(self) -> None:
        """Draw game over or victory overlay"""
        percentage = self.calculate_percentage()
        color = self.WIN_COLOR if self.game_won else self.GAME_OVER_COLOR

        self.overlay.draw_overlay(
            title=self.message,
            subtitle=f"Territory Claimed: {percentage:.1f}%",
            instructions="Press SPACE to restart or ESC to quit",
            title_color=color,
            text_color=self.TEXT_COLOR
        )

    def run(self) -> None:
        """Run the Xonix game"""
        self.initialize_display()
        self.reset_game_state()

        while self.running:
            # Event handling
            for event in pygame.event.get():
                self.handle_input(event)

            # Handle movement
            keys = pygame.key.get_pressed()
            self.handle_movement(keys)

            # Update enemies
            if not self.game_over and not self.game_won:
                self.update_enemies()

            # Draw everything
            self.draw_game()

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
