"""
Paratrooper Game
Classic arcade game - defend your turret from paratroopers
"""

import math
import random

import pygame

from common.constants import BLACK, DEFAULT_FPS, RED, WHITE, YELLOW
from common.high_scores import get_high_score_manager
from common.ui import GameOverlay, ScoreDisplay
from games.base_game import BaseGame


class Helicopter:
    """Helicopter that drops paratroopers"""

    def __init__(self, x: float, y: float, direction: int, speed: float = 2.0):
        self.x = x
        self.y = y
        self.direction = direction  # 1 for right, -1 for left
        self.speed = speed
        self.width = 40
        self.height = 20
        self.alive = True
        self.drop_timer = random.randint(30, 60)

    def update(self) -> None:
        """Update helicopter position and timers"""
        self.x += self.speed * self.direction
        self.drop_timer -= 1

    def should_drop(self) -> bool:
        """Check if it's time to drop a paratrooper"""
        return self.drop_timer <= 0

    def reset_drop_timer(self) -> None:
        """Reset the drop timer after dropping"""
        self.drop_timer = random.randint(40, 80)


class Paratrooper:
    """Falling paratrooper"""

    def __init__(self, x: float, y: float, speed: float = 1.5):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 15
        self.height = 20
        self.alive = True
        self.parachute_open = False
        self.parachute_timer = 20

    def update(self) -> None:
        """Update paratrooper position and parachute state"""
        if not self.parachute_open:
            self.parachute_timer -= 1
            if self.parachute_timer <= 0:
                self.parachute_open = True
        self.y += self.speed


class Bullet:
    """Bullet fired from turret"""

    def __init__(self, x: float, y: float, angle: float, speed: float = 8.0):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        self.alive = True

    def update(self) -> None:
        """Update bullet position"""
        self.x += self.vx
        self.y += self.vy


