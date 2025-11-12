"""High score tracking system with persistent storage"""

import json
from pathlib import Path
from typing import Any


class HighScoreManager:
    """Manages high scores for games with persistent storage"""

    def __init__(self, storage_file: str = "high_scores.json"):
        """
        Initialize the high score manager

        Args:
            storage_file: Path to the JSON file for storing high scores
        """
        # Store in user's home directory for proper persistence
        self.storage_path = Path.home() / ".python_games" / storage_file
        self.scores: dict[str, list[dict[str, Any]]] = {}
        self._ensure_storage_dir()
        self._load_scores()

    def _ensure_storage_dir(self) -> None:
        """Ensure the storage directory exists"""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def _load_scores(self) -> None:
        """Load scores from the storage file"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path) as f:
                    self.scores = json.load(f)
            except (json.JSONDecodeError, OSError):
                # If file is corrupted or unreadable, start fresh
                self.scores = {}
        else:
            self.scores = {}

    def _save_scores(self) -> None:
        """Save scores to the storage file"""
        try:
            with open(self.storage_path, "w") as f:
                json.dump(self.scores, f, indent=2)
        except OSError:
            # Silently fail if we can't write - better than crashing the game
            pass

    def add_score(self, game_name: str, score: int | float, **metadata: Any) -> bool:
        """
        Add a new score for a game

        Args:
            game_name: Name of the game
            score: The score value
            **metadata: Additional metadata (e.g., level, date, player name)

        Returns:
            True if the score is a new high score (in top 10), False otherwise
        """
        if game_name not in self.scores:
            self.scores[game_name] = []

        # Create score entry
        score_entry = {"score": score, **metadata}

        # Add to list
        self.scores[game_name].append(score_entry)

        # Sort by score (descending) and keep top 10
        self.scores[game_name].sort(key=lambda x: x["score"], reverse=True)
        is_high_score = len(self.scores[game_name]) <= 10 or score_entry in self.scores[game_name][:10]
        self.scores[game_name] = self.scores[game_name][:10]

        # Save to disk
        self._save_scores()

        return is_high_score

    def get_high_scores(self, game_name: str, count: int = 10) -> list[dict[str, Any]]:
        """
        Get the top high scores for a game

        Args:
            game_name: Name of the game
            count: Number of scores to return (default: 10)

        Returns:
            List of score entries, sorted by score (descending)
        """
        if game_name not in self.scores:
            return []

        return self.scores[game_name][:count]

    def get_best_score(self, game_name: str) -> int | float | None:
        """
        Get the best score for a game

        Args:
            game_name: Name of the game

        Returns:
            The highest score, or None if no scores exist
        """
        scores = self.get_high_scores(game_name, 1)
        if scores:
            return scores[0]["score"]
        return None

    def clear_scores(self, game_name: str) -> None:
        """
        Clear all scores for a game

        Args:
            game_name: Name of the game
        """
        if game_name in self.scores:
            del self.scores[game_name]
            self._save_scores()


# Global instance for easy access
_global_manager: HighScoreManager | None = None


def get_high_score_manager() -> HighScoreManager:
    """
    Get the global high score manager instance

    Returns:
        The global HighScoreManager instance
    """
    global _global_manager
    if _global_manager is None:
        _global_manager = HighScoreManager()
    return _global_manager
