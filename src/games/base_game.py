"""
Base game class that all games should inherit from
"""

from abc import ABC, abstractmethod


class BaseGame(ABC):
    """
    Base class for all games

    Subclasses should define GAME_NAME and GAME_DESCRIPTION as class attributes
    for metadata that can be accessed without instantiation.
    """

    # Class-level metadata (should be overridden by subclasses)
    GAME_NAME: str = "Unknown Game"
    GAME_DESCRIPTION: str = "No description available"

    @abstractmethod
    def __init__(self):
        """Initialize the game"""
        pass

    @abstractmethod
    def run(self):
        """
        Run the game (blocking call).
        Should return when the game ends.
        """
        pass

    @property
    def name(self) -> str:
        """Return the game name"""
        return self.GAME_NAME

    @property
    def description(self) -> str:
        """Return a short game description"""
        return self.GAME_DESCRIPTION
