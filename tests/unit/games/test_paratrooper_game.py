"""Tests for the Paratrooper game"""

from games.paratrooper.game import ParatrooperGame


def test_paratrooper_game_initialization():
    """Test that ParatrooperGame can be initialized"""
    game = ParatrooperGame()
    assert game is not None


def test_paratrooper_game_has_name():
    """Test that ParatrooperGame has a name property"""
    game = ParatrooperGame()
    assert hasattr(game, "name")
    assert isinstance(game.name, str)
    assert len(game.name) > 0


def test_paratrooper_game_has_description():
    """Test that ParatrooperGame has a description property"""
    game = ParatrooperGame()
    assert hasattr(game, "description")
    assert isinstance(game.description, str)
    assert len(game.description) > 0


def test_paratrooper_game_has_run_method():
    """Test that ParatrooperGame has a run method"""
    game = ParatrooperGame()
    assert hasattr(game, "run")
    assert callable(game.run)


def test_paratrooper_game_inherits_from_base():
    """Test that ParatrooperGame inherits from BaseGame"""
    from games.base_game import BaseGame

    game = ParatrooperGame()
    assert isinstance(game, BaseGame)
