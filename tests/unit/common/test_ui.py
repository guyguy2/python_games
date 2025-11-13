"""
Unit tests for common UI components
"""

import unittest
from unittest.mock import Mock, patch

import pygame

from src.common.ui import GameOverlay, ScoreDisplay


class TestGameOverlay(unittest.TestCase):
    """Test GameOverlay UI component"""

    def setUp(self):
        """Set up test fixtures"""
        self.screen = Mock(spec=pygame.Surface)
        self.screen.get_size.return_value = (800, 600)
        self.screen.blit = Mock()

    @patch("pygame.font.Font")
    def test_initialization(self, mock_font):
        """Test GameOverlay initializes correctly"""
        overlay = GameOverlay(self.screen)

        self.assertEqual(overlay.screen, self.screen)
        # Should create two fonts
        self.assertEqual(mock_font.call_count, 2)

    @patch("pygame.font.Font")
    @patch("pygame.Surface")
    def test_draw_overlay_creates_surfaces(self, mock_surface, mock_font):
        """Test draw_overlay creates necessary surfaces"""
        # Setup mock font
        mock_font_instance = Mock()
        mock_font_instance.render = Mock(return_value=Mock())
        mock_font.return_value = mock_font_instance

        # Setup mock surface
        mock_overlay_surface = Mock()
        mock_surface.return_value = mock_overlay_surface

        # Setup mock rendered text
        mock_text = Mock()
        mock_text.get_rect = Mock(return_value=Mock())
        mock_font_instance.render.return_value = mock_text

        overlay = GameOverlay(self.screen)
        overlay.draw_overlay(
            title="Test Title", subtitle="Test Subtitle", instructions="Test Instructions"
        )

        # Verify overlay surface created
        mock_surface.assert_called_once()
        # Verify alpha set for transparency
        mock_overlay_surface.set_alpha.assert_called_once()

    @patch("pygame.font.Font")
    def test_draw_overlay_renders_text(self, mock_font):
        """Test draw_overlay renders all text"""
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        mock_text = Mock()
        mock_text.get_rect = Mock(return_value=Mock())
        mock_font_instance.render = Mock(return_value=mock_text)

        overlay = GameOverlay(self.screen)
        overlay.draw_overlay(title="Game Over", subtitle="Score: 100", instructions="Press SPACE")

        # Should render three pieces of text (title, subtitle, instructions)
        render_calls = mock_font_instance.render.call_args_list
        self.assertGreaterEqual(len(render_calls), 3)

    @patch("pygame.font.Font")
    def test_draw_overlay_with_custom_colors(self, mock_font):
        """Test draw_overlay with custom colors"""
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        mock_text = Mock()
        mock_text.get_rect = Mock(return_value=Mock())
        mock_font_instance.render = Mock(return_value=mock_text)

        overlay = GameOverlay(self.screen)
        custom_title_color = (255, 0, 0)
        custom_text_color = (0, 255, 0)

        overlay.draw_overlay(
            title="Test",
            subtitle="Test",
            instructions="Test",
            title_color=custom_title_color,
            text_color=custom_text_color,
        )

        # Verify render was called with custom colors
        render_calls = mock_font_instance.render.call_args_list
        # First call should use title color
        self.assertIn(custom_title_color, render_calls[0][0])


class TestScoreDisplay(unittest.TestCase):
    """Test ScoreDisplay UI component"""

    @patch("pygame.font.Font")
    def test_initialization_default_size(self, mock_font):
        """Test ScoreDisplay initializes with default font size"""
        score_display = ScoreDisplay()

        mock_font.assert_called_once_with(None, 36)
        self.assertIsNotNone(score_display.font)

    @patch("pygame.font.Font")
    def test_initialization_custom_size(self, mock_font):
        """Test ScoreDisplay initializes with custom font size"""
        custom_size = 48
        _score_display = ScoreDisplay(font_size=custom_size)

        mock_font.assert_called_once_with(None, custom_size)

    @patch("pygame.font.Font")
    def test_draw(self, mock_font):
        """Test draw method renders and blits text"""
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        mock_text = Mock()
        mock_font_instance.render = Mock(return_value=mock_text)

        screen = Mock(spec=pygame.Surface)
        screen.blit = Mock()

        score_display = ScoreDisplay()
        score_display.draw(screen, "Score: 100", (10, 10))

        # Verify text rendered
        mock_font_instance.render.assert_called_once()
        # Verify text blitted to screen
        screen.blit.assert_called_once_with(mock_text, (10, 10))

    @patch("pygame.font.Font")
    def test_draw_with_custom_color(self, mock_font):
        """Test draw method with custom color"""
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        mock_text = Mock()
        mock_font_instance.render = Mock(return_value=mock_text)

        screen = Mock(spec=pygame.Surface)
        score_display = ScoreDisplay()

        custom_color = (255, 0, 0)
        score_display.draw(screen, "Test", (0, 0), color=custom_color)

        # Verify render called with custom color
        render_call = mock_font_instance.render.call_args
        self.assertIn(custom_color, render_call[0])

    @patch("pygame.font.Font")
    def test_draw_different_texts(self, mock_font):
        """Test draw method with different text strings"""
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        mock_text = Mock()
        mock_font_instance.render = Mock(return_value=mock_text)

        screen = Mock(spec=pygame.Surface)
        score_display = ScoreDisplay()

        test_texts = ["Score: 0", "High Score: 1000", "Level: 5", "Lives: 3"]

        for text in test_texts:
            mock_font_instance.render.reset_mock()
            score_display.draw(screen, text, (0, 0))

            # Verify each text was rendered
            render_call = mock_font_instance.render.call_args
            self.assertIn(text, render_call[0])


if __name__ == "__main__":
    unittest.main()
