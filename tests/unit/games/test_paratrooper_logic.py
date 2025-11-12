"""
Comprehensive unit tests for Paratrooper game logic
"""

import math
import unittest
from unittest.mock import Mock

import pygame

from src.games.paratrooper.game import Bullet, Helicopter, Paratrooper, ParatrooperGame


class TestHelicopter(unittest.TestCase):
    """Test Helicopter class"""

    def test_helicopter_initialization(self):
        """Test helicopter initializes with correct values"""
        heli = Helicopter(100, 200, 1, 3.0)
        self.assertEqual(heli.x, 100)
        self.assertEqual(heli.y, 200)
        self.assertEqual(heli.direction, 1)
        self.assertEqual(heli.speed, 3.0)
        self.assertTrue(heli.alive)
        self.assertGreater(heli.drop_timer, 0)

    def test_helicopter_default_speed(self):
        """Test helicopter has default speed"""
        heli = Helicopter(0, 0, 1)
        self.assertEqual(heli.speed, 2.0)

    def test_helicopter_update(self):
        """Test helicopter updates position and timer"""
        heli = Helicopter(100, 200, 1, 2.0)
        initial_timer = heli.drop_timer

        heli.update()

        # Position should change
        self.assertEqual(heli.x, 102)  # 100 + 2.0 * 1
        self.assertEqual(heli.y, 200)
        # Timer should decrease
        self.assertEqual(heli.drop_timer, initial_timer - 1)

    def test_helicopter_movement_direction(self):
        """Test helicopter moves in correct direction"""
        # Moving right
        heli_right = Helicopter(100, 100, 1, 2.0)
        heli_right.update()
        self.assertGreater(heli_right.x, 100)

        # Moving left
        heli_left = Helicopter(100, 100, -1, 2.0)
        heli_left.update()
        self.assertLess(heli_left.x, 100)

    def test_helicopter_should_drop(self):
        """Test should_drop returns correct value"""
        heli = Helicopter(100, 100, 1)

        # Initially should not drop
        heli.drop_timer = 10
        self.assertFalse(heli.should_drop())

        # Should drop when timer is 0
        heli.drop_timer = 0
        self.assertTrue(heli.should_drop())

        # Should drop when timer is negative
        heli.drop_timer = -1
        self.assertTrue(heli.should_drop())

    def test_helicopter_reset_drop_timer(self):
        """Test reset_drop_timer sets a new timer"""
        heli = Helicopter(100, 100, 1)
        heli.drop_timer = 0

        heli.reset_drop_timer()

        self.assertGreater(heli.drop_timer, 0)
        # Should be within expected range
        self.assertGreaterEqual(heli.drop_timer, 40)
        self.assertLessEqual(heli.drop_timer, 80)


class TestParatrooper(unittest.TestCase):
    """Test Paratrooper class"""

    def test_paratrooper_initialization(self):
        """Test paratrooper initializes with correct values"""
        para = Paratrooper(150, 250, 2.0)
        self.assertEqual(para.x, 150)
        self.assertEqual(para.y, 250)
        self.assertEqual(para.speed, 2.0)
        self.assertTrue(para.alive)
        self.assertFalse(para.parachute_open)
        self.assertGreater(para.parachute_timer, 0)

    def test_paratrooper_default_speed(self):
        """Test paratrooper has default speed"""
        para = Paratrooper(0, 0)
        self.assertEqual(para.speed, 1.5)

    def test_paratrooper_update_falling(self):
        """Test paratrooper falls"""
        para = Paratrooper(100, 100, 2.0)
        initial_y = para.y

        para.update()

        # Should fall downward
        self.assertEqual(para.y, initial_y + 2.0)

    def test_paratrooper_parachute_opens(self):
        """Test parachute opens after timer"""
        para = Paratrooper(100, 100)
        para.parachute_timer = 2

        # First update
        para.update()
        self.assertFalse(para.parachute_open)
        self.assertEqual(para.parachute_timer, 1)

        # Second update - parachute should open when timer reaches 0
        para.update()
        self.assertTrue(para.parachute_open)
        self.assertEqual(para.parachute_timer, 0)


