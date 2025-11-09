"""
Xonix Game
Claim territory by drawing lines while avoiding enemies
"""
import pygame
import random
from games.base_game import BaseGame


class Enemy:
    """Enemy ball that bounces around"""
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 8


class XonixGame(BaseGame):
    """Xonix game implementation"""

    def __init__(self):
        self.name_str = "Xonix"
        self.description_str = "Claim 75% territory while avoiding enemies!"

    @property
    def name(self) -> str:
        return self.name_str

    @property
    def description(self) -> str:
        return self.description_str

    def run(self):
        """Run the Xonix game"""
        pygame.init()

        # Constants
        GRID_SIZE = 10
        GRID_WIDTH = 70
        GRID_HEIGHT = 50
        WINDOW_WIDTH = GRID_SIZE * GRID_WIDTH
        WINDOW_HEIGHT = GRID_SIZE * GRID_HEIGHT + 60

        # Colors
        BG_COLOR = (0, 0, 0)
        CLAIMED_COLOR = (0, 100, 200)
        BORDER_COLOR = (0, 150, 255)
        PLAYER_COLOR = (0, 255, 0)
        TRAIL_COLOR = (255, 255, 0)
        ENEMY_COLOR = (255, 0, 0)
        TEXT_COLOR = (255, 255, 255)
        GAME_OVER_COLOR = (255, 100, 100)
        WIN_COLOR = (0, 255, 0)

        # Cell states
        EMPTY = 0
        CLAIMED = 1
        BORDER = 2
        TRAIL = 3

        # Initialize display
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Xonix")
        clock = pygame.time.Clock()

        # Fonts
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)

        # Initialize game state
        def init_game():
            # Create grid
            grid = [[EMPTY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

            # Create border
            for x in range(GRID_WIDTH):
                grid[0][x] = BORDER
                grid[GRID_HEIGHT - 1][x] = BORDER
            for y in range(GRID_HEIGHT):
                grid[y][0] = BORDER
                grid[y][GRID_WIDTH - 1] = BORDER

            # Player starts on border
            player_x = GRID_WIDTH // 2
            player_y = 0

            # Create enemies
            enemies = []
            for _ in range(3):
                x = random.randint(GRID_WIDTH // 4, 3 * GRID_WIDTH // 4) * GRID_SIZE
                y = random.randint(GRID_HEIGHT // 4, 3 * GRID_HEIGHT // 4) * GRID_SIZE
                vx = random.choice([-2, 2])
                vy = random.choice([-2, 2])
                enemies.append(Enemy(x, y, vx, vy))

            return grid, player_x, player_y, enemies, [], False, 0

        grid, player_x, player_y, enemies, trail, drawing, score = init_game()

        running = True
        game_over = False
        game_won = False
        message = ""

        def get_cell_state(x, y):
            """Get state of cell at position"""
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                return grid[y][x]
            return BORDER

        def is_on_border_or_claimed(x, y):
            """Check if position is on border or claimed territory"""
            state = get_cell_state(x, y)
            return state in [BORDER, CLAIMED]

        def flood_fill(start_x, start_y, enemies):
            """Flood fill to find unclaimed area reachable by enemies"""
            visited = set()
            stack = [(start_x, start_y)]
            area = []

            while stack:
                x, y = stack.pop()
                if (x, y) in visited:
                    continue
                if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
                    continue
                if grid[y][x] != EMPTY:
                    continue

                visited.add((x, y))
                area.append((x, y))

                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    stack.append((x + dx, y + dy))

            # Check if any enemy is in this area
            has_enemy = False
            for enemy in enemies:
                ex, ey = int(enemy.x // GRID_SIZE), int(enemy.y // GRID_SIZE)
                if (ex, ey) in visited:
                    has_enemy = True
                    break

            return area, has_enemy

        def claim_territory():
            """Claim territory after completing a trail"""
            # Mark trail as border
            for x, y in trail:
                grid[y][x] = BORDER

            # Find all empty regions and claim those without enemies
            for y in range(1, GRID_HEIGHT - 1):
                for x in range(1, GRID_WIDTH - 1):
                    if grid[y][x] == EMPTY:
                        area, has_enemy = flood_fill(x, y, enemies)
                        if not has_enemy and area:
                            # Claim this area
                            for ax, ay in area:
                                grid[ay][ax] = CLAIMED

        def calculate_percentage():
            """Calculate percentage of claimed territory"""
            total = (GRID_WIDTH - 2) * (GRID_HEIGHT - 2)
            claimed = sum(1 for y in range(1, GRID_HEIGHT - 1)
                         for x in range(1, GRID_WIDTH - 1)
                         if grid[y][x] in [CLAIMED, BORDER])
            return (claimed / total) * 100 if total > 0 else 0

        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif game_over or game_won:
                        if event.key == pygame.K_SPACE:
                            grid, player_x, player_y, enemies, trail, drawing, score = init_game()
                            game_over = False
                            game_won = False
                            message = ""

            if not game_over and not game_won:
                # Get keyboard input
                keys = pygame.key.get_pressed()
                moved = False
                new_x, new_y = player_x, player_y

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

                if moved:
                    # Check bounds
                    if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                        # Check if moving into empty space (start drawing)
                        if not drawing and get_cell_state(new_x, new_y) == EMPTY:
                            drawing = True
                            trail = [(new_x, new_y)]
                            player_x, player_y = new_x, new_y
                        # Check if drawing and hit trail (game over)
                        elif drawing and (new_x, new_y) in trail:
                            game_over = True
                            message = "Hit your own trail!"
                        # Check if drawing and hit border/claimed (complete)
                        elif drawing and is_on_border_or_claimed(new_x, new_y):
                            drawing = False
                            claim_territory()
                            trail = []
                            player_x, player_y = new_x, new_y
                            score = calculate_percentage()
                            if score >= 75:
                                game_won = True
                                message = "Victory!"
                        # Continue drawing
                        elif drawing and get_cell_state(new_x, new_y) == EMPTY:
                            trail.append((new_x, new_y))
                            player_x, player_y = new_x, new_y
                        # Moving on safe territory
                        elif not drawing:
                            player_x, player_y = new_x, new_y

                # Update enemies
                for enemy in enemies:
                    enemy.x += enemy.vx
                    enemy.y += enemy.vy

                    # Check wall collisions
                    ex, ey = int(enemy.x // GRID_SIZE), int(enemy.y // GRID_SIZE)

                    # Bounce off walls and claimed territory
                    if (enemy.x <= enemy.radius or enemy.x >= WINDOW_WIDTH - enemy.radius or
                        (0 <= ex < GRID_WIDTH and 0 <= ey < GRID_HEIGHT and
                         grid[ey][ex] in [BORDER, CLAIMED])):
                        enemy.vx = -enemy.vx
                        enemy.x += enemy.vx * 2

                    if (enemy.y <= enemy.radius or enemy.y >= GRID_HEIGHT * GRID_SIZE - enemy.radius or
                        (0 <= ex < GRID_WIDTH and 0 <= ey < GRID_HEIGHT and
                         grid[ey][ex] in [BORDER, CLAIMED])):
                        enemy.vy = -enemy.vy
                        enemy.y += enemy.vy * 2

                    # Check collision with player trail
                    if drawing:
                        for tx, ty in trail:
                            tx_pixel, ty_pixel = tx * GRID_SIZE, ty * GRID_SIZE
                            dist_sq = (enemy.x - tx_pixel) ** 2 + (enemy.y - ty_pixel) ** 2
                            if dist_sq < (enemy.radius + GRID_SIZE // 2) ** 2:
                                game_over = True
                                message = "Enemy hit your trail!"
                                break

                    # Check collision with player
                    px_pixel, py_pixel = player_x * GRID_SIZE, player_y * GRID_SIZE
                    dist_sq = (enemy.x - px_pixel) ** 2 + (enemy.y - py_pixel) ** 2
                    if drawing and dist_sq < (enemy.radius + GRID_SIZE // 2) ** 2:
                        game_over = True
                        message = "Enemy hit you!"

            # Drawing
            screen.fill(BG_COLOR)

            # Draw grid
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    if grid[y][x] == CLAIMED:
                        pygame.draw.rect(screen, CLAIMED_COLOR, rect)
                    elif grid[y][x] == BORDER:
                        pygame.draw.rect(screen, BORDER_COLOR, rect)

            # Draw trail
            for x, y in trail:
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, TRAIL_COLOR, rect)

            # Draw enemies
            for enemy in enemies:
                pygame.draw.circle(screen, ENEMY_COLOR, (int(enemy.x), int(enemy.y)), enemy.radius)

            # Draw player
            px, py = player_x * GRID_SIZE + GRID_SIZE // 2, player_y * GRID_SIZE + GRID_SIZE // 2
            pygame.draw.circle(screen, PLAYER_COLOR, (px, py), GRID_SIZE // 2)

            # Draw UI
            percentage = calculate_percentage()
            score_text = font.render(f"Territory: {percentage:.1f}%", True, TEXT_COLOR)
            screen.blit(score_text, (10, GRID_HEIGHT * GRID_SIZE + 10))

            target_text = small_font.render("Target: 75%", True, TEXT_COLOR)
            screen.blit(target_text, (300, GRID_HEIGHT * GRID_SIZE + 15))

            controls_text = small_font.render("Arrow keys to move | ESC to quit", True, TEXT_COLOR)
            screen.blit(controls_text, (WINDOW_WIDTH - 350, GRID_HEIGHT * GRID_SIZE + 15))

            # Draw game over/won message
            if game_over or game_won:
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))

                color = WIN_COLOR if game_won else GAME_OVER_COLOR
                status_text = font.render(message, True, color)
                status_rect = status_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
                screen.blit(status_text, status_rect)

                final_score_text = font.render(f"Territory Claimed: {percentage:.1f}%", True, TEXT_COLOR)
                final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
                screen.blit(final_score_text, final_score_rect)

                restart_text = small_font.render("Press SPACE to restart or ESC to quit", True, TEXT_COLOR)
                restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
                screen.blit(restart_text, restart_rect)

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
