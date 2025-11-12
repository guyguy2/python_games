"""Sound effects and background music manager"""

import contextlib
from pathlib import Path

import pygame


class SoundManager:
    """Manages sound effects and background music for games"""

    def __init__(self, sounds_dir: str = "sounds", volume: float = 0.7):
        """
        Initialize the sound manager

        Args:
            sounds_dir: Directory containing sound files
            volume: Default volume level (0.0 to 1.0)
        """
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            self.mixer_available = True
        except pygame.error:
            self.mixer_available = False

        self.sounds_dir = Path(sounds_dir)
        self.volume = volume
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.music_playing = False
        self.muted = False

    def load_sound(self, name: str, filename: str) -> bool:
        """
        Load a sound effect

        Args:
            name: Name to reference the sound
            filename: Path to sound file relative to sounds_dir

        Returns:
            True if loaded successfully, False otherwise
        """
        if not self.mixer_available:
            return False

        sound_path = self.sounds_dir / filename
        if sound_path.exists():
            try:
                sound = pygame.mixer.Sound(str(sound_path))
                sound.set_volume(self.volume)
                self.sounds[name] = sound
                return True
            except pygame.error:
                return False
        return False

    def play_sound(self, name: str) -> None:
        """
        Play a sound effect

        Args:
            name: Name of the sound to play
        """
        if not self.mixer_available or self.muted:
            return

        if name in self.sounds:
            self.sounds[name].play()

    def load_music(self, filename: str) -> bool:
        """
        Load background music

        Args:
            filename: Path to music file relative to sounds_dir

        Returns:
            True if loaded successfully, False otherwise
        """
        if not self.mixer_available:
            return False

        music_path = self.sounds_dir / filename
        if music_path.exists():
            try:
                pygame.mixer.music.load(str(music_path))
                pygame.mixer.music.set_volume(self.volume * 0.5)  # Music at half volume
                return True
            except pygame.error:
                return False
        return False

    def play_music(self, loops: int = -1) -> None:
        """
        Play background music

        Args:
            loops: Number of times to loop (-1 for infinite)
        """
        if not self.mixer_available or self.muted:
            return

        try:
            pygame.mixer.music.play(loops)
            self.music_playing = True
        except pygame.error:
            pass

    def stop_music(self) -> None:
        """Stop background music"""
        if not self.mixer_available:
            return

        try:
            pygame.mixer.music.stop()
            self.music_playing = False
        except pygame.error:
            pass

    def pause_music(self) -> None:
        """Pause background music"""
        if not self.mixer_available:
            return

        with contextlib.suppress(pygame.error):
            pygame.mixer.music.pause()

    def resume_music(self) -> None:
        """Resume background music"""
        if not self.mixer_available:
            return

        with contextlib.suppress(pygame.error):
            pygame.mixer.music.unpause()

    def set_volume(self, volume: float) -> None:
        """
        Set volume level

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))

        if not self.mixer_available:
            return

        # Update all sound effects
        for sound in self.sounds.values():
            sound.set_volume(self.volume)

        # Update music volume
        with contextlib.suppress(pygame.error):
            pygame.mixer.music.set_volume(self.volume * 0.5)

    def toggle_mute(self) -> bool:
        """
        Toggle mute state

        Returns:
            Current mute state (True if muted)
        """
        self.muted = not self.muted

        if not self.mixer_available:
            return self.muted

        if self.muted:
            self.pause_music()
        elif self.music_playing:
            self.resume_music()

        return self.muted


# Global instance for easy access
_global_sound_manager: SoundManager | None = None


def get_sound_manager() -> SoundManager:
    """
    Get the global sound manager instance

    Returns:
        The global SoundManager instance
    """
    global _global_sound_manager
    if _global_sound_manager is None:
        _global_sound_manager = SoundManager()
    return _global_sound_manager
