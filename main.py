from collections import defaultdict
from enum import Enum
from functools import lru_cache
from itertools import product
import sys
from plruc import plruc as persistent_lru_cache


SLOTS = 4


class Color(Enum):
    BLACK = 0
    WHITE = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    YELLOW = 5


_all_codes = list(product(Color, repeat=SLOTS))
all_codes = _all_codes.copy

@lru_cache(maxsize=None)
def rate(state: tuple[Color, ...], sol: tuple[Color, ...]) -> tuple[int, int]:
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

@lru_cache(maxsize=None)
@persistent_lru_cache
def next_guess(candidates, debug=False):

    best_move = None
    best_worst = float("inf")
    is_candidate: bool = False

    if len(candidates) == 1:
        return candidates[0]

    for i, move in enumerate(all_codes()):
        if debug:
            print(
                f"Evaluating move {i+1}/{len(_all_codes)}: {' '.join(color.name for color in move)}...                          ",
                end="\r",
            )
        scores = defaultdict(int)
        for c in candidates:
            scores[rate(move, c)] += 1

        if len(scores) == 0:
            print("Unmöglicher Zustand, Eingaben überprüfen!")
            sys.exit(42)

        worst = max(scores.values())

        if worst < best_worst or (
            worst == best_worst and move in candidates and not is_candidate
        ):
            best_worst = worst
            best_move = move
            is_candidate = move in candidates

    return best_move


def solve_interactive():
    candidates = tuple(all_codes())
    guess = next_guess(candidates, debug=True)

    for turn in range(1, 20):
        print(f"Zug {turn}: {' '.join(color.name for color in guess)}")

        while True:
            fb_in = input("Feedback (schwarz grau): ").replace(",", "").replace(" ", "")
            if len(fb_in) == 2 and all(
                c in "".join(str(i) for i in range(SLOTS + 1)) for c in fb_in
            ):
                break
            else:
                print(f"Bitte zwei Zahlen (<{SLOTS+1}) eingeben.")

        b, w = map(int, fb_in)

        if (b, w) == (SLOTS, 0):
            print("Gelöst!")
            return

        candidates = tuple(c for c in candidates if rate(guess, c) == (b, w))
        print(f"Noch {len(candidates)} mögliche Codes")

        guess = next_guess(candidates, debug=True)
        print("Evaluated.")

    raise RuntimeError("Nicht gelöst.")


def solve_with_secret(secret):
    candidates = tuple(all_codes())
    guess = next_guess(candidates, debug=True)

    for turn in range(1, 20):
        fb = rate(guess, secret)

        if fb == (SLOTS, 0):
            return turn

        candidates = tuple(c for c in candidates if rate(guess, c) == fb)
        guess = next_guess(candidates)
    raise RuntimeError("Nicht gelöst.")


if __name__ == "__main__":
    if sys.argv[-1] in ("--test", "_-_i-am-crazy-and-want-to-test-all-codes"):
        results = [0] * 20
        for i, test_code in enumerate(all_codes()):
            results[solve_with_secret(test_code)] += 1
            print(f"Code {i+1:>4}/{len(_all_codes)} gelöst.", end="\r")
        print("Verteilung der Lösungszüge über alle Codes:")
        for turns, count in enumerate(results):
            if count > 0:
                print(
                    f"{turns} {'Züge:' if turns > 1 else 'Zug: '} {count:>4} Codes ({f'{count/len(_all_codes)*100:.2f}':>5}%)"
                )
    else:
        solve_interactive()
