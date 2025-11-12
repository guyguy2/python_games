"""
Unit tests for common constants
"""

import unittest

from src.common import constants


class TestConstants(unittest.TestCase):
    """Test common constants are properly defined"""

    def test_color_type_definition(self):
        """Test Color type is defined"""
        self.assertTrue(hasattr(constants, "Color"))

    def test_basic_colors_defined(self):
        """Test basic colors are defined"""
        self.assertTrue(hasattr(constants, "BLACK"))
        self.assertTrue(hasattr(constants, "WHITE"))
        self.assertTrue(hasattr(constants, "RED"))
        self.assertTrue(hasattr(constants, "GREEN"))
        self.assertTrue(hasattr(constants, "BLUE"))
        self.assertTrue(hasattr(constants, "YELLOW"))

    def test_basic_colors_format(self):
        """Test basic colors have correct format"""
        for color in [
            constants.BLACK,
            constants.WHITE,
            constants.RED,
            constants.GREEN,
            constants.BLUE,
            constants.YELLOW,
        ]:
            self.assertIsInstance(color, tuple)
            self.assertEqual(len(color), 3)
            for component in color:
                self.assertIsInstance(component, int)
                self.assertGreaterEqual(component, 0)
                self.assertLessEqual(component, 255)

    def test_specific_color_values(self):
        """Test specific color values are correct"""
        self.assertEqual(constants.BLACK, (0, 0, 0))
        self.assertEqual(constants.WHITE, (255, 255, 255))
        self.assertEqual(constants.RED, (255, 0, 0))
        self.assertEqual(constants.GREEN, (0, 255, 0))
        self.assertEqual(constants.BLUE, (0, 0, 255))
        self.assertEqual(constants.YELLOW, (255, 255, 0))

    def test_dark_theme_colors_defined(self):
        """Test dark theme colors are defined"""
        self.assertTrue(hasattr(constants, "DARK_BG"))
        self.assertTrue(hasattr(constants, "DARK_BUTTON"))
        self.assertTrue(hasattr(constants, "DARK_BUTTON_HOVER"))
        self.assertTrue(hasattr(constants, "LIGHT_TEXT"))

    def test_dark_theme_colors_format(self):
        """Test dark theme colors have correct format"""
        for color in [
            constants.DARK_BG,
            constants.DARK_BUTTON,
            constants.DARK_BUTTON_HOVER,
            constants.LIGHT_TEXT,
        ]:
            self.assertIsInstance(color, tuple)
            self.assertEqual(len(color), 3)
            for component in color:
                self.assertIsInstance(component, int)
                self.assertGreaterEqual(component, 0)
                self.assertLessEqual(component, 255)

    def test_game_specific_colors_defined(self):
        """Test game-specific colors are defined"""
        self.assertTrue(hasattr(constants, "SNAKE_GREEN"))
        self.assertTrue(hasattr(constants, "SNAKE_HEAD_GREEN"))
        self.assertTrue(hasattr(constants, "XONIX_BLUE"))
        self.assertTrue(hasattr(constants, "XONIX_BORDER"))

    def test_game_specific_colors_format(self):
        """Test game-specific colors have correct format"""
        for color in [
            constants.SNAKE_GREEN,
            constants.SNAKE_HEAD_GREEN,
            constants.XONIX_BLUE,
            constants.XONIX_BORDER,
        ]:
            self.assertIsInstance(color, tuple)
            self.assertEqual(len(color), 3)
            for component in color:
                self.assertIsInstance(component, int)
                self.assertGreaterEqual(component, 0)
                self.assertLessEqual(component, 255)

    def test_default_fps_defined(self):
        """Test DEFAULT_FPS is defined"""
        self.assertTrue(hasattr(constants, "DEFAULT_FPS"))

    def test_default_fps_value(self):
        """Test DEFAULT_FPS has valid value"""
        self.assertIsInstance(constants.DEFAULT_FPS, int)
        self.assertGreater(constants.DEFAULT_FPS, 0)
        self.assertLessEqual(constants.DEFAULT_FPS, 240)  # Reasonable upper bound
        self.assertEqual(constants.DEFAULT_FPS, 60)


if __name__ == "__main__":
    unittest.main()
