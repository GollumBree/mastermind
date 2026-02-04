from enum import Enum
from functools import lru_cache
from line_profiler import profile


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
    exact = 0
    sc = [0, 0, 0, 0, 0, 0]
    gc = [0, 0, 0, 0, 0, 0]

    for s, g in zip(sol, state):
        if s == g:
            exact += 1
        else:
            sc[s.value] += 1
            gc[g.value] += 1

    value_only = (
        min(sc[0], gc[0])
        + min(sc[1], gc[1])
        + min(sc[2], gc[2])
        + min(sc[3], gc[3])
        + min(sc[4], gc[4])
        + min(sc[5], gc[5])
    )

    return exact, value_only


# @lru_cache(maxsize=None)
def is_possible(
    guess: State, history: tuple[tuple[State, tuple[int, int]], ...]
) -> bool:
    for prev_guess, prev_rate in history:
        if rate(prev_guess, guess) != prev_rate:
            return False
    return True


@lru_cache(maxsize=None)
@profile
def minimax(
    pos: tuple[State, ...],
    history: tuple[tuple[State, tuple[int, int]], ...] = (),
    a=float("inf"),
    b=-1,
) -> tuple[float, State | None]:
    if len(history) >= 5:
        return float("inf"), None

    pos = tuple(filter(lambda s: is_possible(s, history), pos))

    if len(pos) == 1:
        return 0, pos[0]

    best = float("inf")
    best_move: State | None = None
    for c1 in (Color.BLACK, Color.WHITE):
        for c2 in (Color.BLACK, Color.WHITE):
            for c3 in (Color.BLACK, Color.WHITE):
                for c4 in (Color.BLACK, Color.WHITE):
                    if len(history) < 2:
                        print(
                            "  " * len(history)
                            + f"{((c1.value * 2 + c2.value) * 2 + c3.value) * 2 + c4.value + 1}/{16}"
                        )
                    worst = -1
                    # worst_move: State | None = None
                    for i, sol in enumerate(pos):
                        # for sol in pos:
                        if len(history) < 1:
                            print("  " * len(history) + f" {i + 1}/{len(pos)}")

                        res = minimax(
                            pos,
                            history
                            + (((c1, c2, c3, c4), rate((c1, c2, c3, c4), sol)),),
                            a,
                            b,
                        )

                        if res[0] > worst:
                            worst = res[0]
                            if res[0] > a:
                                # print("pruning a:", res[0], ">", a)
                                break
                            b = max(b, worst)
                            # if worst == float("inf"):
                            #     raise Exception(history)
                            # worst_move = res[1]
                    if worst < best:
                        best = worst
                        best_move = (c1, c2, c3, c4)
                        if worst < b:
                            # print("pruning b:", worst, "<", b)
                            return best + 1, best_move
                        a = min(a, worst)
    # if best_move is not None:
    #     print("returning:", best + 1, best_move)
    return best + 1, best_move


possibilities: tuple[State, ...] = tuple(
    (c1, c2, c3, c4)
    for c1 in (Color.BLACK, Color.WHITE)
    for c2 in (Color.BLACK, Color.WHITE)
    for c3 in (Color.BLACK, Color.WHITE)
    for c4 in (Color.BLACK, Color.WHITE)
)
history: tuple[tuple[State, tuple[int, int]], ...] = ()
SOL = (
    Color.BLACK,
    Color.WHITE,
    Color.BLACK,
    Color.WHITE,
)  # The actual solution for testing
while True:
    moves, best_move = minimax(possibilities)
    print("Best move:", best_move, "in", moves, "moves")
    history += ((best_move, rate(best_move, SOL)),)
    possibilities = tuple(filter(lambda s: is_possible(s, history), possibilities))
    print("Remaining possibilities:", len(possibilities))
    if len(possibilities) == 1:
        print("Solution found:", possibilities[0])
        break
