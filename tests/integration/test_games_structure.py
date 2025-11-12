"""Tests for overall game structure and imports"""


def test_games_package_exists():
    """Test that games package can be imported"""
    import games

    assert games is not None


def test_base_game_can_be_imported():
    """Test that BaseGame can be imported"""
    from games.base_game import BaseGame

    assert BaseGame is not None


def test_snake_game_can_be_imported():
    """Test that SnakeGame can be imported"""
    from games.snake.game import SnakeGame

    assert SnakeGame is not None


def test_xonix_game_can_be_imported():
    """Test that XonixGame can be imported"""
    from games.xonix.game import XonixGame

    assert XonixGame is not None


def test_paratrooper_game_can_be_imported():
    """Test that ParatrooperGame can be imported"""
    from games.paratrooper.game import ParatrooperGame

    assert ParatrooperGame is not None


def test_all_games_are_accessible():
    """Test that all games can be instantiated"""
    from games.paratrooper.game import ParatrooperGame
    from games.snake.game import SnakeGame
    from games.xonix.game import XonixGame

    games = [SnakeGame(), XonixGame(), ParatrooperGame()]

    for game in games:
        assert game is not None
        assert hasattr(game, "name")
        assert hasattr(game, "description")
        assert hasattr(game, "run")


def test_game_names_are_unique():
    """Test that all game names are unique"""
    from games.paratrooper.game import ParatrooperGame
    from games.snake.game import SnakeGame
    from games.xonix.game import XonixGame

    games = [SnakeGame(), XonixGame(), ParatrooperGame()]

    names = [game.name for game in games]
    assert len(names) == len(set(names)), "Game names should be unique"