class TestBullet(unittest.TestCase):
    """Test Bullet class"""

    def test_bullet_initialization(self):
        """Test bullet initializes with correct values"""
        angle = math.pi / 4  # 45 degrees
        bullet = Bullet(100, 200, angle, 10.0)

        self.assertEqual(bullet.x, 100)
        self.assertEqual(bullet.y, 200)
        self.assertEqual(bullet.angle, angle)
        self.assertEqual(bullet.speed, 10.0)
        self.assertTrue(bullet.alive)

        # Velocity should be calculated correctly
        expected_vx = math.cos(angle) * 10.0
        expected_vy = math.sin(angle) * 10.0
        self.assertAlmostEqual(bullet.vx, expected_vx)
        self.assertAlmostEqual(bullet.vy, expected_vy)

    def test_bullet_default_speed(self):
        """Test bullet has default speed"""
        bullet = Bullet(0, 0, 0)
        self.assertEqual(bullet.speed, 8.0)

    def test_bullet_update(self):
        """Test bullet updates position"""
        bullet = Bullet(100, 100, 0, 5.0)  # Angle 0 = horizontal right

        bullet.update()

        # Should move right
        self.assertGreater(bullet.x, 100)
        # Y should stay same for horizontal shot
        self.assertAlmostEqual(bullet.y, 100, places=1)

    def test_bullet_velocity_directions(self):
        """Test bullet velocity in different directions"""
        # Up (negative pi/2)
        bullet_up = Bullet(100, 100, -math.pi / 2, 10.0)
        self.assertAlmostEqual(bullet_up.vx, 0, places=5)
        self.assertLess(bullet_up.vy, 0)  # Negative Y is up

        # Right (0)
        bullet_right = Bullet(100, 100, 0, 10.0)
        self.assertGreater(bullet_right.vx, 0)
        self.assertAlmostEqual(bullet_right.vy, 0, places=5)


