"""
Base game class that all games should inherit from
"""
from abc import ABC, abstractmethod


class BaseGame(ABC):
    """Base class for all games"""

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
    @abstractmethod
    def name(self) -> str:
        """Return the game name"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a short game description"""
        pass
