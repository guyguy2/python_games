"""Tests for the Snake game"""
import pytest
from games.snake.game import SnakeGame


def test_snake_game_initialization():
    """Test that SnakeGame can be initialized"""
    game = SnakeGame()
    assert game is not None


def test_snake_game_has_name():
    """Test that SnakeGame has a name property"""
    game = SnakeGame()
    assert game.name == "Snake"
    assert isinstance(game.name, str)


def test_snake_game_has_description():
    """Test that SnakeGame has a description property"""
    game = SnakeGame()
    assert game.description == "Eat food, grow longer, don't hit yourself!"
    assert isinstance(game.description, str)


def test_snake_game_has_run_method():
    """Test that SnakeGame has a run method"""
    game = SnakeGame()
    assert hasattr(game, 'run')
    assert callable(game.run)


def test_snake_game_inherits_from_base():
    """Test that SnakeGame inherits from BaseGame"""
    from games.base_game import BaseGame
    game = SnakeGame()
    assert isinstance(game, BaseGame)


def test_snake_game_properties_are_strings():
    """Test that all required properties are strings"""
    game = SnakeGame()
    assert isinstance(game.name, str)
    assert isinstance(game.description, str)
    assert len(game.name) > 0
    assert len(game.description) > 0
