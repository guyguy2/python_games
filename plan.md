# Python Game Launcher - Implementation Plan

## Project Overview
A GUI-based game launcher built with Python and uv package manager. The launcher presents a list of classic games that can be launched with a single click.

## Architecture

### Project Structure
```
python_games/
├── pyproject.toml          # uv project configuration
├── README.md               # Project documentation
├── plan.md                 # This file - implementation plan
├── launcher.py             # Main GUI launcher
├── games/                  # Games directory
│   ├── __init__.py
│   ├── base_game.py        # Base class for games
│   ├── snake/
│   │   ├── __init__.py
│   │   └── game.py
│   ├── xonix/
│   │   ├── __init__.py
│   │   └── game.py
│   └── paratrooper/
│       ├── __init__.py
│       └── game.py
└── assets/                 # Shared assets (fonts, sounds, etc.)
```

### Technology Stack
- **Package Manager**: uv (fast Python package manager)
- **GUI Framework**: pygame (versatile, good for both launcher and games)
- **Python Version**: 3.10+

### Design Decisions
1. **Pygame for Everything**: Using pygame for both the launcher and games ensures consistency and reduces dependencies
2. **Modular Game Structure**: Each game is self-contained in its subdirectory with a standard interface
3. **Base Game Class**: All games inherit from a base class that defines the standard interface
4. **Dynamic Game Discovery**: The launcher automatically discovers games in the games/ directory

## Game Specifications

### 1. Snake
**Classic Snake game where the player controls a snake that grows by eating food**
- Grid-based movement
- Snake grows when eating food
- Game over on wall collision or self-collision
- Score tracking
- Speed increases as snake grows

### 2. Xonix (Qix-like)
**Area-claiming game where player draws lines to claim territory**
- Player controls a cursor that draws lines
- Goal: Claim 75% of the playing area
- Enemies bounce around the open area
- Player loses if touched while drawing
- Percentage tracker shows progress

### 3. Paratrooper
**Classic arcade game - defend the turret from paratroopers**
- Turret at bottom center that rotates
- Helicopters drop paratroopers
- Shoot paratroopers before they land
- Paratroopers destroy turret if they land
- Score tracking and wave system

## Implementation Phases

### Phase 1: Project Setup ✅
- [x] Create plan.md
- [x] Initialize uv project with pyproject.toml
- [x] Install pygame dependency
- [x] Create basic directory structure

### Phase 2: Core Framework ✅
- [x] Create base_game.py with Game interface
- [x] Implement main launcher.py GUI
  - Game list display
  - Launch buttons
  - Clean UI with title and instructions

### Phase 3: Game Implementation ✅
- [x] Implement Snake game
  - Grid system
  - Movement controls
  - Food spawning
  - Collision detection
  - Score display

- [x] Implement Xonix game
  - Drawing mechanics
  - Area calculation
  - Enemy AI
  - Territory claiming
  - Win/lose conditions

- [x] Implement Paratrooper game
  - Turret rotation and shooting
  - Helicopter spawning
  - Paratrooper physics
  - Collision detection
  - Wave system

### Phase 4: Polish & Testing ✅
- [x] Test each game individually
- [x] Test launcher integration
- [x] Add README with instructions
- [x] Final testing and bug fixes

### Phase 5: Deployment 🚀
- [x] Commit all changes
- [ ] Push to repository

## Game Interface Contract

Each game must implement:
```python
class Game:
    def __init__(self):
        """Initialize the game"""

    def run(self):
        """Run the game (blocking call)"""

    @property
    def name(self) -> str:
        """Return game name"""

    @property
    def description(self) -> str:
        """Return game description"""
```

## Controls Standard
- **Snake**: Arrow keys to move
- **Xonix**: Arrow keys to move, auto-draw when moving
- **Paratrooper**: Left/Right arrows to rotate, Space to shoot
- **All Games**: ESC to quit back to launcher

## Progress Tracking
- **Started**: 2025-11-09
- **Completed**: 2025-11-09
- **Current Phase**: Phase 5 - Deployment ✅
- **Status**: Implementation complete! All games functional.

## Implementation Summary
✅ Created modular game architecture with base class
✅ Implemented beautiful GUI launcher with hover effects
✅ Developed three complete, polished games:
  - Snake: Classic gameplay with scoring and speed progression
  - Xonix: Territory claiming with flood-fill algorithm
  - Paratrooper: Wave-based arcade action
✅ All games feature restart functionality and clean exit to launcher
✅ Comprehensive README with instructions and controls
