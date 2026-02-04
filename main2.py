from collections import Counter, defaultdict
from enum import Enum
from itertools import product


class Color(Enum):
    BLACK = 0
    WHITE = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    YELLOW = 5


_all_codes = list(product(Color, repeat=4))
all_codes = _all_codes.copy


def score(guess, code):
    blacks = sum(g == c for g, c in zip(guess, code))

    g_rest = [g for g, c in zip(guess, code) if g != c]
    c_rest = [c for g, c in zip(guess, code) if g != c]

    cg = Counter(g_rest)
    cc = Counter(c_rest)

    whites = sum(min(cg[col], cc[col]) for col in cg)
    return (blacks, whites)


def next_guess(candidates):

    best_move = None
    best_worst = float("inf")
    is_candidate: bool = False

    if len(candidates) == 1:
        return candidates[0]

    for move in all_codes():
        scores = defaultdict(int)
        for c in candidates:
            scores[score(move, c)] += 1

        worst = max(scores.values())

        if worst < best_worst or (
            worst == best_worst and move in candidates and not is_candidate
        ):
            best_worst = worst
            best_move = move
            is_candidate = move in candidates

    return best_move


def solve_interactive():
    candidates = all_codes()
    guess = next_guess(candidates)

    for turn in range(1, 10):
        print(f"Zug {turn}: {" ".join(color.name for color in guess)}")

        fb_in = input("Feedback (schwarz grau): ").strip()
        if not fb_in:
            print("Abbruch.")
            return
        b, w = map(int, fb_in.split())

        if (b, w) == (4, 0):
            print("Gelöst!")
            return

        candidates = [c for c in candidates if score(guess, c) == (b, w)]
        print(f"Noch {len(candidates)} mögliche Codes")

        guess = next_guess(candidates)

    raise RuntimeError("Nicht gelöst.")


def solve_with_secret(secret):
    candidates = all_codes()
    guess = next_guess(candidates)

    for turn in range(1, 10):
        fb = score(guess, secret)

        if fb == (4, 0):
            return turn

        candidates = [c for c in candidates if score(guess, c) == fb]
        guess = next_guess(candidates)
    raise RuntimeError("Nicht gelöst.")


if __name__ == "__main__":
    solve_interactive()
    # results = [0] * 10
    # for test_code in all_codes()[250:500]:
    #     # print("\n---\n")
    #     results[solve_with_secret(test_code)] += 1
    # print("Verteilung der Lösungszüge über alle Codes:")
    # for turns, count in enumerate(results):
    #     if count > 0:
    #         print(f"{turns} Züge: {count} Codes")