class ParatrooperGame(BaseGame):
    """Paratrooper game implementation"""

    # Class-level metadata
    GAME_NAME = "Paratrooper"
    GAME_DESCRIPTION = "Defend your turret from paratroopers!"

    # Window constants
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    GROUND_HEIGHT = 50

    # Colors
    SKY_COLOR = (135, 206, 235)
    GROUND_COLOR = (139, 69, 19)
    TURRET_COLOR = (50, 50, 50)
    HELI_COLOR = (100, 100, 100)
    PARA_COLOR = (0, 100, 0)
    PARACHUTE_COLOR = WHITE
    BULLET_COLOR = YELLOW
    TEXT_COLOR = BLACK
    GAME_OVER_COLOR = RED

    # Game settings
    INITIAL_WAVE_HELICOPTERS = 3
    MAX_WAVE_HELICOPTERS = 8
    BARREL_LENGTH = 30
    SHOOT_COOLDOWN = 10
    HELI_SCORE = 50
    PARA_SCORE = 25

    def __init__(self):
        """Initialize the Paratrooper game"""
        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self.font: pygame.font.Font | None = None
        self.small_font: pygame.font.Font | None = None
        self.overlay: GameOverlay | None = None
        self.score_display: ScoreDisplay | None = None
        self.high_score_manager = get_high_score_manager()

        # Game state
        self.turret_x: int = 0
        self.turret_y: int = 0
        self.turret_angle: float = 0.0
        self.turret_alive: bool = True

        self.helicopters: list[Helicopter] = []
        self.paratroopers: list[Paratrooper] = []
        self.bullets: list[Bullet] = []

        self.score: int = 0
        self.wave: int = 1
        self.spawn_timer: int = 60
        self.wave_helicopters: int = self.INITIAL_WAVE_HELICOPTERS
        self.helis_spawned: int = 0
        self.shoot_cooldown: int = 0

        self.running: bool = True
        self.game_over: bool = False
        self.paused: bool = False
        self.is_new_high_score: bool = False
        self.score_saved: bool = False

    def initialize_display(self) -> None:
        """Initialize pygame display and fonts"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Paratrooper")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.overlay = GameOverlay(self.screen)
        self.score_display = ScoreDisplay()

    def reset_game_state(self) -> None:
        """Reset game state to initial values"""
        self.turret_x = self.WINDOW_WIDTH // 2
        self.turret_y = self.WINDOW_HEIGHT - self.GROUND_HEIGHT
        self.turret_angle = -math.pi / 2  # Point up
        self.turret_alive = True

        self.helicopters = []
        self.paratroopers = []
        self.bullets = []

        self.score = 0
        self.wave = 1
        self.spawn_timer = 60
        self.wave_helicopters = self.INITIAL_WAVE_HELICOPTERS
        self.helis_spawned = 0
        self.shoot_cooldown = 0
        self.game_over = False
        self.is_new_high_score = False
        self.score_saved = False

    def save_high_score(self) -> None:
        """Save the current score to high scores"""
        if not self.score_saved:
            self.is_new_high_score = self.high_score_manager.add_score(
                self.GAME_NAME, self.score, wave=self.wave
            )
            self.score_saved = True

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handle keyboard input"""
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_p and not self.game_over:
                self.paused = not self.paused
            elif self.game_over and event.key == pygame.K_SPACE:
                self.reset_game_state()
            elif (
                event.key == pygame.K_SPACE
                and self.turret_alive
                and self.shoot_cooldown <= 0
                and not self.paused
            ):
                self._fire_bullet()

    def _fire_bullet(self) -> None:
        """Fire a bullet from the turret"""
        bullet_x = self.turret_x + math.cos(self.turret_angle) * self.BARREL_LENGTH
        bullet_y = self.turret_y + math.sin(self.turret_angle) * self.BARREL_LENGTH
        self.bullets.append(Bullet(bullet_x, bullet_y, self.turret_angle))
        self.shoot_cooldown = self.SHOOT_COOLDOWN

    def handle_turret_rotation(self, keys) -> None:
        """Handle turret rotation based on keyboard input"""
        if not self.turret_alive or self.paused:
            return

        if keys[pygame.K_LEFT]:
            self.turret_angle -= 0.05
            self.turret_angle = max(self.turret_angle, -math.pi)
        elif keys[pygame.K_RIGHT]:
            self.turret_angle += 0.05
            self.turret_angle = min(self.turret_angle, 0)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def spawn_helicopters(self) -> None:
        """Spawn helicopters based on wave settings"""
        if self.helis_spawned < self.wave_helicopters:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                direction = random.choice([-1, 1])
                x = 0.0 if direction == 1 else float(self.WINDOW_WIDTH)
                y = float(random.randint(50, 150))
                self.helicopters.append(Helicopter(x, y, direction))
                self.helis_spawned += 1
                self.spawn_timer = random.randint(60, 120)

    def update_helicopters(self) -> None:
        """Update all helicopters"""
        for heli in self.helicopters[:]:
            if not heli.alive:
                continue

            heli.update()

            # Drop paratrooper
            if heli.should_drop() and 50 < heli.x < self.WINDOW_WIDTH - 50:
                self.paratroopers.append(Paratrooper(heli.x, heli.y + 10))
                heli.reset_drop_timer()

            # Remove if off screen
            if heli.x < -50 or heli.x > self.WINDOW_WIDTH + 50:
                self.helicopters.remove(heli)

    def update_paratroopers(self) -> None:
        """Update all paratroopers"""
        for para in self.paratroopers[:]:
            if not para.alive:
                continue

            para.update()

            # Check if landed on turret
            if para.y >= self.turret_y - 20:
                self.turret_alive = False
                self.game_over = True
                self.save_high_score()
                self.paratroopers.remove(para)
            elif para.y > self.WINDOW_HEIGHT:
                self.paratroopers.remove(para)

    def update_bullets(self) -> None:
        """Update all bullets and check collisions"""
        for bullet in self.bullets[:]:
            if not bullet.alive:
                continue

            bullet.update()

            # Remove if off screen
            if (
                bullet.x < 0
                or bullet.x > self.WINDOW_WIDTH
                or bullet.y < 0
                or bullet.y > self.WINDOW_HEIGHT
            ):
                self.bullets.remove(bullet)
                continue

            # Check collision with helicopters
            if self._check_bullet_helicopter_collision(bullet):
                continue

            # Check collision with paratroopers
            self._check_bullet_paratrooper_collision(bullet)

    def _check_bullet_helicopter_collision(self, bullet: Bullet) -> bool:
        """Check if bullet hits any helicopter, returns True if hit occurred"""
        for heli in self.helicopters:
            if not heli.alive:
                continue
            if (
                abs(bullet.x - heli.x) < heli.width // 2
                and abs(bullet.y - heli.y) < heli.height // 2
            ):
                heli.alive = False
                bullet.alive = False
                self.score += self.HELI_SCORE
                self.bullets.remove(bullet)
                return True
        return False

    def _check_bullet_paratrooper_collision(self, bullet: Bullet) -> None:
        """Check if bullet hits any paratrooper"""
        if not bullet.alive:
            return

        for para in self.paratroopers:
            if not para.alive:
                continue
            if abs(bullet.x - para.x) < para.width and abs(bullet.y - para.y) < para.height:
                para.alive = False
                bullet.alive = False
                self.score += self.PARA_SCORE
                self.bullets.remove(bullet)
                break

    def check_wave_completion(self) -> None:
        """Check if wave is complete and advance to next wave"""
        if (
            self.helis_spawned >= self.wave_helicopters
            and len(self.helicopters) == 0
            and len(self.paratroopers) == 0
        ):
            self.wave += 1
            self.wave_helicopters = min(
                self.INITIAL_WAVE_HELICOPTERS + self.wave, self.MAX_WAVE_HELICOPTERS
            )
            self.helis_spawned = 0
            self.spawn_timer = 60

    def draw_game(self) -> None:
        """Draw the game state"""
        assert self.screen is not None
        self.screen.fill(self.SKY_COLOR)
        self._draw_ground()
        self._draw_turret()
        self._draw_helicopters()
        self._draw_paratroopers()
        self._draw_bullets()
        self._draw_ui()

        if self.game_over:
            self._draw_game_over()
        elif self.paused:
            self._draw_pause_overlay()

    def _draw_ground(self) -> None:
        """Draw the ground"""
        assert self.screen is not None
        pygame.draw.rect(
            self.screen,
            self.GROUND_COLOR,
            (0, self.WINDOW_HEIGHT - self.GROUND_HEIGHT, self.WINDOW_WIDTH, self.GROUND_HEIGHT),
        )

    def _draw_turret(self) -> None:
        """Draw the turret"""
        assert self.screen is not None
        if self.turret_alive:
            # Draw turret base
            pygame.draw.circle(self.screen, self.TURRET_COLOR, (self.turret_x, self.turret_y), 20)

            # Draw turret barrel
            barrel_end_x = self.turret_x + math.cos(self.turret_angle) * self.BARREL_LENGTH
            barrel_end_y = self.turret_y + math.sin(self.turret_angle) * self.BARREL_LENGTH
            pygame.draw.line(
                self.screen,
                self.TURRET_COLOR,
                (self.turret_x, self.turret_y),
                (barrel_end_x, barrel_end_y),
                6,
            )
        else:
            # Draw destroyed turret
            pygame.draw.circle(self.screen, (100, 100, 100), (self.turret_x, self.turret_y), 20)
            pygame.draw.line(
                self.screen,
                RED,
                (self.turret_x - 15, self.turret_y - 15),
                (self.turret_x + 15, self.turret_y + 15),
                3,
            )
            pygame.draw.line(
                self.screen,
                RED,
                (self.turret_x - 15, self.turret_y + 15),
                (self.turret_x + 15, self.turret_y - 15),
                3,
            )

    def _draw_helicopters(self) -> None:
        """Draw all helicopters"""
        assert self.screen is not None
        for heli in self.helicopters:
            if not heli.alive:
                continue
            # Body
            rect = pygame.Rect(
                heli.x - heli.width // 2, heli.y - heli.height // 2, heli.width, heli.height
            )
            pygame.draw.ellipse(self.screen, self.HELI_COLOR, rect)
            # Rotor
            rotor_y = heli.y - heli.height // 2 - 5
            pygame.draw.line(
                self.screen, (50, 50, 50), (heli.x - 20, rotor_y), (heli.x + 20, rotor_y), 2
            )

    def _draw_paratroopers(self) -> None:
        """Draw all paratroopers"""
        assert self.screen is not None
        for para in self.paratroopers:
            if not para.alive:
                continue

            # Draw parachute if open
            if para.parachute_open:
                chute_points = [
                    (para.x, para.y - 15),
                    (para.x - 15, para.y - 5),
                    (para.x - 10, para.y),
                    (para.x + 10, para.y),
                    (para.x + 15, para.y - 5),
                ]
                pygame.draw.polygon(self.screen, self.PARACHUTE_COLOR, chute_points)
                pygame.draw.lines(
                    self.screen,
                    self.PARA_COLOR,
                    False,
                    [(para.x - 10, para.y), (para.x, para.y + 10), (para.x + 10, para.y)],
                    2,
                )

            # Draw paratrooper body
            pygame.draw.circle(self.screen, self.PARA_COLOR, (int(para.x), int(para.y + 10)), 5)
            pygame.draw.line(
                self.screen, self.PARA_COLOR, (para.x, para.y + 10), (para.x, para.y + 20), 2
            )

    def _draw_bullets(self) -> None:
        """Draw all bullets"""
        assert self.screen is not None
        for bullet in self.bullets:
            if bullet.alive:
                pygame.draw.circle(
                    self.screen, self.BULLET_COLOR, (int(bullet.x), int(bullet.y)), 3
                )

    def _draw_ui(self) -> None:
        """Draw UI elements"""
        assert self.screen is not None
        assert self.score_display is not None
        assert self.small_font is not None
        self.score_display.draw(self.screen, f"Score: {self.score}", (10, 10), self.TEXT_COLOR)

        wave_text = self.small_font.render(f"Wave: {self.wave}", True, self.TEXT_COLOR)
        self.screen.blit(wave_text, (10, 50))

        # Display high score
        best_score = self.high_score_manager.get_best_score(self.GAME_NAME)
        if best_score is not None:
            high_score_text = self.small_font.render(f"Best: {best_score}", True, self.TEXT_COLOR)
            self.screen.blit(high_score_text, (10, 80))

        controls_text = self.small_font.render(
            "Left/Right: Aim | Space: Shoot | P: Pause | ESC: Quit", True, self.TEXT_COLOR
        )
        self.screen.blit(controls_text, (self.WINDOW_WIDTH - 400, 10))

    def _draw_game_over(self) -> None:
        """Draw game over overlay"""
        assert self.overlay is not None
        subtitle = f"Final Score: {self.score} | Waves: {self.wave - 1}"
        if self.is_new_high_score:
            subtitle += " - NEW HIGH SCORE!"

        self.overlay.draw_overlay(
            title="GAME OVER!",
            subtitle=subtitle,
            instructions="Press SPACE to restart or ESC to quit",
            title_color=self.GAME_OVER_COLOR,
            text_color=BLACK,
        )

    def _draw_pause_overlay(self) -> None:
        """Draw pause overlay"""
        assert self.overlay is not None
        self.overlay.draw_overlay(
            title="PAUSED",
            subtitle=f"Score: {self.score} | Wave: {self.wave}",
            instructions="Press P to resume or ESC to quit",
            title_color=YELLOW,
            text_color=BLACK,
        )

    def run(self) -> None:
        """Run the Paratrooper game"""
        self.initialize_display()
        self.reset_game_state()

        assert self.clock is not None
        while self.running:
            # Event handling
            for event in pygame.event.get():
                self.handle_input(event)

            if not self.game_over and not self.paused:
                # Handle turret rotation
                keys = pygame.key.get_pressed()
                self.handle_turret_rotation(keys)

                # Spawn and update enemies
                self.spawn_helicopters()
                self.update_helicopters()
                self.update_paratroopers()
                self.update_bullets()
                self.check_wave_completion()

            # Draw everything
            self.draw_game()

            pygame.display.flip()
            self.clock.tick(DEFAULT_FPS)

        pygame.quit()
