from collections import Counter, defaultdict
from itertools import product

# Mastermind: 4 Positionen, 6 Farben (0..5), Wiederholungen erlaubt
PEGS = 4
COLORS = 6


def score(guess, code):
    """
    Gibt Feedback als (schwarz, weiß) zurück:
    schwarz = richtige Farbe & Position
    weiß    = richtige Farbe falsche Position (ohne die schwarzen doppelt zu zählen)
    """
    blacks = sum(g == c for g, c in zip(guess, code))

    # Zähle nur die nicht-schwarzen Positionen für die Farbübereinstimmung
    g_rest = [g for g, c in zip(guess, code) if g != c]
    c_rest = [c for g, c in zip(guess, code) if g != c]

    cg = Counter(g_rest)
    cc = Counter(c_rest)

    whites = sum(min(cg[col], cc[col]) for col in cg)
    return (blacks, whites)


def all_codes():
    return list(product(range(COLORS), repeat=PEGS))


def knuth_next_guess(candidates, all_moves):
    """
    Minimax:
    Für jeden möglichen Zug m (aus all_moves) betrachten wir die Verteilung der Feedbacks
    gegen alle möglichen Codes in 'candidates'. Worst-Case = größte Bucket-Größe.
    Wir wählen m mit minimalem Worst-Case.
    Tie-break: bevorzuge Züge, die selbst Kandidaten sind.
    """
    best_move = None
    best_worst = float("inf")

    # Optional: kleine Optimierung – wenn nur 1 Kandidat übrig ist, nimm ihn direkt
    if len(candidates) == 1:
        return candidates[0]

    for move in candidates:
        buckets = defaultdict(int)
        for c in candidates:
            buckets[score(move, c)] += 1

        worst = max(buckets.values())

        if worst < best_worst:
            best_worst = worst
            best_move = move

    return best_move


def solve_interactive():
    """
    Interaktiv: Programm gibt den Zug aus, du gibst Feedback (schwarz weiß) ein.
    Farben eingeben als 0..5 (oder optional A..F -> wird gemappt).
    """
    all_moves = all_codes()
    candidates = all_moves.copy()

    # Knuth-Startzug: A A B B -> 0 0 1 1
    guess = (0, 0, 1, 1)

    print("Mastermind Knuth Solver (4 Pegs, 6 Farben)")
    print("Farben: 0..5 (optional A..F)")
    print("Feedback eingeben als: schwarz weiss  (z.B. '1 2')\n")

    for turn in range(1, 10):  # 5 reicht i.d.R., aber wir lassen etwas Luft
        print(f"Zug {turn}: {guess}")

        fb_in = input("Feedback (schwarz weiss): ").strip()
        if not fb_in:
            print("Abbruch.")
            return
        b, w = map(int, fb_in.split())

        if (b, w) == (4, 0):
            print(f"✅ Gelöst in {turn} Zügen! Code = {guess}")
            return

        # Kandidaten filtern
        candidates = [c for c in candidates if score(guess, c) == (b, w)]
        print(f"   Übrig mögliche Codes: {len(candidates)}")

        # Nächsten Zug per Minimax wählen
        guess = knuth_next_guess(candidates, all_moves)

    print("⚠️ Nicht gelöst (unerwartet). Prüfe Feedback-Eingaben.")


def solve_with_secret(secret):
    """
    Testmodus: secret vorgeben (Tuple aus 4 Zahlen 0..5).
    Das Programm spielt sich selbst durch.
    """
    all_moves = all_codes()
    candidates = all_moves.copy()
    guess = (0, 0, 1, 1)

    # print("Testmodus: secret =", secret)

    for turn in range(1, 10):
        fb = score(guess, secret)
        # print(f"Zug {turn}: {guess} -> Feedback {fb}")

        if fb == (4, 0):
            # print(f"✅ Gelöst in {turn} Zügen!")
            return turn

        candidates = [c for c in candidates if score(guess, c) == fb]
        guess = knuth_next_guess(candidates, all_moves)

    print("⚠️ Nicht gelöst (unerwartet).")
    return None


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
