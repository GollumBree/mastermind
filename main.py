from copy import deepcopy
from enum import Enum, auto
from functools import lru_cache


class color(Enum):
    BLACK = auto()
    WHITE = auto()
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()

type State = tuple[color, color, color, color]
type UnfinishedState = tuple[set[color], set[color], set[color], set[color]]


@lru_cache(maxsize=None)
def rate(state: State, sol: State) -> tuple[int, int]:
    black: int = sum(state[i]==sol[i] for i in range(4))
    gray: int = sum(state[i] in sol for i in range(4)) - black
    return black, gray

@lru_cache(maxsize=None)
def is_possible(guess: State, history: tuple[tuple[State, tuple[int, int]], ...]) -> bool:
    for prev_guess, prev_rate in history:
        if rate(prev_guess, guess) != prev_rate:
            return False
    return True

@lru_cache(maxsize=None)
def minimax(pos: tuple[State,...], history: tuple[tuple[State, tuple[int, int]], ...] = ()) -> tuple[float, State | None]: 
    if len(pos) == 1:
        return 0, pos[0]
    
    best = float('inf')
    best_move: State | None = None
    for c1 in color:
        for c2 in color:
            for c3 in color:
                for c4 in color:
                    worst = float('-inf')
                    worst_move: State | None = None
                    for sol in pos:
                        new_pos: tuple[State,...] = tuple(filter(lambda s: is_possible(s, history), pos))
                        res = minimax(new_pos, history + (((c1, c2, c3, c4), rate((c1, c2, c3, c4), sol)),))
                        if res[0] < worst:
                            worst = res[0]
                            worst_move = res[1]
                    if worst > best:
                        best = worst
                        best_move = (c1, c2, c3, c4)
    return best, best_move

                        
possibilities: tuple[State, ...] = tuple((c1, c2, c3, c4) for c1 in color for c2 in color for c3 in color for c4 in color)
print(minimax(possibilities))