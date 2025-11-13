"""
Comprehensive unit tests for Snake game logic
"""

import unittest
from unittest.mock import Mock

import pygame

from src.games.snake.game import SnakeGame


class TestSnakeGameLogic(unittest.TestCase):
    """Test Snake game logic without requiring display"""

    def setUp(self):
        """Set up test fixtures"""
        self.game = SnakeGame()
        # Mock display to avoid pygame window creation
        self.game.screen = Mock(spec=pygame.Surface)
        self.game.clock = Mock(spec=pygame.time.Clock)
        self.game.font = Mock(spec=pygame.font.Font)
        self.game.small_font = Mock(spec=pygame.font.Font)
        self.game.overlay = Mock()
        self.game.score_display = Mock()

    def test_initialization(self):
        """Test game initializes with correct default values"""
        game = SnakeGame()
        self.assertEqual(game.score, 0)
        self.assertEqual(game.direction, SnakeGame.RIGHT)
        self.assertEqual(game.speed, SnakeGame.INITIAL_SPEED)
        self.assertTrue(game.running)
        self.assertFalse(game.game_over)
        self.assertEqual(len(game.snake), 0)

    def test_reset_game_state(self):
        """Test game state resets correctly"""
        # Modify game state
        self.game.score = 100
        self.game.game_over = True
        self.game.speed = 20
        self.game.snake = [(1, 1), (2, 2), (3, 3)]

        # Reset
        self.game.reset_game_state()

        # Verify reset
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.speed, SnakeGame.INITIAL_SPEED)
        self.assertEqual(len(self.game.snake), 1)
        self.assertEqual(self.game.direction, SnakeGame.RIGHT)
        self.assertIsNotNone(self.game.food)

    def test_spawn_food_not_on_snake(self):
        """Test food spawns in position not occupied by snake"""
        self.game.reset_game_state()

        # Spawn food multiple times
        for _ in range(10):
            food = self.game.spawn_food()
            self.assertIsInstance(food, tuple)
            self.assertEqual(len(food), 2)
            # Food should not be on snake
            self.assertNotIn(food, self.game.snake)
            # Food should be within bounds
            self.assertGreaterEqual(food[0], 0)
            self.assertLess(food[0], SnakeGame.GRID_WIDTH)
            self.assertGreaterEqual(food[1], 0)
            self.assertLess(food[1], SnakeGame.GRID_HEIGHT)

    def test_spawn_food_fills_board(self):
        """Test food can spawn when board is nearly full"""
        # Fill most of the board with snake
        self.game.snake = [(x, y) for x in range(SnakeGame.GRID_WIDTH) for y in range(5)]

        food = self.game.spawn_food()
        self.assertNotIn(food, self.game.snake)

    def test_check_collision_walls(self):
        """Test collision detection with walls"""
        # Left wall
        self.assertTrue(self.game._check_collision((-1, 5)))
        # Right wall
        self.assertTrue(self.game._check_collision((SnakeGame.GRID_WIDTH, 5)))
        # Top wall
        self.assertTrue(self.game._check_collision((5, -1)))
        # Bottom wall
        self.assertTrue(self.game._check_collision((5, SnakeGame.GRID_HEIGHT)))

    def test_check_collision_self(self):
        """Test collision detection with snake body"""
        self.game.snake = [(5, 5), (5, 6), (5, 7)]
        # Collision with body
        self.assertTrue(self.game._check_collision((5, 6)))
        # No collision
        self.assertFalse(self.game._check_collision((6, 6)))

    def test_check_collision_valid_position(self):
        """Test valid positions don't register as collisions"""
        self.game.snake = [(5, 5)]
        self.assertFalse(self.game._check_collision((6, 5)))
        self.assertFalse(self.game._check_collision((0, 0)))
        self.assertFalse(
            self.game._check_collision((SnakeGame.GRID_WIDTH - 1, SnakeGame.GRID_HEIGHT - 1))
        )

    def test_handle_direction_input_basic(self):
        """Test basic direction changes"""
        # Test UP input when moving right
        self.game.direction = SnakeGame.RIGHT
        self.game.next_direction = SnakeGame.RIGHT
        self.game._handle_direction_input(pygame.K_UP)
        self.assertEqual(self.game.next_direction, SnakeGame.UP)

        # Test LEFT input when moving up
        self.game.direction = SnakeGame.UP
        self.game.next_direction = SnakeGame.UP
        self.game._handle_direction_input(pygame.K_LEFT)
        self.assertEqual(self.game.next_direction, SnakeGame.LEFT)

        # Test DOWN input when moving left
        self.game.direction = SnakeGame.LEFT
        self.game.next_direction = SnakeGame.LEFT
        self.game._handle_direction_input(pygame.K_DOWN)
        self.assertEqual(self.game.next_direction, SnakeGame.DOWN)

        # Test RIGHT input when moving down
        self.game.direction = SnakeGame.DOWN
        self.game.next_direction = SnakeGame.DOWN
        self.game._handle_direction_input(pygame.K_RIGHT)
        self.assertEqual(self.game.next_direction, SnakeGame.RIGHT)

    def test_handle_direction_input_prevents_180_turn(self):
        """Test that 180-degree turns are prevented"""
        # Moving right, can't go left
        self.game.direction = SnakeGame.RIGHT
        self.game.next_direction = SnakeGame.RIGHT
        self.game._handle_direction_input(pygame.K_LEFT)
        self.assertEqual(self.game.next_direction, SnakeGame.RIGHT)

        # Moving left, can't go right
        self.game.direction = SnakeGame.LEFT
        self.game.next_direction = SnakeGame.LEFT
        self.game._handle_direction_input(pygame.K_RIGHT)
        self.assertEqual(self.game.next_direction, SnakeGame.LEFT)

        # Moving up, can't go down
        self.game.direction = SnakeGame.UP
        self.game.next_direction = SnakeGame.UP
        self.game._handle_direction_input(pygame.K_DOWN)
        self.assertEqual(self.game.next_direction, SnakeGame.UP)

        # Moving down, can't go up
        self.game.direction = SnakeGame.DOWN
        self.game.next_direction = SnakeGame.DOWN
        self.game._handle_direction_input(pygame.K_UP)
        self.assertEqual(self.game.next_direction, SnakeGame.DOWN)

    def test_update_game_state_movement(self):
        """Test snake moves correctly"""
        self.game.snake = [(5, 5)]
        self.game.direction = SnakeGame.RIGHT
        self.game.next_direction = SnakeGame.RIGHT
        self.game.food = (10, 10)  # Food far away

        self.game.update_game_state()

        # Snake should have moved right
        self.assertEqual(self.game.snake[0], (6, 5))
        self.assertEqual(len(self.game.snake), 1)

    def test_update_game_state_food_eating(self):
        """Test snake eats food and grows"""
        self.game.snake = [(5, 5)]
        self.game.direction = SnakeGame.RIGHT
        self.game.next_direction = SnakeGame.RIGHT
        self.game.food = (6, 5)  # Food directly ahead
        self.game.score = 0

        self.game.update_game_state()

        # Snake should have grown
        self.assertEqual(len(self.game.snake), 2)
        # Score should increase
        self.assertEqual(self.game.score, 10)
        # Food should respawn
        self.assertNotEqual(self.game.food, (6, 5))

    def test_update_game_state_wall_collision(self):
        """Test game over on wall collision"""
        # Snake at left edge moving left
        self.game.snake = [(0, 5)]
        self.game.direction = SnakeGame.LEFT
        self.game.next_direction = SnakeGame.LEFT
        self.game.food = (10, 10)
        self.game.game_over = False

        self.game.update_game_state()

        self.assertTrue(self.game.game_over)

    def test_update_game_state_self_collision(self):
        """Test game over on self collision"""
        # Snake arranged to collide with itself
        self.game.snake = [(5, 5), (5, 6), (6, 6), (6, 5)]
        self.game.direction = SnakeGame.DOWN
        self.game.next_direction = SnakeGame.DOWN
        self.game.food = (10, 10)
        self.game.game_over = False

        self.game.update_game_state()

        self.assertTrue(self.game.game_over)

    def test_update_game_state_when_game_over(self):
        """Test update does nothing when game is over"""
        self.game.snake = [(5, 5)]
        self.game.game_over = True
        initial_snake = self.game.snake.copy()

        self.game.update_game_state()

        # Nothing should change
        self.assertEqual(self.game.snake, initial_snake)

    def test_increase_speed(self):
        """Test speed increases with score"""
        # Initial speed
        self.game.score = 0
        self.game._increase_speed()
        self.assertEqual(self.game.speed, SnakeGame.INITIAL_SPEED)

        # Speed should increase at threshold
        self.game.score = SnakeGame.SPEED_INCREASE_THRESHOLD
        self.game._increase_speed()
        self.assertEqual(self.game.speed, SnakeGame.INITIAL_SPEED + 1)

        # Speed should max out
        self.game.score = 1000
        self.game._increase_speed()
        self.assertEqual(self.game.speed, SnakeGame.MAX_SPEED)

    def test_increase_speed_never_exceeds_max(self):
        """Test speed never exceeds maximum"""
        self.game.score = 10000
        self.game._increase_speed()
        self.assertLessEqual(self.game.speed, SnakeGame.MAX_SPEED)

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
        self.assertEqual(SnakeGame.GAME_NAME, "Snake")
        self.assertIsInstance(SnakeGame.GAME_DESCRIPTION, str)
        self.assertGreater(len(SnakeGame.GAME_DESCRIPTION), 0)

    def test_constants(self):
        """Test game constants are valid"""
        self.assertGreater(SnakeGame.GRID_SIZE, 0)
        self.assertGreater(SnakeGame.GRID_WIDTH, 0)
        self.assertGreater(SnakeGame.GRID_HEIGHT, 0)
        self.assertGreater(SnakeGame.INITIAL_SPEED, 0)
        self.assertGreater(SnakeGame.MAX_SPEED, SnakeGame.INITIAL_SPEED)


if __name__ == "__main__":
    unittest.main()
