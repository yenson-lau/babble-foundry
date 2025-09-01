"""
Non-interactive wrapper for Colossal Cave Adventure for turn-based play.

Modifies the port of Crowther and Woods' Colossal Cave Adventure game by
Brandon Rhodes (https://github.com/brandon-rhodes/python-adventure) to provide
a read/write interface instead of the fully interactive mode.

Original Adventure game engine:
Copyright 2010-2015 Brandon Rhodes

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import json
import re
from typing import Any
from adventure.game import Game
from adventure.model import Room
from adventure import load_advent_dat


INSTRUCTIONS = """
SOMEWHERE NEARBY IS COLOSSAL CAVE, WHERE OTHERS HAVE FOUND FORTUNES IN
TREASURE AND GOLD, THOUGH IT IS RUMORED THAT SOME WHO ENTER ARE NEVER
SEEN AGAIN.  MAGIC IS SAID TO WORK IN THE CAVE.  I WILL BE YOUR EYES
AND HANDS.  DIRECT ME WITH COMMANDS OF 1 OR 2 WORDS.  I SHOULD WARN
YOU THAT I LOOK AT ONLY THE FIRST FIVE LETTERS OF EACH WORD, SO YOU'LL
HAVE TO ENTER "NORTHEAST" AS "NE" TO DISTINGUISH IT FROM "NORTH".
(SHOULD YOU GET STUCK, TYPE "HELP" FOR SOME GENERAL HINTS.  FOR INFOR-
MATION ON HOW TO END YOUR ADVENTURE, ETC., TYPE "INFO".)
                              - - -
THIS PROGRAM WAS ORIGINALLY DEVELOPED BY WILLIE CROWTHER.  MOST OF THE
FEATURES OF THE CURRENT PROGRAM WERE ADDED BY DON WOODS (DON @ SU-AI).
CONTACT DON IF YOU HAVE ANY QUESTIONS, COMMENTS, ETC.
""".strip()


class ClossalCaveGame:
    """Non-interactive wrapper for the Clossal Cave Adventure game."""

    def __init__(self, seed=None):
        """Initialize a new game.

        Args:
            seed: Optional random seed for reproducible games
        """
        self._game = Game(seed)
        load_advent_dat(self._game)
        self._game.start()

        self.input('no')    # decline instructions

    def input(self, command_text):
        """Send a command to the game.

        Args:
            command_text: The command text (e.g., "get lamp", "north", "inventory")
        """
        if not command_text.strip():
            return

        # Parse command into words like the traditional mode does
        words = re.findall(r'\w+', command_text.lower())
        if words:
            self._pending_output = self._game.do_command(words)
        else:
            self._pending_output = ''

    @property
    def output(self) -> str:
        return self._game.output.rstrip('\n')

    @property
    def instructions(self) -> str:
        return INSTRUCTIONS

    @property
    def finished(self) -> bool:
        return self._game.is_finished or self._game.is_done

    @property
    def score(self) -> dict[str, int]:
        return dict(
            zip(
                ("current", "max"),
                self._game.compute_score(for_score_command=True)
            )
        )

    @property
    def turns(self):
        """Get the number of turns played.

        Returns:
            int: Number of turns
        """
        return self._game.turns

    @property
    def inventory(self):
        """Get the current inventory items.

        Returns:
            list: List of object names currently being carried
        """
        return [obj.names[0] for obj in self._game.inventory]

    @property
    def location(self) -> Room:
        """Get the current location description.

        Returns:
            str: Short description of current location
        """
        return self._game.loc

    @property
    def is_dead(self) -> bool:
        return self._game.is_dead

    @property
    def deaths(self) -> int:
        return self._game.deaths

    def get_status(self) -> dict[str, Any]:
        return {
            "turns": self.turns,
            "location": {
                "short_desc": self.location.short_description.strip(),
                "long_desc": self.location.long_description.strip()
            },
            "inventory": self.inventory,
            "score": self.score,
            "finished": self.finished,
            "dead": self.is_dead,
            "deaths": self.deaths
        }

    def save(self, filename: str):
        """Save the game state to a file.

        Args:
            filename: Path to save file
        """
        self._game.t_suspend('save', filename)

    @classmethod
    def load(cls, filename: str):
        """Load a saved game.

        Args:
            filename: Path to save file

        Returns:
            ClossalCaveGame: Loaded game instance
        """
        loaded_game = Game.resume(filename)

        # Create wrapper instance
        game = cls.__new__(cls)     # Create without calling __init__
        game._game = loaded_game
        game._pending_output = ''

        return game


if __name__ == '__main__':
    # Example usage:
    game = ClossalCaveGame()
    print("Starting description:", game.output)

    # Example game loop
    commands = ['east', 'get lamp', 'west', 'south', 'inventory']

    for cmd in commands:
        if game.finished:
            break

        print(f"\n> {cmd}")
        game.input(cmd)
        print(game.output)

    print(f"\nGame Status:")
    print(json.dumps(game.get_status(), indent=2))
