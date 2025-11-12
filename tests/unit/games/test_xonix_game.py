"""Tests for the Xonix game"""

from games.xonix.game import XonixGame


def test_xonix_game_initialization():
    """Test that XonixGame can be initialized"""
    game = XonixGame()
    assert game is not None


def test_xonix_game_has_name():
    """Test that XonixGame has a name property"""
    game = XonixGame()
    assert hasattr(game, "name")
    assert isinstance(game.name, str)
    assert len(game.name) > 0


def test_xonix_game_has_description():
    """Test that XonixGame has a description property"""
    game = XonixGame()
    assert hasattr(game, "description")
    assert isinstance(game.description, str)
    assert len(game.description) > 0


def test_xonix_game_has_run_method():
    """Test that XonixGame has a run method"""
    game = XonixGame()
    assert hasattr(game, "run")
    assert callable(game.run)


def test_xonix_game_inherits_from_base():
    """Test that XonixGame inherits from BaseGame"""
    from games.base_game import BaseGame

    game = XonixGame()
    assert isinstance(game, BaseGame)
