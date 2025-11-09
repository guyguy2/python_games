# Python Game Launcher 🎮

A GUI-based game launcher featuring classic arcade games built with Python and pygame.

## Features

- **Modern GUI Launcher**: Clean, intuitive interface to browse and launch games
- **Three Classic Games**:
  - **Snake**: Eat food, grow longer, avoid hitting yourself!
  - **Xonix**: Claim 75% territory while dodging enemies
  - **Paratrooper**: Defend your turret from incoming paratroopers

## Requirements

- Python 3.11+
- uv (Python package manager)
- pygame

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd python_games
```

2. Install dependencies using uv:
```bash
uv sync
```

## Running the Launcher

Launch the game menu:
```bash
uv run python launcher.py
```

## Game Controls

### Snake
- **Arrow Keys**: Move the snake
- **ESC**: Quit to launcher
- **SPACE**: Restart after game over

### Xonix
- **Arrow Keys**: Move and draw territory
- **ESC**: Quit to launcher
- **SPACE**: Restart after game over/win

### Paratrooper
- **Left/Right Arrow**: Aim turret
- **SPACE**: Shoot
- **ESC**: Quit to launcher

## Project Structure

```
python_games/
├── launcher.py              # Main GUI launcher
├── games/                   # Games directory
│   ├── base_game.py        # Base game class
│   ├── snake/              # Snake game
│   ├── xonix/              # Xonix game
│   └── paratrooper/        # Paratrooper game
├── plan.md                 # Development plan and progress
└── pyproject.toml          # Project configuration
```

## Development

Built with:
- **Python 3.11+**
- **pygame 2.6.1** - Game framework
- **uv** - Fast Python package manager

## License

MIT License - Feel free to use and modify!

## Contributing

Contributions are welcome! Feel free to:
- Add new games
- Improve existing games
- Enhance the launcher UI
- Fix bugs

---

Made with ❤️ using Python and pygame
