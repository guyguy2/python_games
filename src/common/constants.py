"""Common constants for all games"""

# Common colors
Color = tuple[int, int, int]

# UI Colors
BLACK: Color = (0, 0, 0)
WHITE: Color = (255, 255, 255)
RED: Color = (255, 0, 0)
GREEN: Color = (0, 255, 0)
BLUE: Color = (0, 0, 255)
YELLOW: Color = (255, 255, 0)

# Dark theme colors
DARK_BG: Color = (20, 20, 40)
DARK_BUTTON: Color = (60, 60, 120)
DARK_BUTTON_HOVER: Color = (80, 80, 160)
LIGHT_TEXT: Color = (200, 200, 200)

# Game-specific colors
SNAKE_GREEN: Color = (0, 255, 0)
SNAKE_HEAD_GREEN: Color = (0, 200, 0)
XONIX_BLUE: Color = (0, 100, 200)
XONIX_BORDER: Color = (0, 150, 255)

# Common settings
DEFAULT_FPS: int = 60
