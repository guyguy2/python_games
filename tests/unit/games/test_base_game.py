"""Tests for the BaseGame abstract class"""

import pytest

from games.base_game import BaseGame


class ConcreteGame(BaseGame):
    """Concrete implementation of BaseGame for testing"""

    def __init__(self):
        self._name = "Test Game"
        self._description = "A test game"

    def run(self):
        """Run the game"""
        return "Game ran successfully"

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description


def test_base_game_cannot_be_instantiated():
    """Test that BaseGame cannot be instantiated directly"""
    with pytest.raises(TypeError):
        BaseGame()


def test_concrete_game_has_required_properties():
    """Test that concrete implementation has all required properties"""
    game = ConcreteGame()
    assert hasattr(game, "name")
    assert hasattr(game, "description")
    assert hasattr(game, "run")


def test_concrete_game_properties():
    """Test that concrete game properties return correct values"""
    game = ConcreteGame()
    assert game.name == "Test Game"
    assert game.description == "A test game"
    assert isinstance(game.name, str)
    assert isinstance(game.description, str)


def test_concrete_game_run_method():
    """Test that concrete game run method works"""
    game = ConcreteGame()
    result = game.run()
    assert result == "Game ran successfully"


def test_incomplete_implementation_fails():
    """Test that incomplete implementation raises TypeError"""
    with pytest.raises(TypeError):

        class IncompleteGame(BaseGame):
            pass

        IncompleteGame()
