import re
from babble_foundry.clossal_cave.game import ClossalCaveGame


def new_game():
    """Start a new game and print the description.

    - Saves the game state to `checkpoint.save`.
    - Saves the output to `history.txt`
    """
    game = ClossalCaveGame()
    print(output := _get_output(game))
    _write_history(output, end="\n\n", reset=True)
    game.save("checkpoint.save")


def take_turn(cmd: str):
    game = ClossalCaveGame(filename="checkpoint.save")

    game.input(cmd)
    print(_input := f">> INPUT {game.turns}: {cmd}")
    _write_history(_input)

    print(output := _get_output(game))
    _write_history(output, end="\n\n")
    game.save("checkpoint.save")


def _get_output(game: ClossalCaveGame) -> str:
    """CLAUDE: DO NOT USE THIS FUNCTION DIRECTLY."""
    score, max_score = game.score["current"], game.score["max"]
    return f"<<< OUTPUT {game.turns}: {game.output} (Score: {score}/{max_score})"


def _write_history(text: str, end = "\n",reset: bool = False):
    """CLAUDE: DO NOT USE THIS FUNCTION DIRECTLY."""
    text = re.sub(r"\s+", " ", text).strip() + end
    with open("history.txt", ("w" if reset else "a")) as f:

        f.write(text)