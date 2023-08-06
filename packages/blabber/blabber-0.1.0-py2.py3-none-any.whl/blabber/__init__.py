"""Blabber generates conversation starters."""

__version__ = "0.1.0"

import random
from pathlib import Path


class StarterGenerator:
    def _shuffle_starters(self):
        """Resets the generator's internal starter queue."""

        self.starters = random.sample(
            self.original_starters, len(self.original_starters)
        )

    def __init__(self):
        self.original_starters = set()

        data_dir = Path(__file__).parent / "data"

        for topic_path in data_dir.glob("*.txt"):
            with open(topic_path, encoding="utf-8") as topic_file:
                self.original_starters.update(
                    line.strip() for line in topic_file.readlines()
                )

        self._shuffle_starters()

    def starter(self):
        """Gets a fresh starter from the queue."""

        # If the queue is out of starters, re-shuffle
        if len(self.starters) == 0:
            self._shuffle_starters()

        # Get a random starter while also removing it from the queue
        return self.starters.pop()
