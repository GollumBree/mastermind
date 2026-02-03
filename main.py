from copy import deepcopy
from enum import Enum, auto
from functools import lru_cache


class Color(Enum):
    BLACK = 0
    WHITE = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    YELLOW = 5

type State = tuple[Color, Color, Color, Color]
type UnfinishedState = tuple[set[Color], set[Color], set[Color], set[Color]]


@lru_cache(maxsize=None)
def rate(state: State, sol: State) -> tuple[int, int]:
    black: int = sum(state[i] == sol[i] for i in range(4))
    gray: int = sum(state[i] in sol for i in range(4)) - black
    return black, gray


@lru_cache(maxsize=None)
def is_possible(
    guess: State, history: tuple[tuple[State, tuple[int, int]], ...]
) -> bool:
    for prev_guess, prev_rate in history:
        if rate(prev_guess, guess) != prev_rate:
            return False
    return True


@lru_cache(maxsize=None)
def minimax(
    pos: tuple[State, ...],
    history: tuple[tuple[State, tuple[int, int]], ...] = (),
    a=float("inf"),
    b=0,
) -> tuple[float, State | None]:
    if len(pos) == 1:
        return 0, pos[0]

    best = float("inf")
    best_move: State | None = None
    for c1 in Color:
        for c2 in Color:
            for c3 in Color:
                for c4 in Color:
                    if len(history)<2:
                        print("  "*len(history) + f"{((c1.value*6+c2.value)*6+c3.value)*6+c4.value}/{6**4}")
                    worst = 0
                    # worst_move: State | None = None
                    for sol in pos:
                        new_pos: tuple[State, ...] = tuple(
                            filter(lambda s: is_possible(s, history), pos)
                        )
                        res = minimax(
                            new_pos,
                            history
                            + (((c1, c2, c3, c4), rate((c1, c2, c3, c4), sol)),),
                            a, b
                        )
                        if res[0] > a:
                            break
                        if res[0] > worst:
                            worst = res[0]
                            b = max(b,worst)
                            # worst_move = res[1]
                    if worst < b:
                        return 0, None
                    if worst < best:
                        a = min(a,worst)
                        best = worst
                        best_move = (c1, c2, c3, c4)
    return best + 1, best_move


possibilities: tuple[State, ...] = tuple(
    (c1, c2, c3, c4) for c1 in Color for c2 in Color for c3 in Color for c4 in Color
)
print(minimax(possibilities))
