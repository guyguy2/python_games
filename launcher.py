"""
Python Game Launcher - Main GUI
"""
import pygame
import sys
from typing import List, Tuple
from games.snake import SnakeGame
from games.xonix import XonixGame
from games.paratrooper import ParatrooperGame


class GameLauncher:
    """Main game launcher GUI"""

    def __init__(self):
        pygame.init()

        # Screen settings
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Python Game Launcher")

        # Colors
        self.BG_COLOR = (20, 20, 40)
        self.TITLE_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (60, 60, 120)
        self.BUTTON_HOVER_COLOR = (80, 80, 160)
        self.BUTTON_TEXT_COLOR = (255, 255, 255)
        self.DESC_COLOR = (200, 200, 200)

        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.button_font = pygame.font.Font(None, 36)
        self.desc_font = pygame.font.Font(None, 24)

        # Games list
        self.games = [
            SnakeGame,
            XonixGame,
            ParatrooperGame
        ]

        # Button rectangles
        self.buttons = []
        self.setup_buttons()

        self.clock = pygame.time.Clock()
        self.running = True

    def setup_buttons(self):
        """Create button rectangles for each game"""
        button_width = 600
        button_height = 80
        button_x = (self.width - button_width) // 2
        start_y = 200
        spacing = 100

        for i, game_class in enumerate(self.games):
            game_instance = game_class()
            button_rect = pygame.Rect(
                button_x,
                start_y + i * spacing,
                button_width,
                button_height
            )
            self.buttons.append({
                'rect': button_rect,
                'game': game_class,
                'name': game_instance.name,
                'description': game_instance.description
            })

    def draw(self, mouse_pos: Tuple[int, int]):
        """Draw the launcher interface"""
        self.screen.fill(self.BG_COLOR)

        # Draw title
        title_text = self.title_font.render("Game Launcher", True, self.TITLE_COLOR)
        title_rect = title_text.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title_text, title_rect)

        # Draw subtitle
        subtitle_text = self.desc_font.render("Click a game to play!", True, self.DESC_COLOR)
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 130))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Draw game buttons
        for button in self.buttons:
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

    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse click on buttons"""
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                self.launch_game(button['game'])
                break

    def launch_game(self, game_class):
        """Launch a game"""
        # Clear the screen before launching
        self.screen.fill(self.BG_COLOR)
        pygame.display.flip()

        # Create and run game instance
        game = game_class()
        game.run()

        # Re-initialize display after game ends
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Python Game Launcher")

    def run(self):
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
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    launcher = GameLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