class TestParatrooperGameLogic(unittest.TestCase):
    """Test Paratrooper game logic without requiring display"""

    def setUp(self):
        """Set up test fixtures"""
        self.game = ParatrooperGame()
        # Mock display to avoid pygame window creation
        self.game.screen = Mock(spec=pygame.Surface)
        self.game.clock = Mock(spec=pygame.time.Clock)
        self.game.font = Mock(spec=pygame.font.Font)
        self.game.small_font = Mock(spec=pygame.font.Font)
        self.game.overlay = Mock()
        self.game.score_display = Mock()

    def test_initialization(self):
        """Test game initializes with correct default values"""
        game = ParatrooperGame()
        self.assertEqual(game.score, 0)
        self.assertEqual(game.wave, 1)
        self.assertTrue(game.running)
        self.assertFalse(game.game_over)
        self.assertTrue(game.turret_alive)
        self.assertEqual(len(game.helicopters), 0)
        self.assertEqual(len(game.paratroopers), 0)
        self.assertEqual(len(game.bullets), 0)

    def test_reset_game_state(self):
        """Test game state resets correctly"""
        # Modify game state
        self.game.score = 1000
        self.game.wave = 5
        self.game.game_over = True
        self.game.turret_alive = False
        self.game.helicopters = [Helicopter(100, 100, 1)]
        self.game.paratroopers = [Paratrooper(100, 100)]
        self.game.bullets = [Bullet(100, 100, 0)]

        # Reset
        self.game.reset_game_state()

        # Verify reset
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.wave, 1)
        self.assertFalse(self.game.game_over)
        self.assertTrue(self.game.turret_alive)
        self.assertEqual(len(self.game.helicopters), 0)
        self.assertEqual(len(self.game.paratroopers), 0)
        self.assertEqual(len(self.game.bullets), 0)

        # Turret should be positioned correctly
        self.assertEqual(self.game.turret_x, ParatrooperGame.WINDOW_WIDTH // 2)
        self.assertEqual(
            self.game.turret_y, ParatrooperGame.WINDOW_HEIGHT - ParatrooperGame.GROUND_HEIGHT
        )
        self.assertAlmostEqual(self.game.turret_angle, -math.pi / 2)

    def test_fire_bullet(self):
        """Test firing a bullet"""
        self.game.reset_game_state()
        initial_bullets = len(self.game.bullets)

        self.game._fire_bullet()

        # Should have one more bullet
        self.assertEqual(len(self.game.bullets), initial_bullets + 1)
        # Cooldown should be set
        self.assertEqual(self.game.shoot_cooldown, ParatrooperGame.SHOOT_COOLDOWN)

        # Bullet should be positioned at barrel end
        bullet = self.game.bullets[0]
        expected_x = self.game.turret_x + math.cos(self.game.turret_angle) * self.game.BARREL_LENGTH
        expected_y = self.game.turret_y + math.sin(self.game.turret_angle) * self.game.BARREL_LENGTH
        self.assertAlmostEqual(bullet.x, expected_x)
        self.assertAlmostEqual(bullet.y, expected_y)

    def test_handle_turret_rotation_left(self):
        """Test turret rotates left"""
        self.game.reset_game_state()
        initial_angle = self.game.turret_angle

        keys = {pygame.K_LEFT: True, pygame.K_RIGHT: False}
        self.game.handle_turret_rotation(keys)

        # Angle should decrease (rotate left)
        self.assertLess(self.game.turret_angle, initial_angle)

    def test_handle_turret_rotation_right(self):
        """Test turret rotates right"""
        self.game.reset_game_state()
        initial_angle = self.game.turret_angle

        keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True}
        self.game.handle_turret_rotation(keys)

        # Angle should increase (rotate right)
        self.assertGreater(self.game.turret_angle, initial_angle)

    def test_handle_turret_rotation_limits(self):
        """Test turret rotation limits"""
        self.game.reset_game_state()

        # Rotate left to limit
        keys = {pygame.K_LEFT: True, pygame.K_RIGHT: False}
        for _ in range(100):
            self.game.handle_turret_rotation(keys)

        self.assertGreaterEqual(self.game.turret_angle, -math.pi)

        # Rotate right to limit
        self.game.turret_angle = -0.1
        keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True}
        for _ in range(100):
            self.game.handle_turret_rotation(keys)

        self.assertLessEqual(self.game.turret_angle, 0)

    def test_handle_turret_rotation_when_destroyed(self):
        """Test turret doesn't rotate when destroyed"""
        self.game.reset_game_state()
        self.game.turret_alive = False
        initial_angle = self.game.turret_angle

        keys = {pygame.K_LEFT: True, pygame.K_RIGHT: False}
        self.game.handle_turret_rotation(keys)

        # Angle should not change
        self.assertEqual(self.game.turret_angle, initial_angle)

    def test_spawn_helicopters(self):
        """Test helicopters spawn correctly"""
        self.game.reset_game_state()
        self.game.spawn_timer = 1

        initial_count = len(self.game.helicopters)
        self.game.spawn_helicopters()

        # Should spawn a helicopter
        self.assertEqual(len(self.game.helicopters), initial_count + 1)
        self.assertEqual(self.game.helis_spawned, 1)

    def test_spawn_helicopters_respects_wave_limit(self):
        """Test helicopters don't spawn beyond wave limit"""
        self.game.reset_game_state()
        self.game.wave_helicopters = 2
        self.game.helis_spawned = 2
        self.game.spawn_timer = 0

        initial_count = len(self.game.helicopters)
        self.game.spawn_helicopters()

        # Should not spawn more helicopters
        self.assertEqual(len(self.game.helicopters), initial_count)

    def test_update_helicopters_movement(self):
        """Test helicopters update position"""
        self.game.reset_game_state()
        heli = Helicopter(100, 100, 1, 2.0)
        self.game.helicopters = [heli]

        self.game.update_helicopters()

        # Helicopter should have moved
        self.assertNotEqual(heli.x, 100)

    def test_update_helicopters_drops_paratroopers(self):
        """Test helicopters drop paratroopers"""
        self.game.reset_game_state()
        heli = Helicopter(200, 100, 1)
        heli.drop_timer = 0  # Ready to drop
        self.game.helicopters = [heli]

        initial_para_count = len(self.game.paratroopers)
        self.game.update_helicopters()

        # Should have dropped a paratrooper
        self.assertEqual(len(self.game.paratroopers), initial_para_count + 1)

    def test_update_helicopters_removes_offscreen(self):
        """Test off-screen helicopters are removed"""
        self.game.reset_game_state()
        heli = Helicopter(-100, 100, -1)  # Off screen to the left
        self.game.helicopters = [heli]

        self.game.update_helicopters()

        # Helicopter should be removed
        self.assertEqual(len(self.game.helicopters), 0)

    def test_update_paratroopers_falling(self):
        """Test paratroopers fall"""
        self.game.reset_game_state()
        para = Paratrooper(100, 100)
        self.game.paratroopers = [para]
        initial_y = para.y

        self.game.update_paratroopers()

        # Should have fallen
        self.assertGreater(para.y, initial_y)

    def test_update_paratroopers_landing_causes_game_over(self):
        """Test paratrooper landing on turret causes game over"""
        self.game.reset_game_state()
        para = Paratrooper(self.game.turret_x, self.game.turret_y - 10)
        self.game.paratroopers = [para]

        self.game.update_paratroopers()

        # Game should be over
        self.assertTrue(self.game.game_over)
        self.assertFalse(self.game.turret_alive)

    def test_update_paratroopers_removes_missed(self):
        """Test paratroopers that miss are removed"""
        self.game.reset_game_state()
        para = Paratrooper(100, ParatrooperGame.WINDOW_HEIGHT + 10)
        self.game.paratroopers = [para]

        self.game.update_paratroopers()

        # Paratrooper should be removed
        self.assertEqual(len(self.game.paratroopers), 0)

    def test_update_bullets_movement(self):
        """Test bullets move"""
        self.game.reset_game_state()
        bullet = Bullet(100, 100, -math.pi / 2)  # Straight up
        self.game.bullets = [bullet]
        initial_y = bullet.y

        self.game.update_bullets()

        # Should have moved up
        self.assertLess(bullet.y, initial_y)

    def test_update_bullets_removes_offscreen(self):
        """Test off-screen bullets are removed"""
        self.game.reset_game_state()
        bullet = Bullet(-100, 100, 0)  # Off screen
        self.game.bullets = [bullet]

        self.game.update_bullets()

        # Bullet should be removed
        self.assertEqual(len(self.game.bullets), 0)

    def test_check_bullet_helicopter_collision(self):
        """Test bullet hits helicopter"""
        self.game.reset_game_state()
        heli = Helicopter(100, 100, 1)
        bullet = Bullet(100, 100, 0)
        self.game.helicopters = [heli]
        self.game.bullets = [bullet]  # Bullet needs to be in list for removal

        hit = self.game._check_bullet_helicopter_collision(bullet)

        self.assertTrue(hit)
        self.assertFalse(heli.alive)
        self.assertFalse(bullet.alive)
        self.assertEqual(self.game.score, ParatrooperGame.HELI_SCORE)

    def test_check_bullet_helicopter_no_collision(self):
        """Test bullet misses helicopter"""
        self.game.reset_game_state()
        heli = Helicopter(100, 100, 1)
        bullet = Bullet(500, 500, 0)  # Far away
        self.game.helicopters = [heli]

        hit = self.game._check_bullet_helicopter_collision(bullet)

        self.assertFalse(hit)
        self.assertTrue(heli.alive)
        self.assertTrue(bullet.alive)
        self.assertEqual(self.game.score, 0)

    def test_check_bullet_paratrooper_collision(self):
        """Test bullet hits paratrooper"""
        self.game.reset_game_state()
        para = Paratrooper(100, 100)
        bullet = Bullet(100, 100, 0)
        self.game.paratroopers = [para]
        self.game.bullets = [bullet]

        self.game._check_bullet_paratrooper_collision(bullet)

        self.assertFalse(para.alive)
        self.assertFalse(bullet.alive)
        self.assertEqual(self.game.score, ParatrooperGame.PARA_SCORE)

    def test_check_bullet_paratrooper_no_collision(self):
        """Test bullet misses paratrooper"""
        self.game.reset_game_state()
        para = Paratrooper(100, 100)
        bullet = Bullet(500, 500, 0)  # Far away
        self.game.paratroopers = [para]
        self.game.bullets = [bullet]

        self.game._check_bullet_paratrooper_collision(bullet)

        self.assertTrue(para.alive)
        self.assertTrue(bullet.alive)
        self.assertEqual(self.game.score, 0)

    def test_check_wave_completion(self):
        """Test wave completion advances to next wave"""
        self.game.reset_game_state()
        self.game.wave_helicopters = 3
        self.game.helis_spawned = 3
        self.game.helicopters = []
        self.game.paratroopers = []

        initial_wave = self.game.wave

        self.game.check_wave_completion()

        # Should advance to next wave
        self.assertEqual(self.game.wave, initial_wave + 1)
        self.assertEqual(self.game.helis_spawned, 0)

    def test_check_wave_completion_not_ready(self):
        """Test wave doesn't complete when enemies remain"""
        self.game.reset_game_state()
        self.game.wave_helicopters = 3
        self.game.helis_spawned = 3
        self.game.helicopters = [Helicopter(100, 100, 1)]  # Helicopter still active

        initial_wave = self.game.wave

        self.game.check_wave_completion()

        # Should not advance wave
        self.assertEqual(self.game.wave, initial_wave)

    def test_handle_input_escape(self):
        """Test ESC key quits the game"""
        event = Mock(spec=pygame.event.Event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_ESCAPE

        self.game.running = True
        self.game.handle_input(event)

        self.assertFalse(self.game.running)

    def test_handle_input_quit(self):
        """Test QUIT event stops the game"""
        event = Mock(spec=pygame.event.Event)
        event.type = pygame.QUIT

        self.game.running = True
        self.game.handle_input(event)

        self.assertFalse(self.game.running)

    def test_handle_input_space_shoots(self):
        """Test SPACE fires bullet"""
        event = Mock(spec=pygame.event.Event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE

        self.game.reset_game_state()
        self.game.handle_input(event)

        # Should have fired a bullet
        self.assertEqual(len(self.game.bullets), 1)

    def test_handle_input_space_restarts(self):
        """Test SPACE restarts game when game over"""
        event = Mock(spec=pygame.event.Event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE

        self.game.game_over = True
        self.game.score = 100
        self.game.handle_input(event)

        # Game should be reset
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)

    def test_metadata(self):
        """Test game metadata"""
        self.assertEqual(ParatrooperGame.GAME_NAME, "Paratrooper")
        self.assertIsInstance(ParatrooperGame.GAME_DESCRIPTION, str)
        self.assertGreater(len(ParatrooperGame.GAME_DESCRIPTION), 0)

    def test_constants(self):
        """Test game constants are valid"""
        self.assertGreater(ParatrooperGame.WINDOW_WIDTH, 0)
        self.assertGreater(ParatrooperGame.WINDOW_HEIGHT, 0)
        self.assertGreater(ParatrooperGame.BARREL_LENGTH, 0)
        self.assertGreater(ParatrooperGame.SHOOT_COOLDOWN, 0)
        self.assertGreater(ParatrooperGame.HELI_SCORE, 0)
        self.assertGreater(ParatrooperGame.PARA_SCORE, 0)


if __name__ == "__main__":
    unittest.main()
