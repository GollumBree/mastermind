from copy import deepcopy
from enum import Enum, auto
from functools import lru_cache
import multiprocessing
import traceback
import sys

sys.setrecursionlimit(10**7)


class color(Enum):
    BLACK = 0
    WHITE = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    YELLOW = 5


type State = tuple[color, color, color, color]
type UnfinishedState = tuple[set[color], set[color], set[color], set[color]]


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
    debug=False,
) -> tuple[float, State | None]:
    return minimax_ab(pos, history, float("-inf"), float("inf"), debug)


@lru_cache(maxsize=None)
def minimax_ab(
    pos: tuple[State, ...],
    history: tuple[tuple[State, tuple[int, int]], ...],
    alpha: float,
    beta: float,
    debug=False,
) -> tuple[float, State | None]:
    if len(pos) == 1:
        return 0, pos[0]
    if len(history) >= 3:
        return float("inf"), None
    
    best = float("-inf")
    best_move: State | None = None
    for c1 in color:
        for c2 in color:
            for c3 in color:
                for c4 in color:
                    if debug:
                        print(
                            f"{c1.value*6*6*6 + c2.value*6*6 + c3.value*6 + c4.value} / {6**4}"
                        )
                    worst = float("inf")
                    worst_move: State | None = None
                    for sol in pos:
                        new_pos: tuple[State, ...] = tuple(
                            filter(lambda s: is_possible(s, history), pos)
                        )
                        res = minimax_ab(
                            new_pos,
                            history
                            + (((c1, c2, c3, c4), rate((c1, c2, c3, c4), sol)),),
                            alpha,
                            beta,
                            debug,
                        )
                        if res[0] < worst:
                            worst = res[0]
                            worst_move = res[1]
                        # Beta cutoff: minimizer found a move better than alpha
                        beta = min(beta, worst)
                        if beta <= alpha:
                            break
                    if worst > best:
                        best = worst
                        best_move = (c1, c2, c3, c4)
                    # Alpha cutoff: maximizer found a move better than beta
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        if beta <= alpha:
            break
    return best, best_move


def mmxstep(c1, c2, c3, c4, dict_, pos):
    sys.setrecursionlimit(10**7)
    print(f"{c1.value*6*6*6 + c2.value*6*6 + c3.value*6 + c4.value} / {6**4} step")
    worst = float("inf")
    worst_move: State | None = None

    for sol in pos:
        new_pos: tuple[State, ...] = pos
        #print(1)
        try:
            res = minimax(new_pos, (((c1, c2, c3, c4), rate((c1, c2, c3, c4), sol)),))
        except Exception as e:
            traceback.print_exc()
            raise e
        #print(2)
        if res[0] < worst:
            worst = res[0]
            worst_move = res[1]
    if worst > dict_["best"]:
        dict_["best"] = worst
        dict_["best_move"] = (c1, c2, c3, c4)
    print(
        f"{c1.value*6*6*6 + c2.value*6*6 + c3.value*6 + c4.value} / {6**4} finished",
        dict_,
    )


def minimax_chef(
    pos: tuple[State, ...],
    history: tuple[tuple[State, tuple[int, int]], ...] = (),
    debug=False,
) -> tuple[float, State | None]:
    if len(pos) == 1:
        return 0, pos[0]

    pool = multiprocessing.Pool(processes=4)
    best = float("-inf")
    best_move: State | None = None
    dict_ = {"best": best, "best_move": best_move}
    # pool.map(lambda x: mmxstep(*x, dict_), [])
    for c1 in color:
        for c2 in color:
            for c3 in color:
                for c4 in color:
                    pool.apply_async(
                        mmxstep, args=(c1, c2, c3, c4, dict_, pos),
                    )
    pool.close()
    pool.join()
    return dict_["best"], dict_["best_move"]


possibilities: tuple[State, ...] = tuple(
    (c1, c2, c3, c4) for c1 in color for c2 in color for c3 in color for c4 in color
)
print(minimax_chef(possibilities))
