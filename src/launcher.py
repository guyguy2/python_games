"""
Python Game Launcher - Main GUI
"""
import pygame
import sys
from typing import List, Tuple, Type, Dict
from games.snake import SnakeGame
from games.xonix import XonixGame
from games.paratrooper import ParatrooperGame
from games.base_game import BaseGame
from common.constants import DARK_BG, DARK_BUTTON, DARK_BUTTON_HOVER, WHITE, LIGHT_TEXT, DEFAULT_FPS


class GameLauncher:
    """Main game launcher GUI"""

    # Window settings
    WIDTH = 800
    HEIGHT = 600

    # Colors
    BG_COLOR = DARK_BG
    TITLE_COLOR = WHITE
    BUTTON_COLOR = DARK_BUTTON
    BUTTON_HOVER_COLOR = DARK_BUTTON_HOVER
    BUTTON_TEXT_COLOR = WHITE
    DESC_COLOR = LIGHT_TEXT

    # Button settings
    BUTTON_WIDTH = 600
    BUTTON_HEIGHT = 80
    BUTTON_SPACING = 100
    BUTTON_START_Y = 200

    def __init__(self):
        """Initialize the game launcher"""
        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Python Game Launcher")

        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.button_font = pygame.font.Font(None, 36)
        self.desc_font = pygame.font.Font(None, 24)

        # Games list - using class references, not instances
        self.games: List[Type[BaseGame]] = [
            SnakeGame,
            XonixGame,
            ParatrooperGame
        ]

        # Button rectangles
        self.buttons: List[Dict] = []
        self.setup_buttons()

        self.clock = pygame.time.Clock()
        self.running = True

    def setup_buttons(self) -> None:
        """
        Create button rectangles for each game

        Uses class attributes (GAME_NAME, GAME_DESCRIPTION) instead of
        instantiating games, which is more efficient.
        """
        button_x = (self.WIDTH - self.BUTTON_WIDTH) // 2

        for i, game_class in enumerate(self.games):
            button_rect = pygame.Rect(
                button_x,
                self.BUTTON_START_Y + i * self.BUTTON_SPACING,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT
            )
            self.buttons.append({
                'rect': button_rect,
                'game': game_class,
                'name': game_class.GAME_NAME,
                'description': game_class.GAME_DESCRIPTION
            })

    def draw(self, mouse_pos: Tuple[int, int]) -> None:
        """Draw the launcher interface"""
        self.screen.fill(self.BG_COLOR)

        # Draw title
        title_text = self.title_font.render("Game Launcher", True, self.TITLE_COLOR)
        title_rect = title_text.get_rect(center=(self.WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)

        # Draw subtitle
        subtitle_text = self.desc_font.render("Click a game to play!", True, self.DESC_COLOR)
        subtitle_rect = subtitle_text.get_rect(center=(self.WIDTH // 2, 130))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Draw game buttons
        for button in self.buttons:
            self._draw_button(button, mouse_pos)

    def _draw_button(self, button: Dict, mouse_pos: Tuple[int, int]) -> None:
        """Draw a single game button"""
        # Check if mouse is hovering
        is_hover = button['rect'].collidepoint(mouse_pos)
        button_color = self.BUTTON_HOVER_COLOR if is_hover else self.BUTTON_COLOR

        # Draw button background
        pygame.draw.rect(self.screen, button_color, button['rect'], border_radius=10)
        pygame.draw.rect(self.screen, self.BUTTON_TEXT_COLOR, button['rect'], 2, border_radius=10)

        # Draw game name
        name_text = self.button_font.render(button['name'], True, self.BUTTON_TEXT_COLOR)
        name_rect = name_text.get_rect(
            center=(button['rect'].centerx, button['rect'].centery - 15)
        )
        self.screen.blit(name_text, name_rect)

        # Draw game description
        desc_text = self.desc_font.render(button['description'], True, self.DESC_COLOR)
        desc_rect = desc_text.get_rect(
            center=(button['rect'].centerx, button['rect'].centery + 15)
        )
        self.screen.blit(desc_text, desc_rect)

    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle mouse click on buttons"""
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                self.launch_game(button['game'])
                break

    def launch_game(self, game_class: Type[BaseGame]) -> None:
        """Launch a game"""
        # Clear the screen before launching
        self.screen.fill(self.BG_COLOR)
        pygame.display.flip()

        # Create and run game instance
        game = game_class()
        game.run()

        # Re-initialize display after game ends
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Python Game Launcher")

    def run(self) -> None:
        """Main launcher loop"""
        while self.running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.draw(mouse_pos)
            pygame.display.flip()
            self.clock.tick(DEFAULT_FPS)

        pygame.quit()
        sys.exit()


def main() -> None:
    """Entry point for the launcher"""
    launcher = GameLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
