"""
Paratrooper Game
Classic arcade game - defend your turret from paratroopers
"""
import pygame
import random
import math
from games.base_game import BaseGame


class Helicopter:
    """Helicopter that drops paratroopers"""
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # 1 for right, -1 for left
        self.speed = 2
        self.width = 40
        self.height = 20
        self.alive = True
        self.drop_timer = random.randint(30, 60)

    def update(self):
        self.x += self.speed * self.direction
        self.drop_timer -= 1

    def should_drop(self):
        return self.drop_timer <= 0

    def reset_drop_timer(self):
        self.drop_timer = random.randint(40, 80)


class Paratrooper:
    """Falling paratrooper"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1.5
        self.width = 15
        self.height = 20
        self.alive = True
        self.parachute_open = False
        self.parachute_timer = 20

    def update(self):
        if not self.parachute_open:
            self.parachute_timer -= 1
            if self.parachute_timer <= 0:
                self.parachute_open = True

        self.y += self.speed


class Bullet:
    """Bullet fired from turret"""
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 8
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        self.alive = True

    def update(self):
        self.x += self.vx
        self.y += self.vy


class ParatrooperGame(BaseGame):
    """Paratrooper game implementation"""

    def __init__(self):
        self.name_str = "Paratrooper"
        self.description_str = "Defend your turret from paratroopers!"

    @property
    def name(self) -> str:
        return self.name_str

    @property
    def description(self) -> str:
        return self.description_str

    def run(self):
        """Run the Paratrooper game"""
        pygame.init()

        # Constants
        WINDOW_WIDTH = 800
        WINDOW_HEIGHT = 600
        GROUND_HEIGHT = 50

        # Colors
        SKY_COLOR = (135, 206, 235)
        GROUND_COLOR = (139, 69, 19)
        TURRET_COLOR = (50, 50, 50)
        HELI_COLOR = (100, 100, 100)
        PARA_COLOR = (0, 100, 0)
        PARACHUTE_COLOR = (255, 255, 255)
        BULLET_COLOR = (255, 255, 0)
        TEXT_COLOR = (0, 0, 0)
        GAME_OVER_COLOR = (255, 0, 0)

        # Initialize display
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Paratrooper")
        clock = pygame.time.Clock()

        # Fonts
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)

        # Initialize game state
        def init_game():
            turret_x = WINDOW_WIDTH // 2
            turret_y = WINDOW_HEIGHT - GROUND_HEIGHT
            turret_angle = -math.pi / 2  # Point up
            turret_alive = True

            helicopters = []
            paratroopers = []
            bullets = []

            score = 0
            wave = 1
            spawn_timer = 60
            wave_helicopters = 3

            return (turret_x, turret_y, turret_angle, turret_alive,
                   helicopters, paratroopers, bullets,
                   score, wave, spawn_timer, wave_helicopters)

        (turret_x, turret_y, turret_angle, turret_alive,
         helicopters, paratroopers, bullets,
         score, wave, spawn_timer, wave_helicopters) = init_game()

        running = True
        game_over = False
        helis_spawned = 0
        shoot_cooldown = 0

        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif game_over:
                        if event.key == pygame.K_SPACE:
                            (turret_x, turret_y, turret_angle, turret_alive,
                             helicopters, paratroopers, bullets,
                             score, wave, spawn_timer, wave_helicopters) = init_game()
                            game_over = False
                            helis_spawned = 0
                            shoot_cooldown = 0
                    elif event.key == pygame.K_SPACE and turret_alive:
                        if shoot_cooldown <= 0:
                            # Fire bullet
                            barrel_length = 30
                            bullet_x = turret_x + math.cos(turret_angle) * barrel_length
                            bullet_y = turret_y + math.sin(turret_angle) * barrel_length
                            bullets.append(Bullet(bullet_x, bullet_y, turret_angle))
                            shoot_cooldown = 10

            if not game_over:
                # Get keyboard input for turret rotation
                keys = pygame.key.get_pressed()
                if turret_alive:
                    if keys[pygame.K_LEFT]:
                        turret_angle -= 0.05
                        turret_angle = max(turret_angle, -math.pi)
                    elif keys[pygame.K_RIGHT]:
                        turret_angle += 0.05
                        turret_angle = min(turret_angle, 0)

                    # Decrease shoot cooldown
                    if shoot_cooldown > 0:
                        shoot_cooldown -= 1

                # Spawn helicopters
                if helis_spawned < wave_helicopters:
                    spawn_timer -= 1
                    if spawn_timer <= 0:
                        direction = random.choice([-1, 1])
                        x = 0 if direction == 1 else WINDOW_WIDTH
                        y = random.randint(50, 150)
                        helicopters.append(Helicopter(x, y, direction))
                        helis_spawned += 1
                        spawn_timer = random.randint(60, 120)

                # Update helicopters
                for heli in helicopters[:]:
                    if not heli.alive:
                        continue

                    heli.update()

                    # Drop paratrooper
                    if heli.should_drop() and 50 < heli.x < WINDOW_WIDTH - 50:
                        paratroopers.append(Paratrooper(heli.x, heli.y + 10))
                        heli.reset_drop_timer()

                    # Remove if off screen
                    if heli.x < -50 or heli.x > WINDOW_WIDTH + 50:
                        helicopters.remove(heli)

                # Update paratroopers
                for para in paratroopers[:]:
                    if not para.alive:
                        continue

                    para.update()

                    # Check if landed
                    if para.y >= turret_y - 20:
                        # Hit turret
                        turret_alive = False
                        game_over = True
                        paratroopers.remove(para)
                    elif para.y > WINDOW_HEIGHT:
                        paratroopers.remove(para)

                # Update bullets
                for bullet in bullets[:]:
                    if not bullet.alive:
                        continue

                    bullet.update()

                    # Remove if off screen
                    if (bullet.x < 0 or bullet.x > WINDOW_WIDTH or
                        bullet.y < 0 or bullet.y > WINDOW_HEIGHT):
                        bullets.remove(bullet)
                        continue

                    # Check collision with helicopters
                    for heli in helicopters:
                        if not heli.alive:
                            continue
                        if (abs(bullet.x - heli.x) < heli.width // 2 and
                            abs(bullet.y - heli.y) < heli.height // 2):
                            heli.alive = False
                            bullet.alive = False
                            score += 50
                            bullets.remove(bullet)
                            break

                    # Check collision with paratroopers
                    if bullet.alive:
                        for para in paratroopers:
                            if not para.alive:
                                continue
                            if (abs(bullet.x - para.x) < para.width and
                                abs(bullet.y - para.y) < para.height):
                                para.alive = False
                                bullet.alive = False
                                score += 25
                                bullets.remove(bullet)
                                break

                # Check for wave completion
                if (helis_spawned >= wave_helicopters and
                    len(helicopters) == 0 and
                    len(paratroopers) == 0):
                    wave += 1
                    wave_helicopters = min(3 + wave, 8)
                    helis_spawned = 0
                    spawn_timer = 60

            # Drawing
            screen.fill(SKY_COLOR)

            # Draw ground
            pygame.draw.rect(screen, GROUND_COLOR,
                           (0, WINDOW_HEIGHT - GROUND_HEIGHT, WINDOW_WIDTH, GROUND_HEIGHT))

            # Draw turret base
            if turret_alive:
                pygame.draw.circle(screen, TURRET_COLOR, (turret_x, turret_y), 20)

                # Draw turret barrel
                barrel_length = 30
                barrel_end_x = turret_x + math.cos(turret_angle) * barrel_length
                barrel_end_y = turret_y + math.sin(turret_angle) * barrel_length
                pygame.draw.line(screen, TURRET_COLOR, (turret_x, turret_y),
                               (barrel_end_x, barrel_end_y), 6)
            else:
                # Draw destroyed turret
                pygame.draw.circle(screen, (100, 100, 100), (turret_x, turret_y), 20)
                pygame.draw.line(screen, (255, 0, 0), (turret_x - 15, turret_y - 15),
                               (turret_x + 15, turret_y + 15), 3)
                pygame.draw.line(screen, (255, 0, 0), (turret_x - 15, turret_y + 15),
                               (turret_x + 15, turret_y - 15), 3)

            # Draw helicopters
            for heli in helicopters:
                if not heli.alive:
                    continue
                # Body
                rect = pygame.Rect(heli.x - heli.width // 2, heli.y - heli.height // 2,
                                  heli.width, heli.height)
                pygame.draw.ellipse(screen, HELI_COLOR, rect)
                # Rotor
                rotor_y = heli.y - heli.height // 2 - 5
                pygame.draw.line(screen, (50, 50, 50),
                               (heli.x - 20, rotor_y), (heli.x + 20, rotor_y), 2)

            # Draw paratroopers
            for para in paratroopers:
                if not para.alive:
                    continue

                # Draw parachute if open
                if para.parachute_open:
                    chute_points = [
                        (para.x, para.y - 15),
                        (para.x - 15, para.y - 5),
                        (para.x - 10, para.y),
                        (para.x + 10, para.y),
                        (para.x + 15, para.y - 5)
                    ]
                    pygame.draw.polygon(screen, PARACHUTE_COLOR, chute_points)
                    pygame.draw.lines(screen, PARA_COLOR, False,
                                    [(para.x - 10, para.y), (para.x, para.y + 10),
                                     (para.x + 10, para.y)], 2)

                # Draw paratrooper body
                pygame.draw.circle(screen, PARA_COLOR, (int(para.x), int(para.y + 10)), 5)
                pygame.draw.line(screen, PARA_COLOR, (para.x, para.y + 10),
                               (para.x, para.y + 20), 2)

            # Draw bullets
            for bullet in bullets:
                if bullet.alive:
                    pygame.draw.circle(screen, BULLET_COLOR, (int(bullet.x), int(bullet.y)), 3)

            # Draw UI
            score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
            screen.blit(score_text, (10, 10))

            wave_text = small_font.render(f"Wave: {wave}", True, TEXT_COLOR)
            screen.blit(wave_text, (10, 50))

            controls_text = small_font.render("Left/Right: Aim | Space: Shoot | ESC: Quit", True, TEXT_COLOR)
            screen.blit(controls_text, (WINDOW_WIDTH - 400, 10))

            # Draw game over message
            if game_over:
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))

                game_over_text = font.render("GAME OVER!", True, GAME_OVER_COLOR)
                game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
                screen.blit(game_over_text, game_over_rect)

                final_score_text = font.render(f"Final Score: {score}", True, TEXT_COLOR)
                final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                screen.blit(final_score_text, final_score_rect)

                wave_reached_text = small_font.render(f"Waves Survived: {wave - 1}", True, TEXT_COLOR)
                wave_reached_rect = wave_reached_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 35))
                screen.blit(wave_reached_text, wave_reached_rect)

                restart_text = small_font.render("Press SPACE to restart or ESC to quit", True, TEXT_COLOR)
                restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
                screen.blit(restart_text, restart_rect)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
