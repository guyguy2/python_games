"""Shared UI components for games"""

import pygame

from .constants import BLACK, WHITE, Color


class GameOverlay:
    """Reusable game over/win overlay component"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def draw_overlay(
        self,
        title: str,
        subtitle: str,
        instructions: str,
        title_color: Color = (255, 100, 100),
        text_color: Color = WHITE,
    ) -> None:
        """Draw a semi-transparent overlay with text"""
        width, height = self.screen.get_size()

        # Create semi-transparent overlay
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Draw title
        title_text = self.font.render(title, True, title_color)
        title_rect = title_text.get_rect(center=(width // 2, height // 2 - 30))
        self.screen.blit(title_text, title_rect)

        # Draw subtitle
        subtitle_text = self.font.render(subtitle, True, text_color)
        subtitle_rect = subtitle_text.get_rect(center=(width // 2, height // 2 + 10))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Draw instructions
        instructions_text = self.small_font.render(instructions, True, text_color)
        instructions_rect = instructions_text.get_rect(center=(width // 2, height // 2 + 50))
        self.screen.blit(instructions_text, instructions_rect)


class ScoreDisplay:
    """Reusable score display component"""

    def __init__(self, font_size: int = 36):
        self.font = pygame.font.Font(None, font_size)

    def draw(
        self, screen: pygame.Surface, text: str, position: tuple[int, int], color: Color = WHITE
    ) -> None:
        """Draw score text at specified position"""
        score_text = self.font.render(text, True, color)
        screen.blit(score_text, position)
