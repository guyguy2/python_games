# Sound Files

This directory is for storing sound effects and background music for the games.

## Directory Structure

```
sounds/
├── README.md           # This file
├── snake/             # Snake game sounds
├── xonix/             # Xonix game sounds
├── paratrooper/       # Paratrooper game sounds
└── common/            # Shared sounds
```

## Supported Formats

The sound system supports common audio formats:
- WAV (recommended for sound effects)
- OGG (recommended for background music)
- MP3

## Adding Sounds

### For Developers

To add sound effects to a game:

1. Place your sound files in the appropriate directory (e.g., `sounds/snake/`)
2. In your game code, load the sounds using the SoundManager:

```python
from common.sound import get_sound_manager

sound_manager = get_sound_manager()

# Load sound effects
sound_manager.load_sound("eat", "snake/eat.wav")
sound_manager.load_sound("game_over", "snake/game_over.wav")

# Load background music
sound_manager.load_music("snake/background.ogg")
sound_manager.play_music()  # Loop infinitely

# Play sound effects
sound_manager.play_sound("eat")
```

### Example Sound Ideas

**Snake:**
- `eat.wav` - Sound when eating food
- `game_over.wav` - Sound when game ends
- `background.ogg` - Background music

**Xonix:**
- `claim.wav` - Sound when claiming territory
- `hit.wav` - Sound when hit by enemy
- `victory.wav` - Sound when winning
- `background.ogg` - Background music

**Paratrooper:**
- `shoot.wav` - Sound when firing
- `explosion.wav` - Sound when hitting target
- `game_over.wav` - Sound when turret is destroyed
- `background.ogg` - Background music

## Volume Control

The sound system includes volume control:
- Default volume: 70%
- Music plays at 50% of the sound effect volume
- Games can implement mute toggle (M key recommended)

## Free Sound Resources

You can find free game sounds at:
- [OpenGameArt.org](https://opengameart.org/)
- [Freesound.org](https://freesound.org/)
- [Zapsplat.com](https://www.zapsplat.com/)
- [Mixkit.co](https://mixkit.co/free-sound-effects/)

Make sure to check the licenses for any sounds you use.

## Note

The game will work perfectly fine without sound files. The sound system gracefully handles missing files and will simply not play sounds if they're not available.
