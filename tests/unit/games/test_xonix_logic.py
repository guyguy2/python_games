"""
Comprehensive unit tests for Xonix game logic
"""

import unittest
from unittest.mock import Mock

import pygame

from src.games.xonix.game import Enemy, XonixGame


class TestEnemy(unittest.TestCase):
    """Test Enemy class"""

    def test_enemy_initialization(self):
        """Test enemy initializes with correct values"""
        enemy = Enemy(100, 200, 2, -3, 10)
        self.assertEqual(enemy.x, 100)
        self.assertEqual(enemy.y, 200)
        self.assertEqual(enemy.vx, 2)
        self.assertEqual(enemy.vy, -3)
        self.assertEqual(enemy.radius, 10)

    def test_enemy_default_radius(self):
        """Test enemy has default radius"""
        enemy = Enemy(0, 0, 1, 1)
        self.assertEqual(enemy.radius, 8)


class TestXonixGameLogic(unittest.TestCase):
    """Test Xonix game logic without requiring display"""

    def setUp(self):
        """Set up test fixtures"""
        self.game = XonixGame()
        # Mock display to avoid pygame window creation
        self.game.screen = Mock(spec=pygame.Surface)
        self.game.clock = Mock(spec=pygame.time.Clock)
        self.game.font = Mock(spec=pygame.font.Font)
        self.game.small_font = Mock(spec=pygame.font.Font)
        self.game.overlay = Mock()
        self.game.score_display = Mock()

    def test_initialization(self):
        """Test game initializes with correct default values"""
        game = XonixGame()
        self.assertEqual(game.score, 0.0)
        self.assertTrue(game.running)
        self.assertFalse(game.game_over)
        self.assertFalse(game.game_won)
        self.assertFalse(game.drawing)
        self.assertEqual(len(game.enemies), 0)
        self.assertEqual(len(game.trail), 0)

    def test_reset_game_state(self):
        """Test game state resets correctly"""
        self.game.reset_game_state()

        # Check grid dimensions
        self.assertEqual(len(self.game.grid), XonixGame.GRID_HEIGHT)
        self.assertEqual(len(self.game.grid[0]), XonixGame.GRID_WIDTH)

        # Check borders are created
        for x in range(XonixGame.GRID_WIDTH):
            self.assertEqual(self.game.grid[0][x], XonixGame.BORDER)
            self.assertEqual(self.game.grid[XonixGame.GRID_HEIGHT - 1][x], XonixGame.BORDER)
        for y in range(XonixGame.GRID_HEIGHT):
            self.assertEqual(self.game.grid[y][0], XonixGame.BORDER)
            self.assertEqual(self.game.grid[y][XonixGame.GRID_WIDTH - 1], XonixGame.BORDER)

        # Check player position
        self.assertEqual(self.game.player_y, 0)
        self.assertGreaterEqual(self.game.player_x, 0)
        self.assertLess(self.game.player_x, XonixGame.GRID_WIDTH)

        # Check enemies created
        self.assertEqual(len(self.game.enemies), XonixGame.INITIAL_ENEMIES)

        # Check game state
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.game_won)
        self.assertFalse(self.game.drawing)
        self.assertEqual(self.game.score, 0.0)

    def test_get_cell_state_valid(self):
        """Test getting cell state for valid positions"""
        self.game.reset_game_state()

        # Border cells
        self.assertEqual(self.game.get_cell_state(0, 0), XonixGame.BORDER)
        self.assertEqual(self.game.get_cell_state(XonixGame.GRID_WIDTH - 1, 0), XonixGame.BORDER)

        # Empty cells
        self.assertEqual(self.game.get_cell_state(1, 1), XonixGame.EMPTY)

    def test_get_cell_state_out_of_bounds(self):
        """Test getting cell state for out of bounds positions"""
        self.game.reset_game_state()

        self.assertEqual(self.game.get_cell_state(-1, 0), XonixGame.BORDER)
        self.assertEqual(self.game.get_cell_state(0, -1), XonixGame.BORDER)
        self.assertEqual(self.game.get_cell_state(XonixGame.GRID_WIDTH, 0), XonixGame.BORDER)
        self.assertEqual(self.game.get_cell_state(0, XonixGame.GRID_HEIGHT), XonixGame.BORDER)

    def test_is_on_border_or_claimed(self):
        """Test checking if position is on border or claimed"""
        self.game.reset_game_state()

        # Border position
        self.assertTrue(self.game.is_on_border_or_claimed(0, 0))

        # Empty position
        self.assertFalse(self.game.is_on_border_or_claimed(1, 1))

        # Claimed position
        self.game.grid[5][5] = XonixGame.CLAIMED
        self.assertTrue(self.game.is_on_border_or_claimed(5, 5))

    def test_calculate_percentage_initial(self):
        """Test percentage calculation at game start"""
        self.game.reset_game_state()

        # Initial percentage should be 0 (no interior claimed yet)
        percentage = self.game.calculate_percentage()
        self.assertEqual(percentage, 0.0)

    def test_calculate_percentage_fully_claimed(self):
        """Test percentage calculation when fully claimed"""
        self.game.reset_game_state()

        # Claim all interior cells
        for y in range(1, XonixGame.GRID_HEIGHT - 1):
            for x in range(1, XonixGame.GRID_WIDTH - 1):
                self.game.grid[y][x] = XonixGame.CLAIMED

        percentage = self.game.calculate_percentage()
        self.assertAlmostEqual(percentage, 100.0, places=1)

    def test_flood_fill_empty_area(self):
        """Test flood fill on empty area"""
        self.game.reset_game_state()
        self.game.enemies = []  # Remove enemies for this test

        # Start flood fill from center
        center_x = XonixGame.GRID_WIDTH // 2
        center_y = XonixGame.GRID_HEIGHT // 2
        area, has_enemy = self.game.flood_fill(center_x, center_y)

        # Should fill most of the interior (minus borders)
        expected_area = (XonixGame.GRID_WIDTH - 2) * (XonixGame.GRID_HEIGHT - 2)
        self.assertEqual(len(area), expected_area)
        self.assertFalse(has_enemy)

    def test_flood_fill_with_enemy(self):
        """Test flood fill detects enemy in area"""
        self.game.reset_game_state()

        # Place enemy in center
        enemy_x = XonixGame.GRID_WIDTH // 2 * XonixGame.GRID_SIZE
        enemy_y = XonixGame.GRID_HEIGHT // 2 * XonixGame.GRID_SIZE
        self.game.enemies = [Enemy(enemy_x, enemy_y, 1, 1)]

        # Flood fill from center
        area, has_enemy = self.game.flood_fill(
            XonixGame.GRID_WIDTH // 2, XonixGame.GRID_HEIGHT // 2
        )

        self.assertTrue(has_enemy)

    def test_flood_fill_bounded_area(self):
        """Test flood fill on bounded area"""
        self.game.reset_game_state()
        self.game.enemies = []

        # Create a small claimed box
        # x from 5 to 9 (inclusive), y from 5 to 10 (inclusive)
        for x in range(5, 10):
            self.game.grid[5][x] = XonixGame.CLAIMED
            self.game.grid[10][x] = XonixGame.CLAIMED
        for y in range(5, 11):
            self.game.grid[y][5] = XonixGame.CLAIMED
            self.game.grid[y][10] = XonixGame.CLAIMED

        # Flood fill inside the box
        area, has_enemy = self.game.flood_fill(7, 7)

        # Interior: x from 6-9 (4 wide), y from 6-9 (4 tall) = 16 cells
        expected_area = 4 * 4
        self.assertEqual(len(area), expected_area)

    def test_claim_territory_simple(self):
        """Test claiming territory"""
        self.game.reset_game_state()
        self.game.enemies = []

        # Create a small trail forming a square
        self.game.trail = [(5, 5), (10, 5), (10, 10), (5, 10)]

        initial_percentage = self.game.calculate_percentage()
        self.game.claim_territory()
        final_percentage = self.game.calculate_percentage()

        # Percentage should increase
        self.assertGreater(final_percentage, initial_percentage)

        # Trail cells should become border
        for x, y in [(5, 5), (10, 5), (10, 10), (5, 10)]:
            self.assertEqual(self.game.grid[y][x], XonixGame.BORDER)

    def test_process_movement_start_drawing(self):
        """Test starting to draw a trail"""
        self.game.reset_game_state()
        self.game.player_x = 0
        self.game.player_y = 5
        self.game.drawing = False

        # Move into empty space
        self.game._process_movement(1, 5)

        self.assertTrue(self.game.drawing)
        self.assertEqual(len(self.game.trail), 1)
        self.assertEqual(self.game.trail[0], (1, 5))

    def test_process_movement_continue_drawing(self):
        """Test continuing to draw a trail"""
        self.game.reset_game_state()
        self.game.player_x = 1
        self.game.player_y = 5
        self.game.drawing = True
        self.game.trail = [(1, 5)]

        # Continue drawing
        self.game._process_movement(2, 5)

        self.assertTrue(self.game.drawing)
        self.assertEqual(len(self.game.trail), 2)
        self.assertEqual(self.game.trail[-1], (2, 5))

    def test_process_movement_hit_own_trail(self):
        """Test hitting own trail causes game over"""
        self.game.reset_game_state()
        self.game.drawing = True
        self.game.trail = [(1, 5), (2, 5), (3, 5)]

        # Hit own trail
        self.game._process_movement(2, 5)

        self.assertTrue(self.game.game_over)
        self.assertIn("trail", self.game.message.lower())

    def test_process_movement_complete_trail(self):
        """Test completing a trail and claiming territory"""
        self.game.reset_game_state()
        self.game.enemies = []
        self.game.player_x = 1
        self.game.player_y = 5
        self.game.drawing = True
        self.game.trail = [(1, 5), (2, 5)]

        initial_percentage = self.game.calculate_percentage()

        # Complete by reaching border
        self.game._process_movement(0, 5)

        self.assertFalse(self.game.drawing)
        self.assertEqual(len(self.game.trail), 0)
        # Score should be updated
        self.assertGreaterEqual(self.game.score, initial_percentage)

    def test_process_movement_win_condition(self):
        """Test winning when reaching target percentage"""
        self.game.reset_game_state()

        # Claim almost all territory
        for y in range(1, XonixGame.GRID_HEIGHT - 1):
            for x in range(1, XonixGame.GRID_WIDTH - 1):
                self.game.grid[y][x] = XonixGame.CLAIMED

        self.game.drawing = True
        self.game.trail = [(5, 5)]
        self.game._process_movement(0, 5)

        self.assertTrue(self.game.game_won)
        self.assertIn("victory", self.game.message.lower())

    def test_enemy_hits_trail(self):
        """Test detecting enemy collision with trail"""
        self.game.reset_game_state()
        self.game.trail = [(10, 10)]

        # Enemy near trail
        enemy = Enemy(
            10 * XonixGame.GRID_SIZE,
            10 * XonixGame.GRID_SIZE,
            1,
            1,
        )

        self.assertTrue(self.game._enemy_hits_trail(enemy))

        # Enemy far from trail
        enemy_far = Enemy(500, 500, 1, 1)
        self.assertFalse(self.game._enemy_hits_trail(enemy_far))

    def test_enemy_hits_player(self):
        """Test detecting enemy collision with player"""
        self.game.reset_game_state()
        self.game.player_x = 10
        self.game.player_y = 10

        # Enemy at player position
        enemy = Enemy(
            10 * XonixGame.GRID_SIZE,
            10 * XonixGame.GRID_SIZE,
            1,
            1,
        )

        self.assertTrue(self.game._enemy_hits_player(enemy))

        # Enemy far from player
        enemy_far = Enemy(500, 500, 1, 1)
        self.assertFalse(self.game._enemy_hits_player(enemy_far))

    def test_update_enemies_movement(self):
        """Test enemies move"""
        self.game.reset_game_state()
        initial_positions = [(e.x, e.y) for e in self.game.enemies]

        # Update enemies
        self.game.update_enemies()

        # At least some enemies should have moved
        final_positions = [(e.x, e.y) for e in self.game.enemies]
        moved = any(
            initial_positions[i] != final_positions[i] for i in range(len(self.game.enemies))
        )
        self.assertTrue(moved)

    def test_update_enemies_trail_collision(self):
        """Test game over when enemy hits trail"""
        self.game.reset_game_state()
        self.game.drawing = True
        self.game.trail = [(10, 10)]

        # Place enemy on trail
        self.game.enemies = [
            Enemy(
                10 * XonixGame.GRID_SIZE,
                10 * XonixGame.GRID_SIZE,
                1,
                1,
            )
        ]

        self.game.update_enemies()

        self.assertTrue(self.game.game_over)

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
        self.game.score = 50.0
        self.game.handle_input(event)

        # Game should be reset
        self.assertEqual(self.game.score, 0.0)
        self.assertFalse(self.game.game_over)

    def test_metadata(self):
        """Test game metadata"""
        self.assertEqual(XonixGame.GAME_NAME, "Xonix")
        self.assertIsInstance(XonixGame.GAME_DESCRIPTION, str)
        self.assertGreater(len(XonixGame.GAME_DESCRIPTION), 0)

    def test_constants(self):
        """Test game constants are valid"""
        self.assertGreater(XonixGame.GRID_SIZE, 0)
        self.assertGreater(XonixGame.GRID_WIDTH, 0)
        self.assertGreater(XonixGame.GRID_HEIGHT, 0)
        self.assertGreater(XonixGame.TARGET_PERCENTAGE, 0)
        self.assertLessEqual(XonixGame.TARGET_PERCENTAGE, 100)
        self.assertGreater(XonixGame.INITIAL_ENEMIES, 0)


if __name__ == "__main__":
    unittest.main()
